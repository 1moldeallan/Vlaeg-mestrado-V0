import streamlit as st
import json
import os
import sys
import html as html_lib

# Adiciona a pasta tools ao path para importar as ferramentas locais
sys.path.append(os.path.join(os.path.dirname(__file__), "tools"))
import lesson_generator
import rag_retriever
import pdf_exporter

st.set_page_config(
    page_title="S.I.N.A.P.S.E | Laboratório Inclusivo",
    layout="wide",
    page_icon=":material/science:",
)

# ============================================================
# TEMA: "CADERNO DE LABORATÓRIO INCLUSIVO"
# Editorial científico · alto contraste · acessível (baixa visão)
# Fraunces (display) + Atkinson Hyperlegible (corpo) + IBM Plex Mono (etiquetas)
# ============================================================
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700;9..144,900&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --paper:       #F6F4EC;   /* fundo bege quente */
    --paper-deep:  #EFEBDD;   /* sombra de papel */
    --surface:     #FFFFFF;   /* cartões */
    --ink:         #15201B;   /* tinta quase-preta */
    --ink-soft:    #41504A;   /* texto secundário */
    --line:        #DCD7C7;   /* linhas finas */
    --green:       #0B6E4F;   /* ação primária */
    --green-deep:  #084F3A;
    --green-tint:  #E7F1EC;
    --amber:       #B4530A;   /* acento / atenção */
    --amber-tint:  #FBEEDF;
    --crimson:     #A02B2B;   /* segurança / proibições */
}

/* ---------- Base ---------- */
[data-testid="stAppViewContainer"] {
    background-color: var(--paper) !important;
    background-image:
        radial-gradient(1200px 600px at 80% -10%, rgba(11,110,79,0.06), transparent 60%),
        linear-gradient(rgba(11,110,79,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(11,110,79,0.045) 1px, transparent 1px);
    background-size: auto, 30px 30px, 30px 30px;
    font-family: 'Atkinson Hyperlegible', sans-serif !important;
    color: var(--ink);
}
[data-testid="stHeader"] { background: transparent !important; }

html, body, [class*="css"] {
    font-family: 'Atkinson Hyperlegible', sans-serif !important;
    color: var(--ink);
}

/* Constrange a leitura a uma medida confortável */
[data-testid="stMain"] .block-container {
    max-width: 940px !important;
    padding-top: 2.2rem !important;
    padding-bottom: 4rem !important;
}

h1, h2, h3, h4 {
    font-family: 'Fraunces', Georgia, serif !important;
    color: var(--ink) !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* ---------- Hero ---------- */
.sinapse-hero {
    animation: riseIn 0.7s cubic-bezier(.2,.7,.2,1) both;
    margin-bottom: 0.4rem;
}
.eyebrow {
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--green);
}
.hero-title {
    font-family: 'Fraunces', serif !important;
    font-weight: 900 !important;
    font-size: clamp(2.6rem, 6vw, 4.1rem) !important;
    line-height: 0.98 !important;
    color: var(--ink) !important;
    margin: 0.35rem 0 0.5rem 0 !important;
    letter-spacing: -0.02em;
}
.hero-title .dot { color: var(--green); }
.hero-sub {
    font-size: 1.12rem;
    line-height: 1.55;
    color: var(--ink-soft);
    max-width: 620px;
    margin: 0;
}
.hero-rule {
    height: 4px;
    width: 100%;
    margin-top: 1.4rem;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--green) 0%, var(--amber) 55%, transparent 100%);
}

/* ---------- Etiquetas de seção (mono eyebrow) ---------- */
.section-tag {
    font-family: 'IBM Plex Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--green-deep);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.2rem;
}
.section-tag::before {
    content: "";
    width: 22px; height: 2px;
    background: var(--green);
    display: inline-block;
}

/* ---------- Cartões (container border + expander) ---------- */
div[data-testid="stForm"],
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    background: var(--surface) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.8) inset, 0 18px 40px -28px rgba(21,32,27,0.35) !important;
}

/* ---------- Labels de campos ---------- */
label, label p {
    color: var(--ink-soft) !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}

