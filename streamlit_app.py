import streamlit as st
import requests
import json

# Configuración básica de la página
st.set_page_config(page_title="ORCA Strategic OS", layout="wide")

# Estilos ejecutivos sin iconos
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        width: 100%; background: #007BFF; color: white;
        border-radius: 4px; padding: 12px; font-weight: bold; border: none;
    }
    .report-card {
        background-color: #161B22; padding: 25px; border-radius: 8px;
        border: 1px solid #30363D; color: #E6EDF3;
    }
    </style>
    """, unsafe_allow_html=True)

# Motor de conexión ultra-directa
def call_ia(prompt):
    # API KEY integrada
    key = "AIzaSyBvG3EIcwLXZE9LxFFJ9lOPplk7FCoIeDs"
    
    # URL forzada a v1 (la versión más estable de Google)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        
        if response.status_code == 200:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: {data.get('error', {}).get('message', 'Fallo de servidor')}"
    except Exception as e:
        return f"Error critico: {str(e)}"

# Interfaz limpia
st.title("ORCA Strategic OS")
st.text("Plataforma de Consultoria Estrategica")

with st.sidebar:
    st.header("Parametros")
    ubicacion = st.text_input("Ubicacion", value="Ecuador")
    st.info("Sistema conectado a Google AI v1")

st.markdown("### Analisis de Activos")
enlaces = st.text_area("Pega los links aqui:", height=150)

if st.button("EJECUTAR ESTRATEGIA"):
    if not enlaces:
        st.warning("Ingresa los enlaces para analizar.")
    else:
        with st.spinner("Procesando..."):
            instruccion = f"Analiza estos perfiles: {enlaces}. Contexto: {ubicacion}. Genera estrategia de marketing, paleta de colores y plan de 7 dias."
            resultado = call_ia(instruccion)
            
            if "Error" in resultado:
                st.error(resultado)
            else:
                st.divider()
                st.markdown(f'<div class="report-card">{resultado}</div>', unsafe_allow_html=True)
