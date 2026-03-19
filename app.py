import streamlit as st
import json
import os
import sys

# Adiciona a pasta tools ao path para importar as ferramentas locais
sys.path.append(os.path.join(os.path.dirname(__file__), "tools"))
import lesson_generator
import rag_retriever
import pdf_exporter

st.set_page_config(page_title="S.I.N.A.P.S.E | Laboratório Inclusivo", layout="centered", page_icon="🧠")

# ==========================================
# INJEÇÃO PUSHDOWN DE CSS (TEMA PREMIUM)
# ==========================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

/* Fundo da tela em formato Gradiente Dark Purple / Absolute Black */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #3B1B6A 0%, #0A0A0A 40%, #050505 100%);
    color: #ffffff;
    font-family: 'Outfit', sans-serif !important;
}

/* Tipografia global */
html, body, [class*="css"]  {
    font-family: 'Outfit', sans-serif !important;
    color: #e0e0e0;
}
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Botões - Acento principal Verde Neon (da Referência) */
div[data-testid="stButton"] button {
    background-color: #CCFF00 !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 30px !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(204, 255, 0, 0.2) !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(204, 255, 0, 0.5) !important;
    background-color: #D4FF33 !important;
}

/* Correção de Contraste Absoluto (Textos Claros e Legíveis) */
label, label p, label span, .st-emotion-cache-1jbcun8, .st-emotion-cache-1629p8f p {
    color: #F8F5FF !important; /* Branco brilhante para não afundar no escuro */
    font-weight: 500 !important;
    font-size: 1.05rem !important;
}

/* ========================================================= */
/* BLINDAGEM NUCLEAR CONTRA CAIXAS BRANCAS DO EMOTION CACHE  */
/* ========================================================= */

/* 1. Tudo o que for filho da caixa de input vira 100% transparente para não vazar nas pontas */
div[data-testid="stTextInput"] > div:nth-child(2) *,
div[data-testid="stTextArea"] > div:nth-child(2) *,
div[data-testid="stSelectbox"] > div:nth-child(2) * {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* 2. Pintamos APENAS a casca mestra (A caixa que contém as sub-caixas) */
div[data-testid="stTextInput"] > div:nth-child(2),
div[data-testid="stTextArea"] > div:nth-child(2),
div[data-testid="stSelectbox"] > div:nth-child(2) {
    background-color: #1A1423 !important;
    border: 1px solid #322544 !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    padding: 0 !important;
}

/* 3. Estilizando o texto que você digita e os placeholders */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    color: #FFFFFF !important;
    font-size: 1.05rem !important;
    padding: 14px 18px !important;
    caret-color: #CCFF00 !important; /* Cursor de digitação piscando na cor Neon */
}

/* Força todo o texto de dentro do SelectBox (A aba que mostra "Propriedades Gerais...") ser branco! */
div[data-testid="stSelectbox"] [data-baseweb="select"] * {
    color: #FFFFFF !important;
    font-size: 1.05rem !important;
}

/* Ajusta o Placeholder (Dicas "Ex: Desejo que...") para um prata super legível */
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #B3ADC2 !important; 
    opacity: 1 !important;
}

/* 4. Foco brilha a casca mestre por fora, e não os filhos */
div[data-testid="stTextInput"] > div:nth-child(2):focus-within,
div[data-testid="stTextArea"] > div:nth-child(2):focus-within,
div[data-testid="stSelectbox"] > div:nth-child(2):focus-within {
    border-color: #8A2BE2 !important;
    box-shadow: 0 0 10px rgba(138, 43, 226, 0.4) !important;
}