/* ---------- Inputs / selectbox / textarea ---------- */
div[data-testid="stTextInput"] > div:nth-child(2),
div[data-testid="stTextArea"] > div:nth-child(2),
div[data-testid="stSelectbox"] > div:nth-child(2) {
    background-color: var(--paper) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 12px !important;
    padding: 0 !important;
    transition: border-color .18s ease, box-shadow .18s ease, background .18s ease;
}
div[data-testid="stTextInput"] > div:nth-child(2) *,
div[data-testid="stTextArea"] > div:nth-child(2) *,
div[data-testid="stSelectbox"] > div:nth-child(2) * {
    background-color: transparent !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    color: var(--ink) !important;
    font-size: 1.02rem !important;
    padding: 13px 16px !important;
    caret-color: var(--green) !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"] * { color: var(--ink) !important; font-size: 1.02rem !important; }
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder { color: #9A9483 !important; }

div[data-testid="stTextInput"] > div:nth-child(2):focus-within,
div[data-testid="stTextArea"] > div:nth-child(2):focus-within,
div[data-testid="stSelectbox"] > div:nth-child(2):focus-within {
    border-color: var(--green) !important;
    background-color: var(--surface) !important;
    box-shadow: 0 0 0 4px rgba(11,110,79,0.14) !important;
}

/* Dropdown popover */
div[data-baseweb="popover"] > div,
ul[role="listbox"],
ul[data-testid="stSelectboxVirtualDropdown"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    box-shadow: 0 20px 45px -20px rgba(21,32,27,0.4) !important;
}
li[role="option"] { background: var(--surface) !important; color: var(--ink-soft) !important; }
li[aria-selected="true"], li[aria-selected="true"] * {
    background-color: var(--green-tint) !important;
    color: var(--green-deep) !important;
    font-weight: 700 !important;
}
li[role="option"]:hover, li[role="option"]:hover * {
    background-color: var(--paper-deep) !important;
    color: var(--ink) !important;
}

/* ---------- Radio (condição visual) ---------- */
[role="radiogroup"] { background: transparent !important; gap: 8px !important; }
[role="radiogroup"] label {
    border: 1.5px solid var(--line) !important;
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    transition: all .18s ease;
}
[role="radiogroup"] label:hover { border-color: var(--green) !important; }
[role="radiogroup"] input { accent-color: var(--green) !important; }

/* ---------- Botão primário ---------- */
div[data-testid="stButton"] button {
    background-color: var(--green) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Atkinson Hyperlegible', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    padding: 13px 24px !important;
    letter-spacing: 0.01em;
    transition: transform .15s ease, box-shadow .2s ease, background .2s ease !important;
    box-shadow: 0 10px 22px -10px rgba(11,110,79,0.65) !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px);
    background-color: var(--green-deep) !important;
    box-shadow: 0 16px 30px -12px rgba(11,110,79,0.7) !important;
}
div[data-testid="stButton"] button:active { transform: translateY(0); }

/* ---------- Botão de download (secundário, contornado) ---------- */
div[data-testid="stDownloadButton"] button {
    background-color: var(--surface) !important;
    color: var(--green-deep) !important;
    border: 1.5px solid var(--green) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    padding: 13px 24px !important;
    transition: all .18s ease !important;
    cursor: pointer !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background-color: var(--green-tint) !important;
    transform: translateY(-2px);
}

/* ---------- Expanders (cartões accordion) ---------- */
[data-testid="stExpander"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 14px 32px -26px rgba(21,32,27,0.4) !important;
    margin-bottom: 14px !important;
}
[data-testid="stExpander"] summary {
    background-color: var(--surface) !important;
    color: var(--ink) !important;
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    font-size: 1.08rem !important;
    padding: 15px 20px !important;
    cursor: pointer !important;
}
[data-testid="stExpander"] summary:hover { background-color: var(--paper) !important; }
[data-testid="stExpander"] > div:last-child { border-top: 1px solid var(--line) !important; }

/* ---------- Alertas (info / success / warning) ---------- */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid var(--line) !important;
    border-left: 5px solid var(--green) !important;
    background: var(--surface) !important;
}
[data-testid="stAlert"] * { color: var(--ink) !important; }

