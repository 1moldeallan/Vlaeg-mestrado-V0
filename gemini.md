# Constituição do Projeto (gemini.md)

## Regras Comportamentais
- **Estrela Guia:** Desenvolver um agente construtor de Planos de Aula de Química voltados para inclusão de alunos cegos.
- **Tom e Abordagem:** O agente deve ter um tom didático, empático e focado na segurança de laboratório.
- **Proibição Estrita:** O agente *nunca* deve sugerir experimentos ou avaliações que dependam exclusivamente da visão (ex: "observe a mudança de cor", "veja a precipitação" sem alteração tátil/térmica/sonora). A validação química do experimento deve ser sempre multi-sensorial (Tato, Olfato, Audição, Lógica de reações exotérmicas/endotérmicas, efervescência sonora, etc).
- **Fonte da Verdade:** O agente deve basear-se (via RAG) nos arquivos PDF/Texto e manuais fornecidos no projeto para extrair métodos experimentalmente validados por pesquisadores de ensino inclusivo.

## Esquemas de Dados (Schemas)

### 1. Payload de Entrada (Input do Professor)
```json
{
  "tema_aula": "string (ex: Ligações Químicas, Cinética, Ácidos e Bases)",
  "tempo_duracao_minutos": "number (opcional)",
  "materiais_disponiveis": "array_of_strings (opcional)"
}
```

### 2. Payload de Saída (Plano de Aula Gerado)
```json
{
  "tema": "string",
  "objetivo_inclusivo": "string",
  "Roteiro_Experimento": {
    "titulo": "string",
    "materiais": ["string"],
    "passo_a_passo": ["string"],
    "adaptacao_deficiencia_visual": "string (Como o aluno cego interage? Audição? Tato? Olfato?)"
  },
  "dicas_seguranca": ["string"]
}
```

## Invariantes Arquiteturais
- Arquitetura de 3 camadas (A.N.T. - Arquitetura, Navegação, Ferramentas).
- A base de conhecimento (artigos validados) deve ser consultada preferencialmente antes de qualquer geração criativa de experimento.
- Lógica de negócios determinística (Camada 3). POPs atualizados antes do código.
