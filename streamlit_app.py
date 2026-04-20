import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ORCA Strategic OS", layout="wide")

# --- ESTILOS PROFESIONALES (SIN ICONOS) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        width: 100%; background: #007BFF; color: white;
        border-radius: 4px; padding: 12px; font-weight: bold; border: none;
    }
    .report-card {
        background-color: #161B22; padding: 25px; border-radius: 8px;
        border: 1px solid #30363D; color: #E6EDF3; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGENCIA (OPENAI) ---
def call_openai_ia(prompt):
    # Tu clave de OpenAI integrada
    api_key = "Sk-proj-ie8te5OSr0dburrHjf8fHMu16ZwFKiiPjzleUwY9dqolEZIx8Jtry6nhfuySvbAhhttNk2PmT3T3BlbkFJNEBynFQltB68Y4P5_r2Hyh86OYmRkfw83Kaid97nGj3MO1BliHDH6omrf-wSJOEgv_or7couYA"
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "Eres un consultor de marketing y branding senior para ORCA Studios."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200:
            return result['choices'][0]['message']['content']
        else:
            error_msg = result.get('error', {}).get('message', 'Fallo de autenticacion o saldo')
            return f"Error de OpenAI ({response.status_code}): {error_msg}"
    except Exception as e:
        return f"Error critico de conexion: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("ORCA Strategic OS")
st.text("Plataforma de Consultoria Estrategica")

with st.sidebar:
    st.header("Configuracion")
    ubicacion = st.text_input("Ubicacion del Mercado", value="Ecuador")
    st.success("Conectado via OpenAI (GPT-4o)")

st.markdown("### Analisis de Activos Digitales")
enlaces = st.text_area("Pega los enlaces (Instagram, TikTok, Web):", height=150)

if st.button("EJECUTAR ESTRATEGIA"):
    if not enlaces:
        st.warning("Por favor, ingresa los enlaces para comenzar el analisis.")
    else:
        with st.spinner("Analizando perfiles y generando estrategia..."):
            instruccion = f"""
            Analiza los siguientes perfiles: {enlaces}
            Mercado objetivo: {ubicacion}
            
            Genera un reporte ejecutivo detallado con:
            1. Analisis de la audiencia local en {ubicacion}.
            2. Estrategia de contenidos y pilares de marca.
            3. Sugerencia visual y paleta de colores (Codigos HEX).
            4. Plan de contenidos de 7 dias (Temas y formatos).
            5. Recomendaciones de escalabilidad.
            """
            
            reporte = call_openai_ia(instruccion)
            
            if "Error" in reporte:
                st.error(reporte)
            else:
                st.divider()
                st.markdown(f"## Estrategia para {ubicacion}")
                st.markdown(f'<div class="report-card">{reporte}</div>', unsafe_allow_html=True)
                st.download_button("Descargar Reporte", reporte, file_name=f"Estrategia_ORCA_{ubicacion}.md")
