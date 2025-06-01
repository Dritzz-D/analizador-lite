#!/bin/bash

echo "🔧 Iniciando limpieza y preparación del entorno Lite..."

# Crear estructura de carpetas necesarias
mkdir -p app agentes core data/entrada/historico data/backups data/salida/resultados logs

echo "✅ Carpetas creadas/verificadas: app/, agentes/, core/, data/, logs/"

# Crear archivo base orquestador.py si no existe
if [ ! -f app/orquestador.py ]; then
  echo "🧠 Generando orquestador.py base..."
  cat > app/orquestador.py << 'EOF'
import os
import pandas as pd
from core.sistema_logging import log_evento
from agentes.validador_dataset import validar_dataframe
from agentes.limpiador_datos import limpiar_datos
from agentes.analizador_descriptivo import analizar_datos

def ejecutar_pipeline():
    try:
        path_entrada = "data/entrada/activa.csv"
        if not os.path.exists(path_entrada):
            log_evento("ARCHIVO ACTIVO NO ENCONTRADO.", nivel="ERROR")
            return

        log_evento("Iniciando limpieza de datos.", nivel="INFO")
        limpiar_datos(path_entrada)

        validacion = validar_dataframe(pd.read_csv("data/salida/datos_limpios.csv"))
        if not validacion["valido"]:
            log_evento(f"No se puede continuar: {validacion['motivo']}", nivel="ERROR")
            return

        analizar_datos("data/salida/datos_limpios.csv")

    except Exception as e:
        log_evento(f"Error general en pipeline: {e}", nivel="ERROR")
EOF
  echo "✅ orquestador.py generado."
else
  echo "ℹ️ orquestador.py ya existe, no se sobrescribe."
fi

# Advertir sobre app.py si no existe
if [ ! -f app/app.py ]; then
  echo "⚠️ app.py no encontrado. Debes restaurarlo manualmente o pegar la versión Lite funcional."
else
  echo "✅ app.py detectado correctamente."
fi

# Limpiar requirements.txt con dependencias esenciales
echo "📦 Generando requirements.txt limpio..."
pip freeze | grep -E 'streamlit|pandas|numpy|matplotlib|reportlab|fpdf' > requirements.txt

# Mostrar resultado
echo "📄 Contenido actual de requirements.txt:"
cat requirements.txt

# Confirmar estructura
echo -e "\n📂 Estructura de /data actual:"
ls -R data

echo -e "\n✅ Preparación finalizada. Puedes ejecutar: streamlit run app/app.py"

