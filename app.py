import streamlit as st
import json
import os
import sys

# Adiciona a pasta tools ao path para importar as ferramentas locais
sys.path.append(os.path.join(os.path.dirname(__file__), "tools"))
import lesson_generator
import rag_retriever

st.set_page_config(page_title="Agente VLAEG | Química Inclusiva", layout="wide", page_icon="🧪")

# Header Criativo
st.title("🧪 Planejador de Laboratório: Química Inclusiva")
st.markdown("""
**Protocolo V.L.A.E.G. Ativado** | Este agente cruza artigos e manuais acadêmicos (`knowledge_base/`) para criar aulas práticas originais baseadas em percepção multi-sensorial (tato, audição e olfato) adaptadas para alunos com deficiência visual.
""")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Configuração da Aula")
    
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
    
    condicao_visual = st.radio("Condição Visual do Aluno:", ["Cego por completo", "Baixa visão"])
    btn_build_index = st.button("📚 Indexar Manuais (Primeiro Uso RAG)")
    if btn_build_index:
        with st.spinner("Lendo os PDFs e criando banco de inteligência da turma..."):
            try:
                rag_retriever.build_vector_store()
                st.success("Arquivos indexados com sucesso! O RAG está pronto.")
            except Exception as e:
                st.error(f"Erro ao indexar: {e}")

with col2:
    st.header("🤖 Plano da IA Gerado")
    
    if st.button("✨ Gerar Plano de Aula", type="primary", use_container_width=True):
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
