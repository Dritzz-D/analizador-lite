# /root/proyectos/multiagente_datos/scripts/backup_diario.py

import sys
import os

# Aseguramos que se encuentre el paquete 'agentes'
sys.path.append("/root/proyectos/multiagente_datos")

from scripts.gestor_backup import realizar_backup_resultados

if __name__ == "__main__":
    realizar_backup_resultados()
