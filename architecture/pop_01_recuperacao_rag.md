# POP 01: Recuperação de Conhecimento (RAG)

## Objetivo
Garantir que o Agente consulte a base bibliográfica validada (`knowledge_base/`) antes de tentar gerar qualquer experimento usando apenas o treinamento nativo do LLM.

## Gatilho
O usuário (Professor) envia um Payload de Entrada contendo:
- `tema_aula` (ex: "Cinética Química")

## Passos (Lógica Determinística)
1. **Extração de Palavras-Chave:** A Camada de Navegação extrai as palavras-chave do `tema_aula`.
2. **Busca Vetorial/Semântica na Base:**
   - A Ferramenta RAG lê o conteúdo dos PDEs em `knowledge_base/`.
   - Busca trechos que cruzem o `tema_aula` + termos de inclusão (ex: "cego", "deficiência visual", "tato", "som", "textura", "inclusivo").
3. **Seleção de Contexto:** 
   - Se encontrar experimentos inclusivos nos artigos, extrai esse bloco de texto.
   - Se *não* encontrar experimentos inclusivos para o tema *específico*, extrai regras gerais de adaptação contidas nos manuais para aplicar em um experimento clássico.
4. **Passagem para o Gerador:** O bloco de texto validado é anexado ao prompt que será enviado ao modelo de linguagem responsável por escrever o Plano de Aula.

## Casos de Borda (Edge Cases)
- **Falha de Leitura do PDF:** Se um PDF corromper, logar o erro no console e usar os PDFs restantes.
- **Nenhum resultado na Base:** O Agente deve alertar o professor: *"Não encontrei literatura validada nesta base para este tema. Criei uma adaptação teórica baseada nas diretrizes de segurança, mas requer revisão rigorosa."*
