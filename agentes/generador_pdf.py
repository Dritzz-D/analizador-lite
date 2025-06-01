# agentes/generador_pdf.py

import os
import datetime
import pandas as pd
from fpdf import FPDF

# Ruta absoluta al directorio del proyecto (por seguridad al usar systemd)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FONT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'fonts'))

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Registrar variantes de la fuente Liberation
        self.add_font("Liberation", "", os.path.join(FONT_DIR, "LiberationSans-Regular.ttf"), uni=True)
        self.add_font("Liberation", "B", os.path.join(FONT_DIR, "LiberationSans-Regular.ttf"), uni=True)
        self.add_font("Liberation", "I", os.path.join(FONT_DIR, "LiberationSans-Regular.ttf"), uni=True)
        self.add_font("Liberation", "BI", os.path.join(FONT_DIR, "LiberationSans-Regular.ttf"), uni=True)
        self.set_font("Liberation", "", 12)

    def header(self):
        self.set_font("Liberation", 'B', 16)
        self.set_text_color(50, 50, 100)
        self.cell(0, 10, 'Informe Descriptivo de Datos', ln=True, align='C')
        self.ln(5)
        self.set_font("Liberation", '', 10)
        now = datetime.datetime.now()
        self.cell(0, 10, f"Generado: {now.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Liberation", 'I', 8)
        self.set_text_color(159, 159, 159)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')


def generar_pdf(resumen_analisis: str, nombre_salida: str):
    """
    Genera un informe PDF a partir de un CSV de resumen de análisis.
    :param resumen_analisis: Ruta al archivo CSV (ej. 'data/salida/resultados/analisis_ultimo.csv')
    :param nombre_salida: Ruta del archivo PDF de salida.
    """
    if not os.path.exists(resumen_analisis):
        raise FileNotFoundError(f"No se encontró el archivo de resumen: {resumen_analisis}")

    df = pd.read_csv(resumen_analisis)

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Liberation", 'B', 14)
    pdf.set_text_color(50, 51, 102)
    pdf.cell(0, 10, "Resumen Descriptivo", ln=True)
    pdf.ln(5)

    pdf.set_font("Liberation", '', 12)
    pdf.set_text_color(0, 0, 0)

    for index, row in df.iterrows():
        variable = row.get("Variable", f"Variable {index}")
        pdf.set_font("Liberation", 'B', 12)
        pdf.cell(0, 10, f"{variable}", ln=True)
        pdf.set_font("Liberation", '', 12)

        for col in df.columns:
            if col != "Variable":
                valor = row[col]
                pdf.cell(0, 10, f"   - {col.capitalize()}: {valor}", ln=True)
        pdf.ln(2)

    os.makedirs(os.path.dirname(nombre_salida), exist_ok=True)
    pdf.output(nombre_salida)

