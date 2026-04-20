import streamlit as st
import requests
import json

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="ORCA Strategic OS",
    layout="wide"
)

# --- ESTILOS PROFESIONALES LIMPIOS ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        width: 100%;
        background: #007BFF;
        color: white;
        border-radius: 4px;
        padding: 12px;
        font-weight: bold;
        border: none;
    }
    .report-card {
        background-color: #161B22;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #30363D;
        color: #E6EDF3;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGENCIA (CONEXION DIRECTA V1) ---
def call_gemini_api(api_key, prompt):
    # Forzamos la version estable v1 para evitar el error 404 v1beta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        if response.status_code == 200:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            error_msg = result.get('error', {}).get('message', 'Error desconocido')
            return f"Error de servidor ({response.status_code}): {error_msg}"
    except Exception as e:
        return f"Error de conexion: {str(e)}"

# --- INTERFAZ DE USUARIO ---
def main():
    st.title("ORCA Strategic OS")
    st.text("Consultoria Estrategica Global")

    # API Key integrada directamente
    API_KEY = "AIzaSyBvG3EIcwLXZE9LxFFJ9lOPplk7FCoIeDs"

    with st.sidebar:
        st.header("Configuracion")
        st.success("Sistema Conectado")
        st.divider()
        location = st.text_input("Ubicacion del Mercado", placeholder="Ej: Ecuador")
        market_type = st.selectbox("Tipo de Mercado", ["Emergente", "Maduro", "Lujo", "Global"])

    st.markdown("### Activos Digitales")
    links = st.text_area("Pega los links (Instagram, TikTok, Web):", height=120)

    if st.button("EJECUTAR CONSULTORIA"):
        if not links or not location:
            st.warning("Por favor, ingresa la ubicacion y los enlaces de referencia.")
        else:
            with st.spinner(f"Analizando mercado en {location}..."):
                # Estructura del Prompt para el modelo
                full_prompt = f"""
                Actua como consultor senior de marketing y estrategia digital.
                Analiza los siguientes activos: {links}
                Contexto Geografico: {location}
                Tipo de Mercado: {market_type}

                Genera un informe con los siguientes puntos:
                1. Analisis del consumidor local en {location}.
                2. Estrategia de conversion y ventas.
                3. Identidad visual sugerida y paleta de colores HEX.
                4. Calendario de contenido para 7 dias.
                5. Proyeccion de escalabilidad.

                Tono: Profesional, directo y ejecutivo.
                """
                
                report = call_gemini_api(API_KEY, full_prompt)
                
                if "Error" in report:
                    st.error(report)
                    st.info("Nota: Verifica que la Facturacion este activa en Google Cloud si el error persiste.")
                else:
                    st.divider()
                    st.markdown(f"## Estrategia Final: {location}")
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                    st.download_button("Exportar Reporte", report, file_name=f"Estrategia_ORCA_{location}.md")

if __name__ == "__main__":
    main()
