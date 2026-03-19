from fpdf import FPDF
import json

plano = {
    "tema": "Misturas",
    "objetivo_inclusivo": "Separar coisas",
    "Roteiro_Experimento": {"titulo": "C", "materiais": ["D"], "passo_a_passo": ["E"], "adaptacao_deficiencia_visual": "F"},
    "dicas_seguranca": ["G"]
}

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "S.I.N.A.P.S.E", align="C", new_x="LMARGIN", new_y="NEXT")

pdf = FPDF(format="A4")
pdf.add_page()
pdf.set_font("helvetica", "B", 14)
pdf.multi_cell(0, 8, "A", new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)
pdf.multi_cell(0, 6, "B", new_x="LMARGIN", new_y="NEXT")
pdf.multi_cell(0, 6, "C", new_x="LMARGIN", new_y="NEXT")

print("Sucesso!")
