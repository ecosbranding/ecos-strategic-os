import streamlit as st
import google.generativeai as genai

# --- CONFIGURACION DE PAGINA ---
st.set_page_config(
    page_title="ORCA Strategic OS",
    layout="wide"
)

# --- ESTILOS LIMPIOS Y PROFESIONALES ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .stButton>button {
        width: 100%;
        background: #007BFF;
        color: white;
        border-radius: 4px;
        padding: 10px;
        font-weight: bold;
        border: none;
    }
    .report-card {
        background-color: #161B22;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #30363D;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DE INTELIGENCIA (FORZADO DE VERSION ESTABLE) ---
def initialize_gemini(api_key):
    try:
        # Configuracion de la llave
        genai.configure(api_key=api_key)
        
        # FORZADO: Especificamos el modelo exacto sin prefijos de ruta
        # La libreria usara por defecto la version estable si no se indica lo contrario
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Error de configuracion: {e}")
        return None

def generate_global_plan(model, links, location, region_type):
    # Prompt optimizado para analisis mundial
    prompt = f"""
    Actua como consultor estrategico senior.
    Analiza los siguientes perfiles: {links}
    
    Contexto:
    - Ciudad/Pais: {location}
    - Mercado: {region_type}

    Genera un informe detallado con:
    1. Analisis del mercado local en {location}.
    2. Estrategia de ventas y conversion.
    3. Guia de estilo visual y colores (Paleta HEX).
    4. Plan de contenidos para 7 dias con horarios.
    5. Analisis de escalabilidad.

    Tono: Profesional y ejecutivo.
    """
    try:
        # Generacion de contenido
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Si vuelve a fallar, este mensaje nos dira exactamente que version esta usando
        return f"Error tecnico: {str(e)}"

# --- INTERFAZ ---
def main():
    st.title("ORCA Strategic OS")
    st.text("Consultoria Estrategica Global")

    with st.sidebar:
        st.header("Ajustes")
        
        # Validacion de llave desde Secrets
        api_key = st.secrets.get("GEMINI_API_KEY")
        
        if api_key:
            st.success("Sistema Conectado")
        else:
            api_key = st.text_input("Ingresa tu API Key", type="password")
            
        st.divider()
        
        location = st.text_input("Ubicacion", placeholder="Ej: Ecuador")
        region_type = st.selectbox("Segmento de Mercado", [
            "Mercado Emergente", 
            "Mercado Maduro", 
            "Mercado de Lujo",
            "Global"
        ])

    st.markdown("### Activos a Analizar")
    links_input = st.text_area("Pega los enlaces aqui:", height=100)

    if st.button("GENERAR ESTRATEGIA"):
        if not api_key:
            st.error("Error: No se encontro la GEMINI_API_KEY en los Secrets.")
        elif not links_input or not location:
            st.warning("Por favor ingresa la ubicacion y los enlaces.")
        else:
            with st.spinner("Procesando consultoria mundial..."):
                model = initialize_gemini(api_key)
                if model:
                    report = generate_global_plan(model, links_input, location, region_type)
                    
                    if "404" in report or "Error" in report:
                        st.error("Error de conexion con el servidor de Google.")
                        st.write(report)
                    else:
                        st.divider()
                        st.markdown(f"## Resultados: {location}")
                        st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                        st.download_button("Descargar Informe", report, file_name=f"Estrategia_{location}.md")

if __name__ == "__main__":
    main()
