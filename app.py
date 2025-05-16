import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("📍 Mapa Interativo - Condições das Estradas")

st.write("Este aplicativo mostra um mapa com condições das estradas baseado em dados geográficos.")

# Upload do arquivo CSV ou leitura padrão
uploaded_file = st.file_uploader("Faça upload do arquivo CSV com dados das estradas", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Pré-visualização dos Dados")
    st.dataframe(df)

    # Verifica colunas necessárias
    if all(col in df.columns for col in ['latitude', 'longitude', 'condicao']):
        m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)

        for _, row in df.iterrows():
            cor = 'green'
            if row['condicao'] == 'Ruim':
                cor = 'red'
            elif row['condicao'] == 'Regular':
                cor = 'orange'

            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=6,
                color=cor,
                fill=True,
                fill_opacity=0.7,
                popup=f"Condição: {row['condicao']}"
            ).add_to(m)

        st.subheader("🗺️ Mapa Gerado")
        st_folium(m, width=1000, height=600)
    else:
        st.error("O CSV deve conter as colunas: latitude, longitude e condicao.")
else:
    st.info("Por favor, faça o upload de um arquivo CSV com dados geográficos.")
