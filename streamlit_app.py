import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="ORCA Strategic OS", layout="wide")

def ejecutar_estrategia(prompt):
    # Intentar leer la clave de los Secrets de Streamlit
    try:
        api_key = st.secrets["OPENAI_API_KEY"].strip()
    except Exception:
        return "Error: No se configuró la clave en 'Misterios' (Secrets)."

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Eres un consultor senior de marketing para ORCA Studios."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error de OpenAI: {response.text}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# Interfaz
st.title("ORCA Strategic OS")
enlaces = st.text_area("Activos a Analizar (Links):")

if st.button("EJECUTAR ESTRATEGIA"):
    if not enlaces:
        st.error("Pega los enlaces primero.")
    else:
        with st.spinner("Generando consultoría..."):
            resultado = ejecutar_estrategia(f"Genera una estrategia para: {enlaces}")
            st.markdown(resultado)
