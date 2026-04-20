import streamlit as st
import google.generativeai as genai

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
        border-radius: 5px;
        padding: 12px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #0056b3;
    }
    .report-card {
        background-color: #161B22;
        padding: 30px;
        border-radius: 10px;
        border: 1px solid #30363D;
        line-height: 1.6;
        color: #E6EDF3;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DE INTELIGENCIA (VERSION ANTI-404) ---
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        # Usamos la cadena simple del modelo, que es la mas estable en Streamlit Cloud
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Error de configuracion: {e}")
        return None

def generate_global_plan(model, links, location, region_type):
    prompt = f"""
    Actua como una firma de consultoria estrategica.
    Analiza los activos digitales: {links}
    
    CONTEXTO:
    - Ubicacion: {location}
    - Mercado: {region_type}

    MISION: Generar un Roadmap Estrategico adaptado a esta zona.
    
    ESTRUCTURA DEL REPORTE:
    1. ANALITICA DE MERCADO: Consumidor y competencia en {location}.
    2. EMBUDO DE VENTAS: Adaptado a habitos locales.
    3. DIRECCION DE ARTE: Estetica, paleta HEX y psicologia del color.
    4. PLAN DE CONTENIDO: Calendario de 7 dias con guiones y horarios.
    5. VIABILIDAD: Analisis de escalabilidad.

    Tono: Ejecutivo y profesional.
    """
    try:
        # Forzamos la generacion de contenido simple
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Mensaje de error detallado para diagnostico
        return f"Error en la generacion: {str(e)}"

# --- INTERFAZ ---
def main():
    st.title("ORCA Strategic OS")
    st.subheader("Consultoria Estrategica Automatizada")

    with st.sidebar:
        st.header("Configuracion")
        
        # Prioridad a Secrets de Streamlit
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("Sistema Conectado")
        else:
            api_key = st.text_input("API Key", type="password")
            
        st.divider()
        
        location = st.text_input("Ciudad o Pais", placeholder="Ej: Ecuador")
        region_type = st.selectbox("Tipo de Mercado", [
            "Mercado Emergente", 
            "Mercado Maduro", 
            "Mercado de Lujo",
            "Global"
        ])

    st.markdown("### Enlaces de Referencia")
    links_input = st.text_area("Pega los links (Instagram, TikTok, Web):", height=150)

    if st.button("GENERAR CONSULTORIA ESTRATEGICA"):
        if not api_key:
            st.error("Falta la API Key en la configuracion.")
        elif not links_input or not location:
            st.warning("Por favor rellena la ubicacion y los enlaces.")
        else:
            with st.spinner("Analizando datos y generando estrategia..."):
                model = initialize_gemini(api_key)
                if model:
                    report = generate_global_plan(model, links_input, location, region_type)
                    
                    if "Error" in report:
                        st.error(report)
                    else:
                        st.divider()
                        st.markdown(f"## Analisis Estrategico: {location}")
                        st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                        st.download_button("Descargar Reporte", report, file_name=f"Estrategia_{location}.md")

if __name__ == "__main__":
    main()