/* Retirando o fundo branco das Selectboxes na hora de escolher itens (DropDown Portal) */
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"],
div[role="listbox"] ul,
ul[role="listbox"],
ul[data-testid="stSelectboxVirtualDropdown"] {
    background-color: #1A1423 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="popover"] li,
ul[role="listbox"] li,
li[role="option"] {
    background-color: #1A1423 !important;
    color: #FFFFFF !important;
}

li[aria-selected="true"], li[aria-selected="true"] * {
    background-color: #322544 !important;
    color: #FFFFFF !important;
}

div[data-baseweb="popover"] li:hover,
ul[role="listbox"] li:hover,
li[role="option"]:hover,
li[role="option"]:hover * {
    background-color: #48247A !important;
    color: #FFFFFF !important;
}

/* Efeito de destaque ao passar o mouse */
div[data-baseweb="popover"] li:hover,
ul[role="listbox"] li:hover,
li[role="option"]:hover,
li[role="option"]:hover * {
    background-color: #48247A !important;
    color: #FFFFFF !important;
}

/* Radio buttons container - Estética Sólida */
[role="radiogroup"] {
    background: #1A1423 !important;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #322544 !important;
}

/* Custom Dividers Neon */
hr {
    border-color: rgba(204, 255, 0, 0.2) !important;
}

/* Painéis Título */
div.stMarkdown p {
    font-size: 1.05rem;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# ==========================================

# Header Criativo
st.title("⚡ S.I.N.A.P.S.E.")
st.subheader("Sistema Inclusivo de Aulas Práticas, Sensoriais e Experimentais")

st.divider()

temas_disponiveis = [
    "Propriedades gerais e específicas da matéria",
    "Fenômeno físico e químico",
    "Substância e mistura",
    "Métodos de separação de misturas",
    "Atomística",
    "Tabela periódica",
    "Ligações químicas",
    "Polaridade e forças intermoleculares",
    "Leis ponderais",
    "Relações numéricas (massa, mol, entidades e volume)",
    "Estequiometria",
    "Funções inorgânicas"
]
tema = st.selectbox("Qual o Tema da Aula Prática?", options=temas_disponiveis)

observacoes = st.text_area("Observações do Professor (Opcional):", placeholder="Ex: desejo que a aula utilize separação de misturas homogêneas...")

condicao_visual = st.radio("Condição Visual do Aluno:", ["Cego", "Baixa visão"])

st.markdown("<br>", unsafe_allow_html=True)
btn_gerar = st.button("🚀 Gerar Plano de Aula", type="primary", use_container_width=True)

st.divider()

if btn_gerar:
    if not tema:
        st.warning("Por favor, digite o tema da aula primeiro.")
    else:
        with st.spinner("Buscando na literatura validada e adequando as Restrições (POP 02)..."):
            try:
                saida = lesson_generator.gerar_plano_de_aula(
                    tema=tema, 
                    observacoes=observacoes, 
                    condicao_visual=condicao_visual
                )
                plano = json.loads(saida) # Parseia a string de volta pra dic
                
                st.success("Plano Gerado com Sucesso! 🌟")
                
                try:
                    pdf_bytes = pdf_exporter.export_to_pdf(saida)
                    st.download_button(
                        label="📥 Compartilhar / Baixar Plano de Aula em PDF",
                        data=pdf_bytes,
                        file_name=f"Plano_SINAPSE_{tema.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar o PDF: {e}")
                    
                st.divider()
                
                # Exibindo estilizado e amigável
                st.subheader(f"📌 {plano.get('tema', tema)}")
                st.info(f"**🎯 Objetivo Inclusivo:** {plano.get('objetivo_inclusivo')}")
                
                roteiro = plano.get("Roteiro_Experimento", {})
                st.markdown(f"### 🔬 Experimento: {roteiro.get('titulo')}")
                
                with st.expander("🛠️ Materiais Necessários", expanded=True):
                    for item in roteiro.get("materiais", []):
                        st.markdown(f"- {item}")
                
                with st.expander("📖 Passo a Passo", expanded=True):
                    for i, passo in enumerate(roteiro.get("passo_a_passo", []), 1):
                        st.markdown(f"**{i}.** {passo}")
                
                st.warning(f"**🧑‍🦯 Adaptação para o Aluno Cego:**\n\n{roteiro.get('adaptacao_deficiencia_visual')}")
                
                with st.expander("⚠️ Regras Estritas de Segurança", expanded=False):
                    for regra in plano.get("dicas_seguranca", []):
                        st.markdown(f"- 🛑 {regra}")
                        
            except json.JSONDecodeError:
                st.error("O modelo não retornou um JSON válido. Veja a saída crua:")
                st.code(saida)
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")
