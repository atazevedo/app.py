import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("🚧 Mapa Interativo - Condições Perigosas nas Estradas")

st.markdown("""
Este aplicativo permite visualizar locais com **perigos em estradas** com base em um indicador `ICMNP`.
Os locais são classificados automaticamente em **níveis de severidade** com base nos quartis desse indicador.
""")

# Upload do CSV
uploaded_file = st.file_uploader("📁 Faça upload do arquivo CSV contendo as colunas 'latitude', 'longitude' e 'ICMNP'", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Pré-visualização dos Dados")
    st.dataframe(df)

    # Verificação de colunas obrigatórias
    if all(col in df.columns for col in ['latitude', 'longitude', 'ICMNP']):
        
        # Calcular quartis
        Q1 = df['ICMNP'].quantile(0.25)
        Q2 = df['ICMNP'].quantile(0.50)
        Q3 = df['ICMNP'].quantile(0.75)

        # Função para classificar severidade
        def categorize_severity(icmnp_value):
            if icmnp_value <= Q1:
                return 'Baixo'
            elif icmnp_value <= Q2:
                return 'Médio'
            elif icmnp_value <= Q3:
                return 'Alto'
            else:
                return 'Crítico'

        # Criar a coluna 'condicao'
        df['condicao'] = df['ICMNP'].apply(categorize_severity)

        # Mapa
        m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)
        marker_cluster = MarkerCluster().add_to(m)

        # Cores associadas à condição
        cor_condicao = {
            'Baixo': 'green',
            'Médio': 'orange',
            'Alto': 'red',
            'Crítico': 'darkred'
        }

        for _, row in df.iterrows():
            lat = row['latitude']
            lon = row['longitude']
            cond = row['condicao']
            icmnp = row['ICMNP']

            folium.Marker(
                location=[lat, lon],
                popup=f"<b>ICMNP:</b> {icmnp:.2f}<br><b>Condição:</b> {cond}",
                icon=folium.Icon(color=cor_condicao.get(cond, 'gray'), icon="exclamation-sign")
            ).add_to(marker_cluster)

        st.subheader("🗺️ Mapa com Classificação de Condição")
        st_folium(m, width=1000, height=600)
    else:
        st.error("⚠️ O CSV precisa conter as colunas: latitude, longitude e ICMNP.")
else:
    st.info("💡 Por favor, faça upload de um CSV contendo as colunas 'latitude', 'longitude' e 'ICMNP'.")
