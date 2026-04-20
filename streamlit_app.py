import streamlit as st
import requests
from urllib.parse import urlparse
import json
import random

# ==============================
# CONFIGURACIÓN GENERAL
# ==============================

st.set_page_config(
    page_title="ORCA Strategic OS",
    layout="wide"
)

# ==============================
# DARK THEME
# ==============================

st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextArea textarea {
        background-color: #1c1f26;
        color: #ffffff;
    }
    .stTextInput input {
        background-color: #1c1f26;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# GEMINI API
# ==============================

def call_gemini(api_key, prompt):
    if not api_key:
        return "Error: API Key no proporcionada."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code != 200:
            return f"Error API ({response.status_code}): {response.text}"

        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.Timeout:
        return "Error: Timeout en la API."
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

# ==============================
# SCRAPING SIMULADO
# ==============================

def simulate_scraping(url):
    try:
        domain = urlparse(url).netloc

        return {
            "url": url,
            "platform": "Instagram" if "instagram" in domain else "TikTok" if "tiktok" in domain else "Web",
            "followers": random.randint(1000, 100000),
            "engagement_rate": round(random.uniform(1.0, 10.0), 2),
            "content_type": random.choice(["Reels", "Educativo", "Lifestyle", "Ventas"]),
            "posting_frequency": random.choice(["Alta", "Media", "Baja"]),
            "brand_tone": random.choice(["Premium", "Casual", "Corporativo"])
        }

    except Exception as e:
        return {"url": url, "error": str(e)}

# ==============================
# PROMPT ESTRATÉGICO
# ==============================

def build_prompt(data, location):
    return f"""
Eres un equipo élite de Silicon Valley compuesto por:
Senior Full-Stack Developer, CMO, Director de Arte Editorial, Data Analyst y MBA.

Analiza estos datos:

{json.dumps(data, indent=2)}

Ubicación objetivo: {location}

Entrega:

1. ESTADÍSTICAS
Diagnóstico de engagement
Salud de marca
Benchmark implícito

2. MARKETING Y VENTAS
Funnel AIDA completo
Estrategia de pauta local

3. DISEÑO GRÁFICO
Estética Luxury Editorial
Paleta de colores HEX
Tipografías

4. CONTENIDO
Calendario de 7 días
Hooks virales
Guiones técnicos

5. ADMINISTRACIÓN
Viabilidad del negocio
Optimización operativa
Cuellos de botella
"""

# ==============================
# UI
# ==============================

st.title("ORCA Strategic OS")
st.subheader("Sistema de inteligencia estratégica automatizada")

# API key precargada en el campo (puedes cambiarla manualmente si quieres)
api_key_input = st.text_input(
    "API Key de Gemini",
    value="gen-lang-client-0393749840",
    type="password"
)

urls_input = st.text_area("URLs (una por línea)")
location = st.text_input("Ubicación objetivo", "Quito, Ecuador")

if st.button("Ejecutar análisis"):

    if not api_key_input:
        st.error("Debes ingresar tu API Key.")
    elif not urls_input.strip():
        st.error("Debes ingresar al menos una URL.")
    else:
        urls = urls_input.split("\n")

        st.info("Ejecutando scraping...")

        results = []
        for url in urls:
            url = url.strip()
            if url:
                results.append(simulate_scraping(url))

        st.success("Scraping completado.")

        prompt = build_prompt(results, location)

        st.info("Procesando análisis estratégico...")

        with st.spinner("Generando resultado..."):
            output = call_gemini(api_key_input, prompt)

        st.success("Análisis completado.")

        st.markdown("## Resultado estratégico")
        st.markdown(output)

        with st.expander("Datos procesados"):
            st.json(results)
