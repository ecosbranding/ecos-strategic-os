import streamlit as st
import requests
import json

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="ORCA Strategic OS",
    layout="wide"
)

# --- ESTILOS LIMPIOS ---
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

# --- MOTOR DE INTELIGENCIA (CONEXION DIRECTA API V1) ---
def call_gemini_api(api_key, prompt):
    # Forzamos la version 1 estable directamente en la URL
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
            return f"Error de servidor ({response.status_code}): {result.get('error', {}).get('message', 'Error desconocido')}"
    except Exception as e:
        return f"Error de conexion: {str(e)}"

# --- INTERFAZ ---
def main():
    st.title("ORCA Strategic OS")
    st.text("Plataforma de Consultoria Estrategica")

    with st.sidebar:
        st.header("Configuracion")
        
        # Obtener API KEY de Secrets
        api_key = st.secrets.get("GEMINI_API_KEY")
        
        if api_key:
            st.success("Conexion Segura")
        else:
            api_key = st.text_input("Ingresa API Key manualmente", type="password")
            
        st.divider()
        location = st.text_input("Ubicacion del Mercado", placeholder="Ej: Ecuador")
        market_type = st.selectbox("Tipo de Mercado", ["Emergente", "Maduro", "Lujo", "Global"])

    st.markdown("### Enlaces para Analisis")
    links = st.text_area("Pega los links (IG, TikTok, Web):", height=120)

    if st.button("EJECUTAR ESTRATEGIA"):
        if not api_key:
            st.error("Falta la GEMINI_API_KEY en los ajustes.")
        elif not links or not location:
            st.warning("Completa la ubicacion y los enlaces.")
        else:
            with st.spinner(f"Analizando mercado en {location}..."):
                # Construccion del Prompt
                full_prompt = f"""
                Actua como consultor senior de marketing. Analiza: {links}
                Zona: {location}. Mercado: {market_type}.
                Genera:
                1. Analisis de audiencia local.
                2. Estrategia de conversion.
                3. Guia visual (HEX).
                4. Plan de contenido 7 dias.
                Tono profesional.
                """
                
                report = call_gemini_api(api_key, full_prompt)
                
                if "Error" in report:
                    st.error(report)
                else:
                    st.divider()
                    st.markdown(f"## Estrategia para {location}")
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                    st.download_button("Descargar Estrategia", report, file_name=f"ORCA_{location}.txt")

if __name__ == "__main__":
    main()
