import json
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "S.I.N.A.P.S.E - Plano de Aula Inclusivo", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C", new_x="LMARGIN", new_y="NEXT")

def sanitizar(texto: str) -> str:
    texto = str(texto).replace('\u2013', '-').replace('\u2014', '-').replace('\u201c', '"').replace('\u201d', '"')
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def export_to_pdf(plano_json: str) -> bytes:
    try:
        plano = json.loads(plano_json)
    except Exception:
        plano = {"tema": "Erro na leitura do Plano", "objetivo_inclusivo": "Falha no parse."}

    # Força a criação explícita no formato folha A4 e unidade mm
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    pdf.set_font("helvetica", "B", 14)
    texto_tema = sanitizar(f"O que faremos hoje: {plano.get('tema', '')}")
    pdf.multi_cell(0, 8, texto_tema, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    pdf.set_font("helvetica", "B", 12)
    pdf.multi_cell(0, 6, sanitizar("Objetivo Inclusivo:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 6, sanitizar(str(plano.get("objetivo_inclusivo", ""))), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    roteiro = plano.get("Roteiro_Experimento", {})
    if not isinstance(roteiro, dict):
        roteiro = {}
        
    titulo = roteiro.get("titulo", "")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.multi_cell(0, 6, sanitizar(f"Experimento: {titulo}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Materiais Necessarios:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    materiais = roteiro.get("materiais", [])
    if isinstance(materiais, list):
        for mat in materiais:
            pdf.multi_cell(0, 6, sanitizar(f"- {mat}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Passo a Passo do Laboratorio:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    passos = roteiro.get("passo_a_passo", [])
    if isinstance(passos, list):
        for i, passo in enumerate(passos, 1):
            pdf.multi_cell(0, 6, sanitizar(f"{i}. {passo}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Adaptacao para a Deficiencia Visual:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 6, sanitizar(str(roteiro.get("adaptacao_deficiencia_visual", ""))), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Dicas e Parametros de Seguranca V.L.A.E.G.:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 11)
    dicas = plano.get("dicas_seguranca", [])
    if isinstance(dicas, list):
        for dica in dicas:
            pdf.multi_cell(0, 6, sanitizar(f"- {dica}"), new_x="LMARGIN", new_y="NEXT")
        
    return bytes(pdf.output())
