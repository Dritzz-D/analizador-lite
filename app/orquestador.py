# orquestador.py — Versión Lite final

import os
import pandas as pd
from datetime import datetime

from agentes.validador_dataset import validar_dataframe
from agentes.limpiador_datos import limpiar_datos
from agentes.analizador_descriptivo import analizar_datos
from core.persistencia import insertar_analisis
from core.sistema_logging import log_evento


def ejecutar_pipeline(ruta_archivo):
    """
    Ejecuta el pipeline completo: validación, limpieza, análisis y persistencia.
    Devuelve el resumen del análisis si es exitoso, o None si falla.
    """
    if not os.path.exists(ruta_archivo):
        log_evento("ERROR", f"Archivo no encontrado: {ruta_archivo}")
        return None

    try:
        df = pd.read_csv(ruta_archivo)
        log_evento("INFO", f"Archivo cargado: {ruta_archivo}")
    except Exception as e:
        log_evento("ERROR", f"Error al leer el archivo: {e}")
        return None

    resultado_validacion = validar_dataframe(df)
    if not resultado_validacion["valido"]:
        log_evento("ERROR", f"Validación fallida: {resultado_validacion['motivo']}")
        return None


    path_salida = "data/salida/datos_limpios.csv"
    df_limpio = limpiar_datos(df, "data/salida/datos_limpios.csv")
    log_evento("SUCCESS", "Datos limpiados correctamente.")


    resumen = analizar_datos(df_limpio)
    log_evento("SUCCESS", "Análisis descriptivo completado.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = os.path.basename(ruta_archivo)

    insertar_analisis(df_limpio, resumen, nombre_archivo=nombre_archivo, timestamp=timestamp)
    log_evento("SUCCESS", "Resultados insertados en la base de datos.")

    return {"resumen": resumen}


# Ejecutable standalone (opcional)
if __name__ == "__main__":
    ruta = "data/entrada/activa.csv"
    ejecutar_pipeline(ruta)

