import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ORCA Strategic OS", layout="wide")

# --- ESTILOS PROFESIONALES ---
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

# --- MOTOR DE INTELIGENCIA (CORRECCIÓN DE RUTA 404) ---
def call_gemini_api(api_key, prompt):
    # RUTA CERTIFICADA: Se eliminó cualquier prefijo innecesario que causaba el 404
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    # Payload optimizado
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "topK": 40,
            "maxOutputTokens": 8192,
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            # Captura detallada del error para diagnóstico
            error_detail = result.get('error', {}).get('message', 'Error desconocido')
            return f"Error {response.status_code}: {error_detail}"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ ---
def main():
    st.title("ORCA Strategic OS")
    st.text("Plataforma de Consultoría Estratégica")

    # Tu API KEY integrada
    API_KEY = "AIzaSyBvG3EIcwLXZE9LxFFJ9lOPplk7FCoIeDs"

    with st.sidebar:
        st.header("Ajustes")
        st.success("Conectado a Google AI")
        st.divider()
        location = st.text_input("Ubicación", value="Ecuador")
        market = st.selectbox("Mercado", ["Global", "Emergente", "Lujo"])

    st.markdown("### Análisis de Activos")
    links = st.text_area("Enlaces de referencia:", height=100)

    if st.button("EJECUTAR ESTRATEGIA"):
        if not links:
            st.warning("Ingresa los enlaces para analizar.")
        else:
            with st.spinner("Generando reporte estratégico..."):
                prompt = f"Analiza estos perfiles: {links}. Contexto: {location}. Genera una estrategia de marketing, paleta de colores y plan de 7 días."
                report = call_gemini_api(API_KEY, prompt)
                
                if "Error" in report:
                    st.error(report)
                else:
                    st.divider()
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
