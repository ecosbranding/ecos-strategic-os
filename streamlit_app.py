import streamlit as st
import google.generativeai as genai
import re
import json
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA (ESTÁNDAR SILICON VALLEY) ---
st.set_page_config(
    page_title="ORCA Strategic OS",
    page_icon="🐋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CUSTOM (DARK THEME & LUXURY EDITORIAL) ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button {
        width: 100%;
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #0056b3; border: 1px solid #007BFF; }
    .report-card {
        background-color: #161B22;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #007BFF;
        margin-bottom: 25px;
        line-height: 1.6;
    }
    .success-text { color: #28a745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGENCIA ARTIFICIAL ---
def initialize_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def simulate_scraping(links):
    """Simula la extracción de metadatos de los links ingresados."""
    extracted_data = []
    for link in links:
        link = link.strip()
        if not link: continue
        platform = "Web/General"
        if "instagram.com" in link: platform = "Instagram"
        elif "tiktok.com" in link: platform = "TikTok"
        elif "facebook.com" in link: platform = "Facebook"
        
        extracted_data.append({
            "url": link,
            "platform": platform,
            "status": "Análisis Listo"
        })
    return extracted_data

# --- LÓGICA DE NEGOCIOS (PROMPT ESTRATÉGICO) ---
def generate_strategic_plan(model, data, location):
    links_context = "\n".join([f"- {item['platform']}: {item['url']}" for item in data])
    
    prompt = f"""
    Actúa como un Equipo de Élite (CMO, Analista de Datos, Director de Arte y MBA).
    Genera una consultoría completa para una marca con presencia en: {location}.
    
    ACTIVOS DIGITALES DETECTADOS:
    {links_context}

    REQUERIMIENTOS TÉCNICOS DEL REPORTE:
    1. ESTRATEGIA 360°: Análisis de engagement y salud de marca.
    2. MARKETING & VENTAS: Embudo AIDA y plan de pauta local en {location}.
    3. DISEÑO EDITORIAL: Estética 'Luxury Editorial', paleta de colores HEX y tipografía.
    4. CONTENIDO: Calendario de 7 días con guiones (hooks, tomas, iluminación).
    5. ADMINISTRACIÓN: Análisis de viabilidad operativa y ROI proyectado.

    Tono: Profesional, sofisticado y ejecutable. No resumas.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error en el motor estratégico: {str(e)}"

# --- INTERFAZ DE USUARIO ---
def main():
    st.title("🐋 ORCA Strategic OS")
    st.subheader("Automated Consulting & Intelligence Suite")
    
    # CONTROL DE MANDO (SIDEBAR)
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # INTEGRACIÓN CON SECRETS
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.markdown('<p class="success-text">✅ Sistema de IA Conectado</p>', unsafe_allow_html=True)
        else:
            api_key = st.text_input("Ingresa Gemini API Key", type="password")
            st.warning("⚠️ Clave no detectada en Secrets. Ingresa una manualmente.")
            
        st.divider()
        location = st.text_input("📍 Ubicación del Mercado", placeholder="Ej: Quito, Ecuador")
        st.info("Configurado para el mercado local de " + (location if location else "la región"))

    # ÁREA DE TRABAJO
    col_input, col_status = st.columns([1.2, 0.8])
    
    with col_input:
        st.markdown("### 🔗 Enlaces de Referencia")
        links_text = st.text_area(
            "Pega URLs de IG, TikTok o Web (una por línea):",
            placeholder="https://www.instagram.com/orcastudios...",
            height=180
        )
    
    with col_status:
        st.markdown("### 📡 Scanner de Metadatos")
        if links_text:
            links_list = links_text.split('\n')
            results = simulate_scraping(links_list)
            for r in results:
                st.write(f"🔹 **{r['platform']}**: {r['status']}")
        else:
            st.write("Esperando activos digitales...")

    # ACCIÓN ESTRATÉGICA
    if st.button("DESPLEGAR CONSULTORÍA 360°"):
        if not api_key:
            st.error("Error: Se requiere una API Key válida para procesar.")
        elif not links_text or not location:
            st.error("Error: Debes ingresar links y una ubicación geográfica.")
        else:
            with st.spinner("El equipo de Silicon Valley está analizando tu marca..."):
                model = initialize_gemini(api_key)
                if model:
                    scraped_data = simulate_scraping(links_text.split('\n'))
                    report = generate_strategic_plan(model, scraped_data, location)
                    
                    st.divider()
                    st.markdown("## 📊 HOJA DE RUTA ESTRATÉGICA")
                    st.markdown(f'<div class="report-card">{report}</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📄 Exportar Estrategia (PDF/MD)",
                        data=report,
                        file_name=f"ORCA_Estrategia_{location}.md",
                        mime="text/markdown"
                    )

if __name__ == "__main__":
    main()
