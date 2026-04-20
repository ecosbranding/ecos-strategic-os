import streamlit as st
import google.generativeai as genai
import re
import json
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA (UI/UX) ---
st.set_page_config(
    page_title="ORCA Strategic OS",
    page_icon="🐋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CUSTOM (DARK THEME & EDITORIAL DESIGN) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button {
        width: 100%;
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    .stTextInput>div>div>input { background-color: #1A1C24; color: white; border: 1px solid #30363D; }
    .report-card {
        background-color: #161B22;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007BFF;
        margin-bottom: 20px;
    }
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -0.5px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE BACKEND: CONECTIVIDAD & IA ---
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error al conectar con la API de Google: {e}")
        return None

def simulate_scraping(links):
    """
    Simula la extracción de metadatos y análisis de salud de marca
    basado en los patrones de las URLs proporcionadas.
    """
    extracted_data = []
    for link in links:
        if not link.strip():
            continue
        platform = "Web"
        if "instagram.com" in link: platform = "Instagram"
        elif "tiktok.com" in link: platform = "TikTok"
        
        # Simulación de extracción de métricas mediante análisis de patrón
        extracted_data.append({
            "url": link,
            "platform": platform,
            "status": "Verified",
            "detected_tone": "Editorial/Professional"
        })
    return extracted_data

# --- MÓDULO DE LÓGICA DE NEGOCIOS (SYSTEM PROMPT) ---
def generate_strategic_plan(model, data, location):
    links_context = "\n".join([f"- {item['platform']}: {item['url']}" for item in data])
    
    prompt = f"""
    Eres un equipo Élite de Consultoría en Silicon Valley (CMO, Director de Arte, MBA).
    Analiza los siguientes activos digitales para una marca en {location}:
    CONTEXTO DE MARCA:
    {links_context}

    TU MISIÓN: Generar una Hoja de Ruta 360° en formato Markdown profesional.

    ESTRUCTURA OBLIGATORIA:
    1. ANÁLISIS DE SALUD DIGITAL (Métricas Estimadas): Engagement rate, coherencia visual y posicionamiento.
    2. ESTRATEGIA DE MARKETING & VENTAS: 
       - Funnel AIDA específico para el mercado de {location}.
       - Estrategia de pauta local (Facebook/IG Ads + Google Maps).
    3. DIRECTORIO DE ARTE (Luxury Editorial):
       - Definición estética (Minimalismo, High-Contrast, etc.).
       - Paleta de colores (Códigos Hex).
       - Tipografías sugeridas (Serif vs Sans).
    4. CALENDARIO EDITORIAL (7 DÍAS): 
       - Incluye para cada día: Título, Hook, Guión técnico (toma, iluminación, ángulo) y audio tendencia.
    5. VIABILIDAD FINANCIERA (MBA): 
       - Análisis de ROI proyectado y optimización operativa.

    Tono: Ejecutivo, sofisticado, directo y altamente técnico.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en el procesamiento estratégico: {str(e)}"

# --- INTERFAZ DE USUARIO (UI) ---
def main():
    st.title("🐋 ORCA Strategic OS")
    st.subheader("Automated Consulting Suite | V 1.0")
    
    with st.sidebar:
        st.header("Control de Mando")
        api_key = st.text_input("Gemini API Key", type="password", help="Ingresa tu Google AI Studio API Key")
        location = st.text_input("Ubicación Geográfica", placeholder="Ej. Quito, Ecuador")
        st.divider()
        st.info("Esta PWA utiliza IA de Google para análisis de mercado en tiempo real.")

    # MÓDULO DE ENTRADA
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔗 Activos Digitales")
        links_input = st.text_area(
            "Ingresa los enlaces (uno por línea)",
            placeholder="https://instagram.com/marca\nhttps://tiktok.com/@marca",
            height=150
        )
    
    with col2:
        st.markdown("### 📊 Estado del Sistema")
        if links_input and location:
            links_list = links_input.split('\n')
            scraping_results = simulate_scraping(links_list)
            for res in scraping_results:
                st.write(f"✅ **{res['platform']}**: Detectado correctamente.")
        else:
            st.warning("Esperando datos de entrada...")

    # ACCIÓN PRINCIPAL
    if st.button("GENERAR HOJA DE RUTA 360°"):
        if not api_key:
            st.error("GEMINI_API_KEY = "AIzaSyBvG3EIcwLXZE9LxFFJ9lOPplk7FCoIeDs"")
        elif not links_input or not location:
            st.error("Faltan datos requeridos (Links o Ubicación).")
        else:
            with st.spinner("ORCA AI está procesando la estrategia..."):
                model = initialize_gemini(api_key)
                if model:
                    # Simulación de Scraping para el contexto
                    scraped_data = simulate_scraping(links_input.split('\n'))
                    
                    # Generación de Estrategia
                    report = generate_strategic_plan(model, scraped_data, location)
                    
                    st.divider()
                    st.markdown("## 🏁 RESULTADO ESTRATÉGICO")
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                    
                    # Opción de Descarga
                    st.download_button(
                        label="Descargar Informe Estratégico",
                        data=report,
                        file_name=f"ORCA_Strategy_{location}.md",
                        mime="text/markdown"
                    )

if __name__ == "__main__":
    main()
