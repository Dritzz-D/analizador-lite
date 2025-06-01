# agentes/logs_agente.py

import os
import datetime

# Ruta del archivo de log
ruta_log = os.path.join(os.path.dirname(__file__), '..', 'logs', 'streamlit.log')

def log_evento(mensaje, nivel="INFO"):
    """
    Registra un evento en el log principal con formato estándar.
    Formato: [YYYY-MM-DD HH:MM:SS] [NIVEL] Mensaje
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] [{nivel.upper()}] {mensaje}\n"

    # Crear carpeta de logs si no existe
    os.makedirs(os.path.dirname(ruta_log), exist_ok=True)

    # Escribir el log
    with open(ruta_log, 'a', encoding='utf-8') as archivo:
        archivo.write(linea)

def borrar_logs():
    """
    Borra completamente el contenido del archivo de logs.
    """
    if os.path.exists(ruta_log):
        open(ruta_log, 'w').close()
        #Log eliminado. No registrar evento tras borrar (evita reiniciar el log con una línea)

def leer_logs(n_lineas=20):
    """
    Devuelve las últimas n líneas del log como lista de strings.
    """
    if os.path.exists(ruta_log):
        with open(ruta_log, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
            return lineas[-n_lineas:]
    return []

