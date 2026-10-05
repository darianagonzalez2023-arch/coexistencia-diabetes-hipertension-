import streamlit as st
import pandas as pd
import joblib
from pathlib import Path 

# Cargar el modelo
ruta_modelo = Path(__file__).parent / "modelo_coexistencia.pkl"
modelo = joblib.load(ruta_modelo)

# Configuración de la página
st.set_page_config(
    page_title="Coexistencia DM + HTA",
    page_icon="❤️",
    layout="centered"
)

# Título
st.title("🩺❤️ Evaluación de coexistencia DM + HTA")

st.write(
    "Agregue los datos de la persona para obtener una estimación "
    "del nivel de coexistencia de diabetes mellitus e hipertensión arterial."
)

st.info(
    "Esta es una herramienta que corresponde a un modelo académico de predicción "
    "basado en los datos analizados de Bucaramanga."
)

# Datos de entrada
st.subheader("Datos de la persona")

sexo_mostrado = st.selectbox(
    "Sexo",
    ["♀️FEMENINO", "♂️MASCULINO"]
)
sexos = {"♀️FEMENINO" : "FEMENINO", "♂️MASCULINO" : "MASCULINO"}
sexo = sexos[sexo_mostrado]
edad = st.number_input("Edad (años)",
                       min_value=0,
                       max_value=120,
                       value=30,
                       step=1
                       )

def obtener_ciclo_de_vida(edad) : 
    if 0 <= edad <= 6: return "PRIMERA INFANCIA" 
    elif 7 <= edad <= 11: return "INFANCIA" 
    elif 12 <= edad <= 17: return "ADOLESCENCIA" 
    elif 18 <= edad <= 28: return "JOVENES" 
    elif 29 <= edad <= 59: return "ADULTEZ" 
    else: 
        return "PERSONA MAYOR" 
    
ciclo = obtener_ciclo_de_vida(edad)
st.caption(f"Grupo etareo identificado: {ciclo}")

# Botón
if st.button("🔍 Estimar el nivel de coexistencia"):

    # Crear los datos de la persona
    persona = pd.DataFrame({
        "CICLO_DE_VIDA": [ciclo],
        "Sexo": [sexo]
    })

    # Obtener probabilidad
    probabilidad = modelo.predict_proba(persona)[0, 1]

    porcentaje = probabilidad * 100

    # Clasificación
    if porcentaje >= 20:
        nivel = "ALTO"
        prioridad = "ALTA"
    elif porcentaje > 15:
        nivel = "MEDIO-ALTO"
        prioridad = "ALTA"
    elif porcentaje >= 10:
        nivel = "MEDIO"
        prioridad = "MEDIA"
    else:
        nivel = "BAJO"
        prioridad = "BAJA"

    # Mostrar resultado
    st.subheader("Resultado")

    st.metric(
        "📊Probabilidad estimada de coexistencia",
        f"{porcentaje:.2f}%"
    )

    if nivel == "ALTO":
        st.error(f"🔴 NIVEL DE COEXISTENCIA: {nivel}")

    elif nivel == "MEDIO-ALTO":
        st.warning(f"🟠 NIVEL DE COEXISTENCIA: {nivel}")

    elif nivel == "MEDIO":
        st.warning(f"🟡 NIVEL DE COEXISTENCIA: {nivel}")

    else:
        st.success(f"🟢 NIVEL DE COEXISTENCIA: {nivel}")

    st.write(f"**Prioridad:** {prioridad}")

    st.progress(min(probabilidad, 1.0))

    st.caption(
        "Nota: Este porcentaje corresponde a una estimación del modelo y "
        "no debe ser tomado como un diagnóstico clínico."
    )

    #Diseño 

    st.markdown("""<style>.stApp{background-color: #E3F2FD;}
    h1{color: #1B4965;}
    button{background-color: #1B4965; 
    color: azul claro;}
    body{front-family: "Trebuchet MS, sans-serif;}</style>""",unsafe_allow_html=True)