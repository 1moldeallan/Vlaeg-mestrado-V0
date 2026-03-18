# Plano de Tarefas (task_plan.md)

## Fases
- [x] Protocolo 0: Inicialização
- [x] Fase 1: Visão (Definição de escopo, RAG e Schemas)
- [x] Fase 2: Link (Conexões externas e Base de Conhecimento)
- [x] Fase 3: Arquitetura (POPs e Roteamento)
- [x] Fase 4: Estilo (Interface Web)
- [ ] Fase 5: Gatilho (Implantação)

## Objetivos e Checklists

**Fase 3: Arquitetura (Concluída)**
- [x] Escrever POP Técnico (Procedimento Operacional Padrão) em `architecture/` para a Busca nos Artigos (Retrieval RAG).
- [x] Escrever POP Técnico para a Geração do Plano de Aula (Garantindo regras inclusivas estritas de Não-Visão).
- [x] Validar a lógica do POP com o Professor antes de escrever qualquer código em Python.

**Fase 4: Estilo (Concluída)**
- [x] Construir script básico em `tools/` usando RAG (LangChain ou similar) lendo da `knowledge_base/`.
- [x] Integrar acesso à API validada no `.env` para responder em formato JSON (Payload de Saída).
- [x] Desenvolver a Interface Web simples para o Professor enviar o tema e receber o plano.

