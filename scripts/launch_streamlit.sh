#!/bin/bash

cd /root/proyectos/multiagente_datos
source venv/bin/activate
exec streamlit run app/app.py --server.port 8501 --server.enableXsrfProtection=false

