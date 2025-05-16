import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("🚧 Mapa Interativo - Condições Perigosas nas Estradas")

st.markdown("""
Este aplicativo permite visualizar locais com **perigos em estradas** com base no indicador `ICMNP`.
Os dados passam por **tratamento**, são **classificados** em níveis de severidade e **exibidos em um mapa interativo**.
""")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("📁 Faça upload do arquivo CSV contendo as colunas 'Latitude', 'Longitude', 'ICMNP'...", type=["csv"])

if uploaded_file is not None:
    # Carregar dados
    df = pd.read_csv(uploaded_file)

    # ---------- LIMPEZA E TRATAMENTO DE DADOS ----------
    # Remover linhas com valores nulos nas colunas essenciais
    df = df.dropna(subset=['Latitude', 'Longitude', 'ICMNP'])

    # Converter para tipo numérico (se necessário)
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['ICMNP'] = pd.to_numeric(df['ICMNP'], errors='coerce')

    # Remover linhas com coordenadas inválidas
    df = df[(df['Latitude'].between(-90, 90)) & (df['Longitude'].between(-180, 180))]

    # Novamente remover valores nulos após conversão
    df = df.dropna(subset=['Latitude', 'Longitude', 'ICMNP'])

    # Exibir prévia
    st.subheader("🔍 Pré-visualização dos Dados Tratados")
    st.dataframe(df)

    # ---------- CLASSIFICAÇÃO BASEADA EM QUARTIS ----------
    Q1 = df['ICMNP'].quantile(0.25)
    Q2 = df['ICMNP'].quantile(0.50)
    Q3 = df['ICMNP'].quantile(0.75)

    def categorize_severity(icmnp_value):
        if icmnp_value <= Q1:
            return 'Baixo'
        elif icmnp_value <= Q2:
            return 'Médio'
        elif icmnp_value <= Q3:
            return 'Alto'
        else:
            return 'Crítico'

    df['condicao'] = df['ICMNP'].apply(categorize_severity)

    # ---------- MAPA INTERATIVO ----------
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)

    cor_condicao = {
        'Baixo': 'green',
        'Médio': 'orange',
        'Alto': 'red',
        'Crítico': 'darkred'
    }

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"<b>ICMNP:</b> {row['ICMNP']:.2f}<br><b>Condição:</b> {row['condicao']}",
            icon=folium.Icon(color=cor_condicao.get(row['condicao'], 'gray'))
        ).add_to(marker_cluster)

    st.subheader("🗺️ Mapa com Classificação de Condição")
    st_folium(m, width=1000, height=600)

else:
    st.info("💡 Por favor, envie um arquivo CSV contendo as colunas 'Latitude', 'Longitude' e 'ICMNP'.")
