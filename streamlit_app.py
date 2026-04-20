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
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DE INTELIGENCIA ---
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        # Se utiliza la ruta completa del modelo para máxima compatibilidad
        return genai.GenerativeModel(model_name='models/gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error de conexion: {e}")
        return None

def generate_global_plan(model, links, location, region_type):
    prompt = f"""
    Actua como una firma de consultoria estrategica de alto nivel.
    Analiza los siguientes activos digitales: {links}
    
    CONTEXTO GEOGRAFICO:
    - Ubicacion: {location}
    - Tipo de Mercado: {region_type}

    MISION: Generar un Strategic Roadmap 360 adaptado cultural y economicamente a esta zona.
    
    ESTRUCTURA DEL REPORTE:
    1. ANALITICA DE MERCADO: Comportamiento del consumidor y competencia en {location}.
    2. EMBUDO DE VENTAS (AIDA): Adaptado a la moneda y habitos de compra locales.
    3. DIRECCION DE ARTE: Estetica visual (Luxury Editorial), paleta HEX y psicologia del color.
    4. PLAN DE CONTENIDO: Calendario de 7 dias con Hooks, guiones y mejores horas de publicacion.
    5. VIABILIDAD Y ROI: Analisis de escalabilidad.

    Tono: Ejecutivo, directo y altamente profesional.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en el motor estrategico: {str(e)}"

# --- INTERFAZ ---
def main():
    st.title("ORCA Strategic OS")
    st.subheader("Consultoria Estrategica Automatizada")

    with st.sidebar:
        st.header("Configuracion")
        
        # Uso de Secrets para la API Key
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("Sistema Conectado")
        else:
            api_key = st.text_input("API Key", type="password")
            
        st.divider()
        
        location = st.text_input("Ciudad o Pais", placeholder="Ej: Madrid, España")
        region_type = st.selectbox("Tipo de Mercado", [
            "Mercado Emergente", 
            "Mercado Maduro", 
            "Mercado de Lujo",
            "Global"
        ])

    st.markdown("### Enlaces de Referencia")
    links_input = st.text_area("Ingresa los links de redes sociales o web:", height=150)

    if st.button("GENERAR CONSULTORIA ESTRATEGICA"):
        if api_key and links_input and location:
            with st.spinner(f"Procesando analisis para {location}..."):
                model = initialize_gemini(api_key)
                if model:
                    report = generate_global_plan(model, links_input, location, region_type)
                    st.divider()
                    st.markdown(f"## Estrategia: {location}")
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                    
                    st.download_button("Exportar Reporte", report, file_name=f"Estrategia_{location}.md")
        else:
            st.warning("Asegurate de haber configurado la ubicacion y los enlaces correctamente.")

if __name__ == "__main__":
    main()
