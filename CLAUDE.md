# S.I.N.A.P.S.E — Laboratório Inclusivo

Agente de IA que gera **planos de aula práticos de Química** acessíveis para alunos com deficiência
visual (cegos ou de baixa visão), garantindo que a aula seja **a mesma para toda a turma, sem
isolamento**. Projeto de Dissertação de Mestrado (CapUERJ).

## Como funciona (visão geral)

1. O professor escolhe um **tema de Química** e, opcionalmente, escreve observações, além de definir
   a **condição visual do aluno** (CEGO / BAIXA VISÃO) na interface Streamlit.
2. O sistema faz **RAG**: busca trechos relevantes na base científica (PDFs em `knowledge_base/`,
   indexados no ChromaDB) para fundamentar a resposta.
3. O LLM (**Google Gemini**) recebe o contexto RAG + regras rígidas de acessibilidade e retorna um
   **plano de aula estruturado em JSON**.
4. A interface exibe o plano de forma amigável e permite **baixar em PDF**.

## Arquitetura / arquivos principais

- `app.py` — interface **Streamlit** (UI, tema CSS, orquestra a geração e a exibição). É o ponto de entrada.
- `tools/lesson_generator.py` — monta o prompt, injeta o contexto RAG, chama o Gemini e devolve o
  JSON do plano (string). Contém o schema esperado e as **regras absolutas de acessibilidade**.
- `tools/rag_retriever.py` — RAG. `build_vector_store()` indexa os PDFs no ChromaDB;
  `retrieve_context(query, k=4)` recupera os trechos relevantes.
- `tools/pdf_exporter.py` — converte o plano JSON em **PDF** (fpdf2).
- `tools/test_llm_connection.py` — teste de conexão com o Gemini.
- `knowledge_base/` — PDFs científicos que alimentam o RAG.
- `vector_db/chroma_db/` — banco vetorial ChromaDB persistido (commitado no repo).
- `.env` — contém `GEMINI_API_KEY` (NÃO versionado, está no .gitignore).

## Como rodar

```bash
# 1. Ativar o ambiente virtual
source .venv/bin/activate

# 2. (Primeira vez ou ao trocar PDFs) construir o banco vetorial RAG
python tools/rag_retriever.py --build

# 3. Rodar o app
streamlit run app.py
```

Gerar um plano via linha de comando (sem UI):
```bash
python tools/lesson_generator.py "Tabela periódica"
```

## Modelos usados

- **Geração de texto:** `gemini-2.5-flash` (temperature 0.2 — segue rigorosamente as regras).
- **Embeddings (RAG):** `models/gemini-embedding-001`.
- Coleção ChromaDB: `quimica_inclusiva`.

## Schema do plano (saída JSON)

```json
{
  "tema": "string",
  "objetivo_inclusivo": "string",
  "Roteiro_Experimento": {
    "titulo": "string",
    "materiais": ["string"],
    "passo_a_passo": ["string"],
    "adaptacao_deficiencia_visual": "string"
  },
  "dicas_seguranca": ["string"]
}
```

O LLM deve retornar **apenas JSON puro** (sem markdown). `lesson_generator.py` ainda recorta o bloco
`{...}` por segurança caso o modelo adicione texto extra.

## Regras de acessibilidade (o coração do projeto)

O prompt impõe restrições que NÃO devem ser enfraquecidas sem necessidade — são o objetivo da
dissertação:

1. **Proibido desfechos puramente visuais** (não depender só de mudança de cor / precipitado intocável).
2. **Substituição sensorial obrigatória** — trocar o visual por tato (variação térmica segura),
   audição (efervescência) ou olfato seguro.
3. **Sem alinhamento de menisco** — usar seringas com limitadores.
4. **Sem chama aberta solta** (preferir chapa elétrica); experimento do aluno cego dentro de
   **bandeja de contenção**.
5. **Sem "olhômetro"** — medidas padronizadas de forma tátil/sonora.

## Convenções

- O código e os comentários estão em **português**. Mantenha esse padrão.
- Mensagens de commit seguem **Conventional Commits** (`fix:`, `style:`, `feat:` ...).
- O schema JSON é injetado como **string hardcoded** no prompt (não via Pydantic `.schema_json()`),
  porque o LLM tende a omitir a chave `adaptacao_deficiencia_visual` quando recebe os `$refs` do
  Pydantic. Não reverter isso.
- O CSS da UI é injetado inline em `app.py` (tema claro "SaaS", fonte acessível *Atkinson Hyperlegible*).

## Notas

- "POP" e "V.L.A.E.G." nos comentários/prompt são nomes internos do protocolo pedagógico do projeto.
- Os arquivos `test_pdf*.py` na raiz e `out.txt`, `findings.md`, `progress.md`, `task_plan.md` são
  artefatos de desenvolvimento/anotações, não fazem parte do fluxo de produção.