/* ---------- Cartão de Adaptação (o coração do projeto) ---------- */
.adapt-card {
    position: relative;
    background:
        radial-gradient(600px 200px at 100% 0%, rgba(180,83,10,0.08), transparent 70%),
        linear-gradient(180deg, #FFFDF8 0%, var(--surface) 100%);
    border: 1.5px solid var(--amber);
    border-radius: 18px;
    padding: 26px 28px;
    margin: 8px 0 18px 0;
    box-shadow: 0 20px 45px -28px rgba(180,83,10,0.55);
    animation: riseIn 0.5s ease both;
}
.adapt-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--amber);
    margin-bottom: 0.5rem;
}
.adapt-title {
    font-family: 'Fraunces', serif !important;
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--ink);
    margin: 0 0 0.7rem 0;
}
.adapt-body {
    font-size: 1.08rem;
    line-height: 1.65;
    color: var(--ink);
    margin: 0;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, var(--green-deep) 0%, #0A3D2D 100%) !important;
    border-right: 1px solid rgba(0,0,0,0.2) !important;
}
[data-testid="stSidebar"] * { color: #EDF3EF !important; }
.sb-brand {
    font-family: 'Fraunces', serif;
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: 0.02em;
    color: #FFFFFF;
    margin: 0.2rem 0 0.1rem 0;
}
.sb-tag {
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.68rem;
    color: #9FD9C2;
}
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-color: rgba(255,255,255,0.22) !important;
    background: rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { border-color: #9FD9C2 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.16) !important; }
.sb-note {
    font-size: 0.85rem;
    line-height: 1.5;
    color: #BFE0D2 !important;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 12px;
    padding: 12px 14px;
}

/* ---------- Listas no corpo ---------- */
div.stMarkdown p { font-size: 1.04rem; line-height: 1.65; }

/* ---------- Divisores ---------- */
hr { border-color: var(--line) !important; margin: 1.8rem 0 !important; }

/* ---------- Animação ---------- */
@keyframes riseIn {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Esconde âncoras flutuantes dos cabeçalhos */
[data-testid="stHeaderActionElements"] { display: none !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
# ============================================================

# ---------- Sidebar: identidade + configuração ----------
with st.sidebar:
    st.markdown(
        "<div class='sb-brand'>S.I.N.A.P.S.E.</div>"
        "<div class='sb-tag'>Laboratório Inclusivo</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown("<div class='sb-tag'>Configuração do Aluno</div>", unsafe_allow_html=True)
    condicao_visual = st.radio("Condição visual:", ["CEGO", "BAIXA VISÃO"], index=0)
    st.divider()
    st.markdown(
        "<div class='sb-note'>As fontes científicas são recuperadas automaticamente da base "
        "validada (RAG) para fundamentar cada experimento.</div>",
        unsafe_allow_html=True,
    )

# ---------- Hero ----------
st.markdown(
    """
    <div class="sinapse-hero">
        <span class="eyebrow">Protocolo V.L.A.E.G · Química Acessível</span>
        <h1 class="hero-title">S.I.N.A.P.S.E<span class="dot">.</span></h1>
        <p class="hero-sub">Planos de aula práticos de Química desenhados para a turma inteira —
        com substituição sensorial garantida para alunos com deficiência visual, sem isolamento.</p>
        <div class="hero-rule"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Cartão de entrada ----------
with st.container(border=True):
    st.markdown("<span class='section-tag'>Origem Acadêmica</span>", unsafe_allow_html=True)
    st.markdown("#### :material/menu_book: Tema do experimento")

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
        "Funções inorgânicas",
    ]
    tema = st.selectbox("Selecione o tema mapeado para o experimento", options=temas_disponiveis)

    observacoes = st.text_area(
        "Observações do docente (opcional)",
        placeholder="Ex.: priorizar materiais recicláveis para o experimento…",
        height=120,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    btn_gerar = st.button(
        "Gerar plano de aula via Gemini",
        type="primary",
        use_container_width=True,
        icon=":material/auto_awesome:",
    )

if btn_gerar:
    if not tema:
        st.warning("Por favor, selecione o tema da aula primeiro.")
    else:
        with st.spinner("Buscando na literatura validada e adequando as restrições (POP 02)…"):
            try:
                saida = lesson_generator.gerar_plano_de_aula(
                    tema=tema,
                    observacoes=observacoes,
                    condicao_visual=condicao_visual,
                )
                plano = json.loads(saida)  # Parseia a string de volta pra dict

                st.success("Plano gerado com sucesso!", icon=":material/stars:")

                try:
                    pdf_bytes = pdf_exporter.export_to_pdf(saida)
                    st.download_button(
                        label="Compartilhar / baixar plano de aula em PDF",
                        data=pdf_bytes,
                        file_name=f"Plano_SINAPSE_{tema.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        icon=":material/download:",
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar o PDF: {e}")

                st.divider()

                # ---------- Exibição do plano ----------
                st.markdown("<span class='section-tag'>Plano de Aula</span>", unsafe_allow_html=True)
                st.subheader(f":material/push_pin: {plano.get('tema', tema)}", anchor=False)
                st.info(f"**Objetivo inclusivo:** {plano.get('objetivo_inclusivo')}", icon=":material/ads_click:")

                roteiro = plano.get("Roteiro_Experimento", {})
                st.subheader(f":material/science: Experimento: {roteiro.get('titulo')}", anchor=False)

                with st.expander(":material/handyman: Materiais necessários", expanded=True):
                    for item in roteiro.get("materiais", []):
                        st.markdown(f"- {item}")

                with st.expander(":material/menu_book: Passo a passo", expanded=True):
                    for i, passo in enumerate(roteiro.get("passo_a_passo", []), 1):
                        st.markdown(f"**{i}.** {passo}")

                # Destaque central: adaptação para deficiência visual
                adaptacao = roteiro.get("adaptacao_deficiencia_visual") or ""
                adaptacao_html = html_lib.escape(adaptacao).replace("\n", "<br>")
                st.markdown(
                    f"""
                    <div class="adapt-card">
                        <div class="adapt-eyebrow">Núcleo de Acessibilidade · Substituição Sensorial</div>
                        <div class="adapt-title">Adaptação para o aluno ({condicao_visual})</div>
                        <p class="adapt-body">{adaptacao_html}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander(":material/warning: Regras estritas de segurança", expanded=False):
                    for regra in plano.get("dicas_seguranca", []):
                        st.markdown(f"- :material/block: {regra}")

            except json.JSONDecodeError:
                st.error("O modelo não retornou um JSON válido. Veja a saída crua:")
                st.code(saida)
            except Exception as e:
                st.error(f"Erro inesperado: {str(e)}")
