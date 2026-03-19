from fpdf import FPDF
class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "S.I.N.A.P.S.E - Plano de Aula", align="C")
        self.ln(15)

pdf = PDF()
pdf.add_page()
pdf.set_font("helvetica", "B", 14)
pdf.multi_cell(0, 8, "O que faremos hoje:")
print("Sucesso!")
