import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from datetime import datetime

from orquestador import ejecutar_pipeline
from core.sistema_logging import log_evento, leer_logs
from agentes.generador_pdf import generar_pdf
from core.persistencia import insertar_archivo
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="📊 Analizador Lite", layout="wide")
st.title("📊 Analizador Descriptivo de Datos - Versión Lite")
if st.button("🔒 Cerrar sesión"):
    st.session_state.authenticated = False
    st.experimental_rerun()


# --- Autenticación por PIN ---
PIN = os.getenv("APP_PIN")
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    with st.form("login_form"):
        pin = st.text_input("🔑 Introduce tu PIN:", type="password")
        submitted = st.form_submit_button("Entrar")
        if submitted and pin == PIN:
            st.session_state.authenticated = True
            st.rerun()
        elif submitted:
            st.error("❌ PIN incorrecto.")
    st.stop()

# --- Subida del archivo ---
st.subheader("📂 Subir archivo de datos (.csv)")
archivo = st.file_uploader("Selecciona tu archivo:", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)
    nombre_archivo = archivo.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta_activa = "data/entrada/activa.csv"
    ruta_historico = f"data/entrada/historico/{timestamp}_{nombre_archivo}"
    df.to_csv(ruta_activa, index=False)
    df.to_csv(ruta_historico, index=False)

    insertar_archivo(nombre_original=nombre_archivo, ruta_guardado=ruta_historico,
                     tamano_bytes=len(archivo.getbuffer()), formato="csv", proyecto="Lite")

    log_evento(f"Archivo subido por usuario: {nombre_archivo}")
    st.success("✅ Archivo subido correctamente.")
    with st.expander("👀 Vista previa del archivo"):
        st.dataframe(df.head(10))

    if st.button("🔍 Ejecutar análisis"):
        log_evento("Inicio del análisis solicitado por usuario.")
        with st.spinner("⏳ Ejecutando análisis..."):
            resumen = ejecutar_pipeline(ruta_activa)

        if resumen:
            st.session_state["resumen_analisis"] = resumen
            st.success("✅ Análisis completado.")
            log_evento("Análisis completado con éxito.")

            with st.expander("✔️ Resultados del análisis"):
                st.subheader("📄 Resumen Descriptivo")
                st.dataframe(resumen["resumen"])
        else:
            st.error("❌ El análisis no se pudo completar.")
            log_evento("Análisis fallido o incompleto.", nivel="ERROR")

# --- Generar PDF si hay análisis previo ---
if "resumen_analisis" in st.session_state:
    st.subheader("🧾 Informe PDF")
    if st.button("📄 Generar informe PDF"):
        try:
            ruta_pdf = "data/salida/resultados/informe_lite.pdf"
            generar_pdf(
                resumen_analisis="data/salida/resultados/analisis_ultimo.csv",
                nombre_salida=ruta_pdf
            )
            st.success("📄 PDF generado correctamente.")
            log_evento("Informe PDF generado correctamente.")
            with open(ruta_pdf, "rb") as f:
                st.download_button("⬇️ Descargar PDF", f.read(), file_name="informe_lite.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"❌ Error al generar PDF: {e}")
            log_evento(f"Error al generar PDF: {e}", nivel="ERROR")

# --- Historial de análisis ---
st.divider()
with st.expander("📁 Historial de análisis anteriores"):
    try:
        st.download_button("⬇️ Descargar último resumen",
                           data=open("data/salida/resumen_analisis.csv", "rb"),
                           file_name="resumen_analisis.csv")
    except FileNotFoundError:
        st.warning("No se encontró el archivo de resumen.")

# --- Mostrar logs ---
st.subheader("📖 Registros del Sistema")
if st.button("📜 Ver últimos 10 eventos"):
    try:
        logs = leer_logs()
        ultimos_logs = logs[-10:]
        for line in ultimos_logs:
            st.text(line.strip())
    except Exception as e:
        st.error(f"❌ No se pudo leer el log: {e}")

