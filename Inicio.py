import os
import streamlit as st
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# 1. Configuración de la página
st.set_page_config(
    page_title="Calculadora Mágica de Dígitos 🧮",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilos CSS Cyberpunk Neón (Barra Lateral y Fondo Completamente Oscuros)
st.markdown("""
    <style>
    /* Fondo general oscuro */
    .stApp {
        background-color: #1A1F2C !important;
        color: #FFFFFF !important;
    }
    #MainMenu, footer, header {visibility: hidden;}

    /* FORZAR BARRA LATERAL TOTALMENTE OSCURA */
    section[data-testid="stSidebar"] {
        background-color: #121722 !important;
        border-right: 2px solid #00F0FF !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #121722 !important;
    }

    /* Títulos y textos de la Barra Lateral en Azul Neón */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #00F0FF !important;
        font-weight: bold !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.6) !important;
    }

    /* Tarjetas de Métricas en la Barra Lateral */
    div[data-testid="stMetric"] {
        background-color: #1A2232 !important;
        border: 1px solid #00F0FF !important;
        border-radius: 8px !important;
        padding: 10px !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2) !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #90CDF4 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #00FF66 !important;
        font-weight: bold !important;
    }

    /* Título principal con resplandor neón */
    .neon-title {
        font-size: 2.3rem;
        font-weight: 900;
        text-align: center;
        color: #00F0FF;
        text-shadow: 0 0 10px #00F0FF, 0 0 20px #00F0FF;
        margin-bottom: 0.5rem;
    }

    /* Subtítulos y textos de los Pasos en Azul Neón */
    .cyan-sub-title {
        color: #00F0FF !important;
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.6) !important;
        margin-top: 1rem !important;
        margin-bottom: 0.8rem !important;
    }

    .step-box {
        background: #252D3D;
        border: 2px solid #00F0FF;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        margin-bottom: 1rem;
    }

    .result-box {
        background: linear-gradient(135deg, #0A2540 0%, #1A365D 100%);
        border: 3px solid #00FF66;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.4);
    }

    /* Marco del Canvas */
    iframe[title="streamlit_drawable_canvas.canvas"] {
        border: 3px solid #00F0FF !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3) !important;
    }

    /* Botones Neón */
    div.stButton > button {
        width: 100%;
        background: transparent !important;
        color: #00FF66 !important;
        border: 2px solid #00FF66 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2) !important;
    }

    div.stButton > button:hover {
        background-color: #00FF66 !important;
        color: #0A0E17 !important;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.8) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar el modelo MNIST
@st.cache_resource
def load_mnist_model():
    model_files = ['mnist_model.keras', 'mnist_model.h5']
    for model_path in model_files:
        if os.path.exists(model_path):
            try:
                return keras.models.load_model(model_path)
            except Exception:
                continue
    return None

model = load_mnist_model()

# 4. Inicializar variables de estado
if "num1" not in st.session_state:
    st.session_state.num1 = None
if "num2" not in st.session_state:
    st.session_state.num2 = None
if "step" not in st.session_state:
    st.session_state.step = 1

# Barra Lateral (Sidebar) Oscura
with st.sidebar:
    st.markdown('<div class="cyan-sub-title">⚙️ Estado de la App</div>', unsafe_allow_html=True)
    
    if model:
        st.success("✅ Modelo MNIST Conectado")
    else:
        st.error("❌ Sube `mnist_model.keras` a la raíz de tu proyecto")

    st.markdown("---")
    st.markdown('<div class="cyan-sub-title">🧮 Números Guardados:</div>', unsafe_allow_html=True)
    st.metric("Primer Número", st.session_state.num1 if st.session_state.num1 is not None else "—")
    st.metric("Segundo Número", st.session_state.num2 if st.session_state.num2 is not None else "—")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Calculadora"):
        st.session_state.num1 = None
        st.session_state.num2 = None
        st.session_state.step = 1
        st.rerun()

# Encabezado principal
st.markdown('<h1 class="neon-title">🧮 CALCULADORA MÁGICA INFANTIL ✍️</h1>', unsafe_allow_html=True)

# Espacio opcional para tu imagen fija desde GitHub
try:
    custom_image = Image.open('Calculadora_cool.jpg')
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(custom_image, use_container_width=True)
except Exception:
    pass

# Descripción de la app
st.markdown("""
    <div class="step-box">
        <p style="margin:0; font-size:1.05rem;">
            ¡Bienvenido a la Calculadora Mágica! Dibuja un número en el tablero, la Inteligencia Artificial lo reconocerá y podrás hacer sumas, restas, multiplicaciones o divisiones.
        </p>
    </div>
""", unsafe_allow_html=True)

if model is None:
    st.warning("⚠️ No se ha encontrado el modelo `mnist_model.keras` en el repositorio.")
    st.stop()

# --- PASO 1 & 2: DIBUJO DE NÚMEROS ---
st.markdown(
    f'<div class="cyan-sub-title">✏️ Paso {st.session_state.step}: Dibuja el {"PRIMER" if st.session_state.step == 1 else "SEGUNDO"} número</div>', 
    unsafe_allow_html=True
)

col_canvas, col_ctrl = st.columns([2, 1])

with col_canvas:
    canvas_result = st_canvas(
        fill_color="black",
        stroke_width=22,
        stroke_color="white",
        background_color="black",
        width=350,
        height=350,
        drawing_mode="freedraw",
        key=f"canvas_step_{st.session_state.step}",
    )

with col_ctrl:
    st.markdown('<div class="cyan-sub-title">🕹️ Acciones</div>', unsafe_allow_html=True)
    
    if st.button("🔍 **Detectar Número**", type="primary"):
        if canvas_result.image_data is not None and np.max(canvas_result.image_data) > 0:
            image = Image.fromarray(canvas_result.image_data.astype("uint8")).convert("L")
            image_resized = image.resize((28, 28), Image.Resampling.LANCZOS)
            img_array = np.array(image_resized) / 255.0
            img_array = img_array.reshape(1, 28, 28, 1)

            prediction = model.predict(img_array, verbose=0)
            detected_digit = int(np.argmax(prediction))
            confidence = float(np.max(prediction) * 100)

            if st.session_state.step == 1:
                st.session_state.num1 = detected_digit
                st.success(f"🎉 ¡Primer número detectado: **{detected_digit}**! ({confidence:.1f}% confianza)")
                st.session_state.step = 2
                st.rerun()
            else:
                st.session_state.num2 = detected_digit
                st.success(f"🎉 ¡Segundo número detectado: **{detected_digit}**! ({confidence:.1f}% confianza)")
                st.rerun()
        else:
            st.warning("⚠️ Dibuja un número en el recuadro negro antes de detectar.")

    if st.button("🗑️ Borrar Dibujo"):
        st.rerun()

# --- PASO 3: OPERACIÓN Y RESULTADO ---
if st.session_state.num1 is not None and st.session_state.num2 is not None:
    st.markdown("---")
    st.markdown('<div class="cyan-sub-title">➕ Elije la operación para resolver:</div>', unsafe_allow_html=True)

    col_op1, col_op2, col_op3, col_op4 = st.columns(4)

    operation = None
    if col_op1.button("➕ SUMAR"):
        operation = "+"
    if col_op2.button("➖ RESTAR"):
        operation = "-"
    if col_op3.button("✖️ MULTIPLICAR"):
        operation = "*"
    if col_op4.button("➗ DIVIDIR"):
        operation = "/"

    if operation:
        n1 = st.session_state.num1
        n2 = st.session_state.num2

        if operation == "+":
            res = n1 + n2
            symbol = "+"
        elif operation == "-":
            res = n1 - n2
            symbol = "-"
        elif operation == "*":
            res = n1 * n2
            symbol = "×"
        elif operation == "/":
            res = round(n1 / n2, 2) if n2 != 0 else "Error (No se divide por 0)"
            symbol = "÷"

        st.markdown(f"""
            <div class="result-box">
                <h2 style="color: #00F0FF; margin:0;">🎯 ¡RESULTADO FINAL!</h2>
                <h1 style="color: #00FF66; font-size: 3.5rem; margin:10px 0;">{n1} {symbol} {n2} = {res}</h1>
            </div>
        """, unsafe_allow_html=True)
