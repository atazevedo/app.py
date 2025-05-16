igoimport streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

 # Define severity levels based on quartiles
 def categorize_severity(icmnp_value):
    if icmnp_value <= Q1:
       return 'Low'
    elif icmnp_value <= Q2:
       return 'Medium'
    elif icmnp_value <= Q3:
       return 'High'
    else:
       return 'Critical'

st.set_page_config(layout="wide")
st.title("🚧 Mapa Interativo - Locais com Perigos nas Estradas")

st.markdown("""
Este aplicativo permite visualizar locais com registros de **perigos em estradas** 
com base em dados geográficos. Faça upload de um arquivo CSV contendo latitude, longitude, e descrição do perigo.
""")

# Upload do CSV
uploaded_file = st.file_uploader("📁 Faça upload do arquivo CSV com os perigos registrados", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Calculate quartiles for ICMNP
    Q1 = df['ICMNP'].quantile(0.25) 
    Q2 = df['ICMNP'].quantile(0.5)
    Q3 = df['ICMNP'].quantile(0.75)

    # Create the 'perigo' column
    df['perigo'] = df['ICMNP'].apply(categorize_severity)

    st.subheader("🔍 Pré-visualização dos Dados")
    st.dataframe(df)

    # Verificar colunas obrigatórias
    if all(col in df.columns for col in ['latitude', 'longitude', 'perigo']):
        m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=6)
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in df.iterrows():
            perigo = row['perigo']
            cor = 'blue'
            if 'acidente' in perigo.lower():
                cor = 'red'
            elif 'deslizamento' in perigo.lower():
                cor = 'orange'
            elif 'alagamento' in perigo.lower():
                cor = 'darkblue'

            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Perigo: {perigo}",
                icon=folium.Icon(color=cor, icon="exclamation-sign")
            ).add_to(marker_cluster)

        st.subheader("🗺️ Mapa Gerado")
        st_folium(m, width=1000, height=600)
    else:
        st.error("⚠️ O CSV deve conter as colunas: latitude, longitude e perigo.")
else:
    st.info("💡 Por favor, faça o upload de um arquivo CSV com as colunas: latitude, longitude e perigo.")
