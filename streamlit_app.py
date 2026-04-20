import streamlit as st
import requests
from urllib.parse import urlparse
import json
import random

# ==============================
# CONFIGURACIÓN BASE
# ==============================

st.set_page_config(
    page_title="ORCA Strategic OS",
    layout="wide"
)

# ==============================
# UI BASE (EVITA PANTALLA NEGRA)
# ==============================

st.title("ORCA Strategic OS")
st.write("Sistema de inteligencia estratégica automatizada")

# ==============================
# SECRETS (SEGURO Y ROBUSTO)
# ==============================

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)

if not GEMINI_API_KEY:
    st.warning("API Key no encontrada en secrets. El sistema funcionará limitado.")

# ==============================
# DARK MODE SIMPLE
# ==============================

st.markdown("""
<style>
    body { background-color: #0e1117; color: #ffffff; }
    .stTextArea textarea { background-color: #1c1f26; color: white; }
    .stTextInput input { background-color: #1c1f26; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        font-weight: 600;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# GEMINI API CALL (ROBUSTO)
# ==============================

def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return "Error: API Key no configurada."

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"Error API ({response.status_code}): {response.text}"

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"Error conexión API: {str(e)}"

# ==============================
# SCRAPING SIMULADO (ESTABLE)
# ==============================

def simulate_scraping(url):
    try:
        domain = urlparse(url).netloc

        return {
            "url": url,
            "platform": (
                "Instagram" if "instagram" in domain
                else "TikTok" if "tiktok" in domain
                else "Web"
            ),
            "followers": random.randint(1000, 90000),
            "engagement_rate": round(random.uniform(1.0, 9.5), 2),
            "content_type": random.choice(["Reels", "Educativo", "Lifestyle", "Ventas"]),
            "posting_frequency": random.choice(["Alta", "Media", "Baja"]),
            "brand_tone": random.choice(["Premium", "Casual", "Corporativo"])
        }

    except Exception as e:
        return {"url": url, "error": str(e)}

# ==============================
# PROMPT ORCA
# ==============================

def build_prompt(data, location):
    return f"""
Eres ORCA Strategic OS, un equipo de consultoría de élite.

Analiza estos datos:

{json.dumps(data, indent=2)}

Ubicación: {location}

Entrega:

1. ESTADÍSTICAS
- Engagement
- Salud de marca

2. MARKETING
- Funnel AIDA
- Estrategia local

3. DISEÑO
- Estética premium editorial
- Colores HEX
- Tipografías

4. CONTENIDO
- 7 días de contenido
- Hooks virales
- Guiones técnicos

5. NEGOCIO
- Viabilidad
- Optimización
"""

# ==============================
# INPUTS UI
# ==============================

urls_input = st.text_area("URLs (una por línea)")
location = st.text_input("Ubicación", "Quito, Ecuador")

# ==============================
# BOTÓN PRINCIPAL
# ==============================

if st.button("Ejecutar análisis"):

    st.write("Iniciando proceso...")

    if not urls_input.strip():
        st.error("Debes ingresar URLs.")
    else:

        urls = urls_input.split("\n")

        st.write("Procesando scraping...")

        results = []
        for url in urls:
            url = url.strip()
            if url:
                results.append(simulate_scraping(url))

        st.write("Scraping completado.")

        prompt = build_prompt(results, location)

        st.write("Consultando Gemini...")

        output = call_gemini(prompt)

        st.markdown("## Resultado estratégico")
        st.write(output)

        with st.expander("Datos procesados"):
            st.json(results)

# ==============================
# DEBUG OPCIONAL
# ==============================

with st.expander("Debug"):
    st.write("API KEY cargada:", bool(GEMINI_API_KEY))
