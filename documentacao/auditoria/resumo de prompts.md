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
- **Complemento (resumo com identificação corrigida em P007):** nome e matrícula do colega, Noberto Frota Oliveira Nogueira (568044).
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

## P007 — 17/11/2026 — Correção do nome do colega

- **Solicitação (resumo fiel):** corrigir em todo o projeto o nome do colega para Noberto Frota Oliveira Nogueira.
- **Finalidade:** usar o nome completo confirmado pelo usuário, mantendo a matrícula 568044.
- **Saída:** README, AGENTS, notebook, gerador, verificador e relatório atualizados. A identificação anterior em P003 foi convertida em resumo com referência a esta correção, sem apresentá-la como citação literal.
- **Validação:** conferência das ocorrências, do PDF regenerado e da preservação das células de código e saídas executadas do notebook; resultados numéricos preservados.

## P008 — 17/11/2026 — Distribuição de trabalhos declarada pelo usuário

- **Solicitação (resumo fiel):** incorporar a distribuição enviada pelo usuário, com a conclusão “essa foi a distribuição dos trabalhos”.
- **Tiago Oliveira Lima (564988):** Parte 1: seleção dos trabalhos nos Encontros Universitários e elaboração dos resumos 1, 3 e 5. Parte 2: definição do escopo junto ao assistente (P001–P003); conferência das derivadas analíticas do TP3 e do TP9 contra o catálogo da primeira atividade; conferência da busca de Goldstein recuperada da Atividade 1 e de seus parâmetros (c = 0,1, α inicial = 1); análise dos resultados do TP3 e do TP9 (simetria das trajetórias, ziguezague do gradiente, vale estreito); execução dos comandos do Manual de Uso para checar a reprodutibilidade.
- **Noberto Frota Oliveira Nogueira (568044):** Parte 1: seleção dos trabalhos nos Encontros Universitários e elaboração dos resumos 2 e 4. Parte 2: conferência da atribuição de problemas e métodos (script de sorteio, semente 1133032) e dos pontos A/B; conferência das derivadas do TP14 e do TP16 e das referências analíticas (quatro mínimos do TP14, convexidade e Hessiana singular do TP16); revisão das salvaguardas do BFGS (condição de curvatura) e dos reinícios de Fletcher–Reeves; análise dos resultados do TP14 e do TP16 e redação da resposta à questão investigativa sobre bacias de atração; revisão do erro E001 e leitura final do relatório.
- **Finalidade e saída:** completar a matriz de responsabilidades do notebook e do relatório, atualizar README e AGENTS e manter o apoio da IA identificado separadamente. O nome completo confirmado em P007 foi mantido.
- **Validação:** conferência da correspondência com a declaração, preservação das células de código e saídas executadas do notebook, verificação integrada e revisão do PDF regenerado.
- **Limite:** as atividades humanas são registradas conforme declaração do usuário. A declaração não acrescenta as fichas da Parte 1 aos arquivos da entrega.

## P009 — 17/11/2026 — Commit e push

- **Solicitação literal:** “faça commit e push”.
- **Finalidade:** versionar e enviar a atualização da matriz de responsabilidades e seus documentos derivados ao remoto configurado.
- **Validação anterior ao envio:** verificação integrada aprovada em P008, células de código e saídas do notebook preservadas e PDF de 12 páginas conferido; revisão do diff e da situação do remoto antes da publicação.
