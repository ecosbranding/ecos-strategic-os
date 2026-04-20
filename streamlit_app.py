import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="ORCA Strategic OS | Global Edition",
    page_icon="🐋",
    layout="wide"
)

# --- ESTILOS PROFESIONALES ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #007BFF 0%, #00d4ff 100%);
        color: white;
        border-radius: 10px;
        padding: 15px;
        font-weight: bold;
        border: none;
    }
    .report-card {
        background-color: #161B22;
        padding: 30px;
        border-radius: 15px;
        border-top: 4px solid #007BFF;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE INTELIGENCIA ---
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        # Usamos 1.5 Flash por su velocidad y capacidad de análisis global
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# --- GENERADOR DE CONSULTORÍA GLOBAL ---
def generate_global_plan(model, links, location, region_type):
    prompt = f"""
    Eres una firma de consultoría de élite de Silicon Valley. 
    Analiza estos activos digitales: {links}
    
    CONTEXTO GEOGRÁFICO:
    - Ubicación Específica: {location}
    - Tipo de Mercado: {region_type}

    TU MISIÓN: Generar un 'Strategic Roadmap 360°' adaptado cultural y económicamente a esta zona.
    
    ESTRUCTURA DEL REPORTE:
    1. ANALÍTICA DE MERCADO LOCAL: Comportamiento del consumidor en {location} y competencia detectada.
    2. FUNNEL DE VENTAS (AIDA): Adaptado a la moneda y hábitos de compra de la región.
    3. ART DIRECTION (Luxury Editorial): Estética visual, paleta HEX y psicología del color para ese mercado.
    4. CONTENT ENGINE: Calendario de 7 días con Hooks, guiones técnicos y mejores horas de publicación en {location}.
    5. OPERACIONES & ROI: Análisis de viabilidad y escalabilidad global.

    Instrucción de Calidad: Responde con autoridad técnica, tono ejecutivo y soluciones accionables.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en el motor estratégico: {str(e)}"

# --- INTERFAZ ---
def main():
    st.title("🐋 ORCA Strategic OS")
    st.subheader("Global Automated Consulting Suite")

    with st.sidebar:
        st.header("🌎 Configuración Global")
        
        # Conexión Segura con Secrets
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.success("IA Conectada exitosamente")
        else:
            api_key = st.text_input("API Key", type="password")
            
        st.divider()
        
        # SELECTOR MUNDIAL
        location = st.text_input("📍 Ciudad / País", placeholder="Ej: Madrid, España")
        region_type = st.selectbox("📊 Tipo de Mercado", [
            "Mercado Emergente (Latam/África)", 
            "Mercado Maduro (EE.UU./Europa)", 
            "Mercado de Lujo (Dubai/Singapur)",
            "Global (Sin frontera específica)"
        ])

    # ENTRADA DE DATOS
    st.markdown("### 🔗 Activos a Analizar")
    links_input = st.text_area("Pega los links (Instagram, TikTok, Web):", height=150)

    if st.button("DESPLEGAR CONSULTORÍA MUNDIAL"):
        if api_key and links_input and location:
            with st.spinner(f"Analizando mercado en {location}..."):
                model = initialize_gemini(api_key)
                if model:
                    report = generate_global_plan(model, links_input, location, region_type)
                    st.divider()
                    st.markdown(f"## 🏁 Estrategia para {location}")
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                    
                    st.download_button("Descargar Reporte", report, file_name=f"ORCA_{location}.md")
        else:
            st.error("Por favor completa: API Key (en Secrets), Ubicación y Links.")

if __name__ == "__main__":
    main()
