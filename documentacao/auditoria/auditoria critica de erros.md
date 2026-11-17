# Auditoria crítica de erros — Segundo trabalho de PNL

## E001 — 16/11/2026 — Tolerância NaN aceita indevidamente (P003)

- **Contexto/local:** primeira implementação de `minimizar`, em `otimizacao.py`, validação de parâmetros e parada por gradiente.
- **Erro da IA:** validar tolerância apenas com `tol_grad <= 0` permitia NaN. No TP3, com ponto inicial na origem e `Parametros(tol_grad=float('nan'))`, o programa tentava busca com direção zero e retornava `falha_busca`, em vez de rejeitar o parâmetro inválido antes de avaliar a função.
- **Identificação:** revisão de entradas e execução reproduzível. A saída anterior está integralmente registrada em `resultados/auditoria/E001_antes.json`.
- **Causa:** em aritmética IEEE, `NaN <= 0` é falso; também `norma_grad <= NaN` é falso, inclusive quando o gradiente é exatamente zero. A entrada inválida atravessava a verificação e desativava a parada por gradiente.
- **Correção:** verificar `np.isfinite` em todos os parâmetros reais antes das comparações; verificar limites inteiros e faixas das salvaguardas. Não modificar a fórmula de qualquer método.
- **Validação posterior:** `testar.py` passou após a correção, incluindo NaN, +inf e −inf nos seis parâmetros reais (18 rejeições por ValueError) e o caso estacionário válido sem busca. Evidência em `resultados/auditoria/E001_depois.json`.
- **Limites:** trata-se de bug de validação de entrada, não de derivada incorreta. Os ensaios anteriores usaram parâmetros finitos e não acionaram esse caso; sua repetição com a última versão e atualização dos hashes ainda estavam pendentes quando o usuário pediu interrupção. O conteúdo deve integrar o apêndice do relatório, ainda não gerado.

### Validação final após retomada — P004, 16/11/2026

Os 24 ensaios principais e os 24 de refinamento foram repetidos com a correção E001, preservando os resultados anteriores com parâmetros finitos. `verificar_entrega.py` confirmou os hashes atuais e a consistência das trajetórias e das duas desigualdades de Goldstein. As nove células do notebook foram executadas sem erro. O relato E001 foi incorporado ao apêndice do PDF de 12 páginas, cujas páginas foram renderizadas e inspecionadas visualmente. A evidência anterior incorreta permanece preservada para auditoria, sem ser confundida com a saída corrigida.

## O002 — 17/11/2026 — Ordem de execução durante a organização (P005)

- **Contexto:** ao validar a mudança para `codigo/`, a IA iniciou a execução do notebook enquanto os ensaios adicionais ainda gravavam arquivos de resultados.
- **Falha observada:** a célula que lê o refinamento encontrou um JSON temporariamente incompleto e terminou com `JSONDecodeError`.
- **Causa e correção:** leitura e gravação do mesmo conjunto de arquivos ocorreram simultaneamente. Aguardar o término do produtor e executar novamente o notebook, respeitando a ordem documentada no README, resolveu o problema. Não foi necessário alterar fórmulas ou métodos para corrigi-lo.
- **Validação posterior:** todas as nove células executadas com sucesso após o término das gravações. Este é um incidente operacional de orquestração; não substitui o erro elegível E001 nem indica alteração dos resultados matemáticos.
