import json
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 14)
        self.cell(0, 10, "S.I.N.A.P.S.E - Plano de Aula Inclusivo", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

def sanitizar(texto: str) -> str:
    # FPDF fonts basicas as vezes conflitam com acentos latinos complexos.
    # Essa higienizacao limpa emojis e mantem acentos normais PT-BR compativeis com latin-1
    texto = str(texto).replace('\u2013', '-').replace('\u2014', '-').replace('\u201c', '"').replace('\u201d', '"')
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def export_to_pdf(plano_json: str) -> bytes:
    try:
        plano = json.loads(plano_json)
    except Exception:
        plano = {"tema": "Erro na leitura do Plano", "objetivo_inclusivo": "Falha no parse."}

    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font("helvetica", "B", 14)
    pdf.multi_cell(0, 8, sanitizar(f"O que faremos hoje: {plano.get('tema', '')}"))
    pdf.ln(3)
    
    pdf.set_font("helvetica", "B", 12)
    pdf.multi_cell(0, 6, sanitizar("Objetivo Inclusivo:"))
    pdf.set_font("helvetica", "", 12)
    pdf.multi_cell(0, 6, sanitizar(str(plano.get("objetivo_inclusivo", ""))))
    pdf.ln(5)
    
    roteiro = plano.get("Roteiro_Experimento", {})
    if not isinstance(roteiro, dict):
        roteiro = {}
        
    titulo = roteiro.get("titulo", "")
    
    pdf.set_font("helvetica", "B", 12)
    pdf.multi_cell(0, 6, sanitizar(f"Experimento: {titulo}"))
    pdf.ln(3)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Materiais Necessarios:"))
    pdf.set_font("helvetica", "", 11)
    materiais = roteiro.get("materiais", [])
    if isinstance(materiais, list):
        for mat in materiais:
            pdf.multi_cell(0, 6, sanitizar(f"- {mat}"))
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Passo a Passo do Laboratorio:"))
    pdf.set_font("helvetica", "", 11)
    passos = roteiro.get("passo_a_passo", [])
    if isinstance(passos, list):
        for i, passo in enumerate(passos, 1):
            pdf.multi_cell(0, 6, sanitizar(f"{i}. {passo}"))
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Adaptacao para a Deficiencia Visual:"))
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 6, sanitizar(str(roteiro.get("adaptacao_deficiencia_visual", ""))))
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 11)
    pdf.multi_cell(0, 6, sanitizar("Dicas e Parametros de Seguranca V.L.A.E.G.:"))
    pdf.set_font("helvetica", "", 11)
    dicas = plano.get("dicas_seguranca", [])
    for dica in dicas:
        pdf.multi_cell(0, 6, sanitizar(f"- {dica}"))
        
    return bytes(pdf.output())
