# agentes/analizador_descriptivo.py

import pandas as pd
import os

def analizar_datos(df: pd.DataFrame) -> dict:
    """
    Realiza análisis estadístico descriptivo sobre columnas numéricas del DataFrame.
    Guarda un resumen en CSV y lo devuelve como dict para visualización.
    """

    columnas_validas = [
        col for col in df.select_dtypes(include=["number"]).columns
        if df[col].dropna().shape[0] >= 5
    ]

    if len(columnas_validas) < 2:
        return {
            "ERROR": "No hay suficientes columnas numéricas válidas (mínimo 2 con al menos 5 valores no nulos)."
        }

    resumen = {
        col: {
            "media": round(df[col].mean(), 2),
            "mínimo": df[col].min(),
            "máximo": df[col].max(),
            "conteo": int(df[col].count())
        }
        for col in columnas_validas
    }

    resumen_df = pd.DataFrame(resumen).T.reset_index().rename(columns={"index": "Variable"})
    os.makedirs("data/salida/resultados", exist_ok=True)
    resumen_df.to_csv("data/salida/resultados/analisis_ultimo.csv", index=False)

    return {"resumen": resumen_df}

