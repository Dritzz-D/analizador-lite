import sqlite3
from datetime import datetime
import os

# Ruta unificada de la base de datos Lite
DB_PATH = os.path.join("data", "db", "asistente_datos.db")


def insertar_archivo(nombre_original, ruta_guardado, tamano_bytes, formato, proyecto=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fecha_subida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO archivos (nombre_original, ruta_guardado, tamano_bytes, formato, proyecto, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nombre_original, ruta_guardado, tamano_bytes, formato, proyecto, fecha_subida))

    conn.commit()
    conn.close()


def insertar_analisis(df, resumen, nombre_archivo, timestamp):
    """
    Guarda un resumen del análisis descriptivo en la tabla 'archivos'.
    Simplificado para la versión Lite.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        filas, columnas = df.shape
        tamano_bytes = df.memory_usage(deep=True).sum()
        formato = "csv"
        proyecto = "Lite"

        cursor.execute('''
            INSERT INTO archivos (nombre_original, ruta_guardado, tamano_bytes, formato, proyecto, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre_archivo, f"data/entrada/historico/{timestamp}_{nombre_archivo}",
              tamano_bytes, formato, proyecto, timestamp))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Fallo al insertar análisis: {e}")

