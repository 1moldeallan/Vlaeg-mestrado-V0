# POP 02: Geração de Experimento Inclusivo

## Objetivo
Processar o contexto recuperado pelo POP 01 e gerar um Plano de Aula (Payload de Saída) que seja rigorosamente seguro e acessível para alunos com deficiência visual.

## 1. Restrições de Indicadores de Fenômenos
- **Proibição de Desfechos Estritamente Visuais:** É proibido que a conclusão do experimento dependa apenas de mudanças de cor (titulações colorimétricas comuns, testes de chama, indicadores de pH como fenolftaleína).
- **Substituição:** Uso de sensores de pH que convertem o valor em sinal sonoro ou o uso de indicadores naturais com odores fortes.
- **Proibição de Precipitados "Intocáveis":** Se a formação de um sólido (precipitado) ocorre em solução ácida ou corrosiva que impeça o toque, ela é considerada uma barreira.
- **Substituição:** Reações que geram precipitados em meios neutros e seguros, permitindo que o aluno filtre a solução e sinta a textura do sólido retido no papel de filtro.

## 2. Restrições de Equipamentos e Vidrarias
- **Proibição de Vidraria Lisa:** É proibido o uso de béqueres, provetas ou pipetas sem marcações em alto-relevo (feitas com cola quente, fita técnica ou entalhe).
- **Proibição de Menisco Visual:** Experimentos que exigem a leitura da "barriga" do líquido (menisco) em nível de olho são inacessíveis.
- **Substituição:** Uso de seringas com limitadores físicos no êmbolo (travas de plástico ou metal) que travam o movimento ao atingir o volume exato (ex: 10ml).

## 3. Restrições de Segurança e Espaço
- **Proibição de Fontes de Calor com Chama Exposta:** O bico de Bunsen deve ser evitado ou proibido se não houver um anteparo físico que delimite a área de risco.
- **Substituição:** Mantas aquecedoras ou chapas elétricas, que são mais estáveis e fáceis de localizar espacialmente sem o risco de uma chama invisível (para o aluno) oscilando com o vento.
- **Proibição de Bancadas "Abertas":** Não se deve permitir que o experimento ocorra solto sobre a mesa.
- **Restrição Técnica:** O uso de uma bandeja de contenção com bordas altas é obrigatório. Ela delimita o "mundo" do aluno e impede que reagentes derramados alcancem suas roupas ou materiais de escrita (Braille/Reglete).

## 4. Restrições de Manuseio de Reagentes
- **Proibição de Reagentes Voláteis Inodoros e Perigosos:** Gases tóxicos que não possuem cheiro característico são extremamente perigosos, pois o aluno perde a principal via de alerta (o olfato).
- **Proibição de Transferência por "Olhômetro":** Qualquer etapa que diga "adicione até que a solução fique turva" deve ser substituída por medidas exatas ou por uma mudança sensorial perceptível (como a efervescência que pode ser ouvida).

## Formato de Saída Obrigatório
O resultado gerado pelo LLM deve ser forçado ao Schema JSON definido no `gemini.md` (Payload de Saída), contendo obrigatoriamente a chave `"adaptacao_deficiencia_visual"` detalhando *exatamente* qual sentido (além da visão) o aluno usará para constatar o fenômeno químico.
