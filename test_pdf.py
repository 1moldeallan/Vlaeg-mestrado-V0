from tools.pdf_exporter import export_to_pdf
import json

plano = {
    "tema": "A",
    "objetivo_inclusivo": "B",
    "Roteiro_Experimento": {"titulo": "C", "materiais": ["D"], "passo_a_passo": ["E"], "adaptacao_deficiencia_visual": "F"},
    "dicas_seguranca": ["G"]
}
try:
    export_to_pdf(json.dumps(plano))
    print("Sucesso!")
except Exception as e:
    print("Erro:", str(e))
