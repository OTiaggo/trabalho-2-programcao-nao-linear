# Registro de prompts — Segundo trabalho de PNL

## P001 — 16/11/2026 — Adaptação das instruções

- **Solicitação (resumo fiel):** ler o enunciado do segundo trabalho e refatorar o `AGENTS.md` herdado do primeiro, mantendo a estratégia de documentar prompts e correções.
- **Finalidade:** estabelecer contexto, requisitos e pendências do novo projeto.
- **Saída:** `AGENTS.md` reestruturado e início dos três registros de auditoria/contribuições.
- **Validação:** leitura textual e visual das três páginas; requisitos confrontados com as novas instruções.
- **Limites:** nenhum algoritmo implementado ou experimento executado; variantes sorteadas e trabalhos EU/UFC ainda não definidos.

Nos próximos registros, incluir identificador, data, pedido literal ou resumo identificado, finalidade, arquivos afetados e validação realizada/pendente.

## P002 — 16/11/2026 — Incorporação das atribuições

- **Solicitação (resumo fiel):** o estudante informou que adicionou os arquivos `atribuicao dos metodos.txt` e `atribuicao dos problemas de teste.txt`.
- **Finalidade:** atualizar o contexto com as atribuições fornecidas, substituindo referências herdadas.
- **Evidências:** saída de problemas indica graduação em dupla (564988 e 568044), TP 3/G1, TP 14/G2, TP 9/G2 e TP 16/G3; buscas anteriores: Seção Áurea, Falsa Posição e Goldstein.
- **Validação dos métodos:** o arquivo contém o script, sem saída impressa. Reprodução local com `random.Random(568044+564988)` e duas escolhas nas listas na ordem original retornou BFGS e FR. Não houve alteração de matrículas nem novo critério de seleção.
- **Saída:** atualização de `AGENTS.md`, deste registro e de `no que a IA ajudou.md`; cinco fichas e 24 execuções previstas. Arquivos de atribuição e notebook preservados.
- **Limites:** catálogo, fórmulas, pontos iniciais, código reutilizável e nome do segundo integrante ainda pendentes. Nenhum experimento executado nesta atualização. A mudança de contexto não foi classificada como erro algorítmico da IA.

## P003 — 16/11/2026 — Resolver a Parte 2; interrupção a pedido

- **Solicitação literal:** “resolva a parte 2 do trabalho [PNL_projeto_segundo_20262.pdf](PNL_projeto_segundo_20262.pdf)”.
- **Complemento literal:** “norberto frota - 568044”.
- **Finalidade:** implementar gradiente, BFGS e FR, executar pontos A/B, analisar resultados e preparar código, notebook e relatório com manual e auditoria.
- **Realizado:** catálogo recuperado e conferido; Goldstein reutilizada com identidade sintática verificada; código e testes criados; 24 ensaios principais e 24 de refinamento executados com trajetórias preservadas; erro E001 reproduzido, corrigido e testado.
- **Arquivos afetados:** scripts Python, requirements.txt, .gitignore, fontes/, resultados/, AGENTS.md e registros. `preparar_entrega.py` contém rascunho ainda não executado do notebook/relatório.
- **Validação:** diferenças finitas de gradientes/Hessianas em seis pontos por problema; testes do quadrático, gradiente nulo, curvatura/secante BFGS, reflexão, domínio e busca limitada; cada passo dos ensaios confrontado com as cotas de Goldstein. Após E001, testes passaram, mas os ensaios completos ainda não foram repetidos com a última versão.
- **Interrupção literal:** “vou precisar interromper a execução e continuar mais tarde”. Trabalho interrompido, com ponto de retomada em AGENTS.md. PDF e notebook executado ainda não entregues. Atribuição pessoal das tarefas permanece pendente de informação dos estudantes.

## P004 — 16/11/2026 — Retomada e finalização da Parte 2

- **Solicitação literal:** “continue”.
- **Finalidade:** retomar as verificações e concluir os entregáveis técnicos da Parte 2.
- **Saída:** notebook executado, relatório PDF de 12 páginas, README com reprodução, verificador final e registros atualizados. Ajustados os literais de fórmulas e a quebra de linha do gerador antes da execução do notebook.
- **Arquivos afetados:** `preparar_entrega.py`, `parte 2.ipynb`, `output/pdf/relatorio_parte2.pdf`, `README.md`, `verificar_entrega.py`, resultados, AGENTS.md e os três registros de auditoria/contribuições.
- **Validação:** 24 ensaios principais e 24 adicionais repetidos com a correção E001; mesmos resultados; nove células do notebook executadas sem erro; verificação de trajetórias, Goldstein, simetria, hashes, fontes e estrutura; todas as 12 páginas do PDF renderizadas e conferidas visualmente.
- **Limites:** quatro ensaios adicionais do gradiente atingem 20.000 passos sem satisfazer a tolerância e permanecem inconclusivos. Divisão real de tarefas humanas não informada; não foi inventada. Parte 1 fora do escopo deste pedido.

## P005 — 17/11/2026 — Organização do repositório

- **Solicitação literal:** “organize o repositorio”.
- **Finalidade:** agrupar código, fontes e registros para facilitar navegação e execução.
- **Saída:** scripts em `codigo/`, atribuições em `fontes/atribuicoes/`, enunciado em `fontes/` e registros em `documentacao/auditoria/`. README e AGENTS descrevem os caminhos atuais. Notebook e relatório atualizados com os comandos correspondentes.
- **Validação:** ensaios repetidos sem alterar matemática ou parâmetros; notebook reexecutado, rastreabilidade/hashes e integração conferidos; PDF renderizado novamente para conferir a diagramação após atualizar os caminhos.
- **Preservação:** resultados, originais e evidências E001 mantidos; nomes históricos e datas originais dos registros preservados.

## P006 — 17/11/2026 — Nome completo do estudante

- **Solicitação literal:** “meu nome completo é tiago oliveira lima”.
- **Finalidade:** atualizar a identificação para Tiago Oliveira Lima.
- **Saída:** nome completo no README, AGENTS, identificação do notebook e capa, matriz, rodapés e metadados do relatório; gerador atualizado para preservar a correção em futuras versões.
- **Validação:** PDF regenerado e conferido; notebook manteve as células de código e suas saídas executadas. Nenhuma fórmula, parâmetro ou resultado numérico alterado.
