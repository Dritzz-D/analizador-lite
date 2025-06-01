# agentes/backups_agente.py

import os
import shutil
import datetime

def realizar_backup_resultados():
    """
    Realiza un backup de todos los archivos de resultados generados.
    """
    origen = os.path.join(os.path.dirname(__file__), '..', 'data', 'salida', 'resultados')
    destino_base = os.path.join(os.path.dirname(__file__), '..', 'data', 'backups')

    # Crear carpeta de destino si no existe
    os.makedirs(destino_base, exist_ok=True)

    if not os.path.exists(origen) or not os.listdir(origen):
        print("[BACKUP] No hay resultados para respaldar.")
        return

    # Crear subcarpeta con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(destino_base, f"backup_{timestamp}")
    os.makedirs(destino, exist_ok=True)

    # Copiar archivos
    for archivo in os.listdir(origen):
        try:
            origen_archivo = os.path.join(origen, archivo)
            destino_archivo = os.path.join(destino, archivo)
            shutil.copy2(origen_archivo, destino_archivo)
        except Exception as e:
            print(f"[BACKUP] Error al copiar {archivo}: {e}")

    print(f"[BACKUP] Backup realizado exitosamente en: {destino}")
