from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 16)
        self.cell(0, 10, "Prueba de PDF: Informe Lite", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 10)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", '', 12)
pdf.cell(0, 10, "Informe de prueba: texto compatible con PDF clásico.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.output("data/salida/resultados/test_fuente.pdf")
print("PDF generado: data/salida/resultados/test_fuente.pdf")

