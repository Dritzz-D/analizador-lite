# agentes/validador_agente.py

import pandas as pd

def validar_dataframe(df, min_columnas_numericas=2, min_valores_por_columna=5):
    resultado = {
        "valido": False,
        "motivo": "",
        "detalles": {}
    }

    if df.empty:
        resultado["motivo"] = "El DataFrame está vacío."
        return resultado

    columnas_vacias = df.columns[df.isnull().all()].tolist()
    columnas_constantes = [col for col in df.columns if df[col].nunique(dropna=True) <= 1]
    columnas_numericas = df.select_dtypes(include=['number'])
    columnas_validas = []

    for col in columnas_numericas.columns:
        if columnas_numericas[col].dropna().shape[0] >= min_valores_por_columna:
            columnas_validas.append(col)

    resultado["detalles"] = {
        "columnas_numericas": columnas_numericas.columns.tolist(),
        "columnas_validas_para_analisis": columnas_validas,
        "columnas_vacias": columnas_vacias,
        "columnas_constantes": columnas_constantes,
        "columnas_totales": list(df.columns)
    }

    if len(columnas_validas) >= min_columnas_numericas:
        resultado["valido"] = True
        resultado["motivo"] = "Dataset válido para análisis completo."
    else:
        resultado["motivo"] = (
            f"Dataset inválido: solo {len(columnas_validas)} columna(s) numérica(s) válida(s). "
            f"Se requieren al menos {min_columnas_numericas}."
        )

    return resultado
