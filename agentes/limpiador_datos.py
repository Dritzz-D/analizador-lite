# agentes/limpiador_datos.py

import pandas as pd
from core.sistema_logging import log_evento

def detectar_columnas_numericas_reales(df, umbral_nulos=0.5, excluir_nombres_sospechosos=True):
    df_numerico = df.select_dtypes(include=['number'])
    columnas_validas = []
    sospechosas = {'nombre', 'profesion', 'id', 'codigo', 'clave'}

    for col in df_numerico.columns:
        proporcion_nulos = df[col].isnull().mean()
        if proporcion_nulos > umbral_nulos:
            continue
        if excluir_nombres_sospechosos and col.lower() in sospechosas:
            continue
        columnas_validas.append(col)

    return columnas_validas


def limpiar_datos(df, path_salida):
    """
    Limpieza Lite:
    - Limpia nombres de columnas
    - Intenta conversión a numérico
    - Elimina duplicados
    - Rellena nulos
    - Guarda CSV limpio
    """

    try:
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip().str.replace(" ", "_")

        # Limpiar strings
        df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

        # Convertir a numérico columnas plausibles
        for col in df.columns:
            if df[col].dtype == 'object':
                temp_col = df[col].astype(str).str.replace(",", ".").str.replace(r"[^\d\.\-]", "", regex=True)
                numeric_try = pd.to_numeric(temp_col, errors='coerce')
                if numeric_try.notna().mean() >= 0.7 and numeric_try.notna().sum() >= 5:
                    df[col] = numeric_try

        columnas_numericas = detectar_columnas_numericas_reales(df)
        log_evento("INFO", f"Columnas numéricas detectadas: {columnas_numericas}")

        df = df.drop_duplicates()

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna("Desconocido")
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        df.to_csv(path_salida, index=False)
        log_evento("SUCCESS", f"Datos limpiados exitosamente: {path_salida}")
        return df

    except Exception as e:
        log_evento("ERROR", f"Error en limpieza: {e}")
        return pd.DataFrame()  # en caso de fallo

