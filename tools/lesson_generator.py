import os
import json
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import rag_retriever

class RoteiroExperimento(BaseModel):
    titulo: str = Field(description="Título criativo e claro do experimento")
    materiais: List[str] = Field(description="Lista de materiais e reagentes necessários")
    passo_a_passo: List[str] = Field(description="Procedimento do laboratório ordenado cronologicamente")
    adaptacao_deficiencia_visual: str = Field(description="Explicação exata de como a pessoa cega vai participar ativamente e como a percepção multi-sensorial ocorrerá (tato, audição, cheiro seguro)")

class PlanoDeAulaSaida(BaseModel):
    tema: str = Field(description="Tema central da aula de química")
    objetivo_inclusivo: str = Field(description="Objetivo educacional voltado à inclusão de todos os alunos")
    Roteiro_Experimento: RoteiroExperimento
    dicas_seguranca: List[str] = Field(description="Regras severas de contenção e uso seguro no laboratório inclusivo")

def gerar_plano_de_aula(tema: str, observacoes: str = "", condicao_visual: str = "Cego por completo") -> str:
    """Invoca o LLM com o Contexto RAG e força a saída no Schema JSON validado."""
    rag_retriever.load_environment()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return json.dumps({"erro": "GEMINI_API_KEY ausente no .env"})

    try:
        contexto_pdf = rag_retriever.retrieve_context(tema)
    except Exception as e:
        contexto_pdf = f"[AVISO: Banco de dados vetorial ainda não foi inicializado. Erro: {str(e)}]"

    # Usaremos um modelo robusto para raciocinar sobre inclusão
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2, # Reduzimos a temperatura para seguir estritamente o POP
        convert_system_message_to_human=True,
        google_api_key=api_key
    )
    
    # Injetar o Schema nas instruções
    parser = PlanoDeAulaSaida.schema_json()

    template = """
    Você é um agente educacional focado em Química e Educação Inclusiva (Protocolo V.L.A.E.G.).
    A sua tarefa é construir um Plano de Aula Prática sobre o tema: {tema}.
    
    A sala possui alunos videntes e um aluno com a seguinte condição visual: {condicao_visual}. A aula precisa ser A MESMA para todos, sem isolamento.

    ### OBSERVAÇÕES E DIRETRIZES DO PROFESSOR:
    {observacoes}

    ### CONTEXTO DA BASE CIENTÍFICA (EXTRAÍDO DE ARTIGOS/LIVROS DA KNOWLEDGE_BASE):
    {contexto}

    ### SUAS REGRAS ABSOLUTAS (OBRIGATÓRIO OBEDECER):
    1. PROIBIDO DESFECHOS VISUAIS: o experimento nunca pode depender APENAS de mudanças de cor ou precipitados intocáveis (ex: em ácido).
    2. SUBSTITUIÇÃO SENSORIAL OBRIGATÓRIA: troque desfechos visuais por tato (variação térmica, não perigosa), audição (efervescência) ou olfato seguro.
    3. VIDRARIA E EQUIPAMENTO: É proibido exigir alinhamento de menisco para medir líquidos. Use seringas com limitadores.
    4. FONTE DE CALOR E ESPAÇO: É proibida chama aberta (Bico de Bunsen) solta. Prefira chapas elétricas. O experimento do aluno cego tem que ocorrer obrigatoriamente dentro de uma "bandeja de contenção".
    5. TRANSFERÊNCIA DE FLUIDO: Proibido o "olhômetro". Medidas devem ser padronizadas de forma tátil/sonora.

    Escreva o resultado final **OBRIGATORIAMENTE** seguindo o esquema JSON abaixo. 
    Retorne **apenas** o JSON válido puro, sem blocos de formatação markdown tipo ```json no começo e fim, sem texto de introdução ou conclusão.
    {schema_json}
    """
    
    prompt = PromptTemplate(
        input_variables=["tema", "observacoes", "condicao_visual", "contexto", "schema_json"],
        template=template
    )

    formatted_prompt = prompt.format(
        tema=tema,
        observacoes=observacoes if observacoes.strip() else "Nenhuma observação extra fornecida. Siga com o planejamento criativo livre.",
        condicao_visual=condicao_visual,
        contexto=contexto_pdf,
        schema_json=parser
    )

    response = llm.invoke(formatted_prompt)
    
    # Limpeza básica caso o LLM insista em mandar Markdown
    raw_content = response.content.strip()
    if raw_content.startswith("```json"):
        raw_content = raw_content[7:]
    if raw_content.endswith("```"):
        raw_content = raw_content[:-3]
        
    return raw_content.strip()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        tema_arg = " ".join(sys.argv[1:])
        print(f"Gerando plano para o tema: {tema_arg}\n")
        resultado_json = gerar_plano_de_aula(tema_arg)
        print(resultado_json)
    else:
        print("Uso: python tools/lesson_generator.py 'Tema da aula'")
