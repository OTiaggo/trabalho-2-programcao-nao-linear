# AGENTS.md — Segundo trabalho de Programação Não Linear

## 1. Finalidade e estado atual

Este arquivo orienta a continuidade do **segundo trabalho** de Programação Não Linear. Leia-o antes de implementar, pesquisar ou redigir entregáveis. Atualização inicial: **16/11/2026**.

**Organização atual (17/11/2026):** scripts em `codigo/`; enunciado em `fontes/PNL_projeto_segundo_20262.pdf`; atribuições em `fontes/atribuicoes/`; registros de prompts, erros e contribuições em `documentacao/auditoria/`. Notebook na raiz, resultados em `resultados/` e relatório em `output/pdf/`. Executar comandos pela raiz: `.venv/Scripts/python codigo/executar.py`, `.venv/Scripts/python codigo/testar.py`, `.venv/Scripts/python codigo/preparar_entrega.py` e `.venv/Scripts/python codigo/verificar_entrega.py`. Referências sem esses prefixos nas seções históricas indicam as localizações anteriores; usar este mapa e o README para os caminhos atuais.

**Estado comprovado em 16/11/2026, após retomada:** Parte 2 implementada e verificada; 24 ensaios principais e 24 de refinamento reexecutados com a correção final; notebook executado integralmente; relatório PDF de 12 páginas gerado e todas as páginas conferidas visualmente. Resultados e auditoria preservados. A matriz distingue o apoio da IA, mas a divisão de tarefas humanas depende de declaração dos integrantes. A Parte 1 não foi iniciada.

O estudante solicitou manter a estratégia de registrar prompts, contribuições da IA e erros reais com suas correções. Atualizar esses registros durante o desenvolvimento e incorporá-los ao apêndice de auditoria do relatório.

### Separação entre os trabalhos

- A paleta de cores, a fotografia e o tema histórico de localização pertencem ao primeiro trabalho. A Parte 1 atual é pesquisa nos EU/UFC.
- O segundo trabalho exige otimização multidimensional iterativa. Um único passo e os antigos 27 casos de busca linear não atendem ao novo experimento.
- Resultados, incidentes e pendências de LaTeX anteriores não são resultados ou tarefas concluídas deste projeto.
- O novo PDF recomenda manter os problemas anteriores e reutilizar buscas lineares implementadas na primeira atividade. Localizar e revisar o código antes de declarar reutilização.
- A organização em dois notebooks e as escolhas editoriais do relatório anterior não se transferem automaticamente. A organização atual ainda não foi definida.

## 2. Contexto acadêmico e fonte normativa

- Estudante: Tiago, Bacharelado em Ciência de Dados, Universidade Federal do Ceará.
- Disciplina: Programação Não Linear. Professor: Ricardo Coelho.
- Atividade: **Segunda Atividade Computacional — Resumos e resolução de problemas irrestritos com métodos de otimização multidimensionais**.
- Modalidade confirmada: **graduação em dupla**, Tiago (**564988**) e Norberto Frota (**568044**). O usuário informou “norberto frota - 568044”; a outra matrícula corresponde a Tiago pelo contexto da dupla. Divisão de tarefas humanas ainda não informada.
- Prazo no novo PDF: **17 de novembro de 2026 (terça-feira)**. Horário e canal de envio não informados.
- Comunicação e documentação: português do Brasil.

**Fonte:** `PNL_projeto_segundo_20262.pdf`. Página 1: modalidades e fichas; página 2: métodos, reflexão, tolerâncias sugeridas e auditoria; página 3: entregáveis, prazo e sorteios.

O título principal da página 1 contém “Primeiro Projeto Computacional”, mas cabeçalhos, matriz e conteúdo identificam a segunda atividade. Tratar isso como inconsistência editorial, sem importar os requisitos antigos.

Links transcritos do PDF, ainda não consultados nesta etapa:

- Sorteio de problemas: https://colab.research.google.com/drive/1v0dj9hxsnZ6_IzLa8XD0YEkibY_bldYd?usp=sharing
- Sorteio de métodos: https://colab.research.google.com/drive/1Gac-ap5Fn3Q3I7JcyKaM14k0X0dQZbe4?usp=sharing

Não inventar matrícula nem repetir sorteio sem necessidade. Procurar primeiro um resultado fornecido pelo estudante; se faltar, solicitar o resultado ou os dados necessários para obtê-lo.

## 3. Carga de trabalho e decisões pendentes

| Modalidade no PDF | Trabalhos EU/UFC | Problemas-teste |
|---|---:|---:|
| Graduação individual | 3 | 3 |
| Graduação em dupla | 5 | 4 |
| Pós-graduação individual | 3 | 4 |
| Pós-graduação em dupla | 5 | 5 |

Todas as modalidades comparam gradiente clássico, uma variante Quase-Newton sorteada e uma variante de Gradiente Conjugado sorteada.

Para a modalidade atual, produzir **exatamente cinco fichas**, com **no máximo uma página cada**, e trabalhar com quatro problemas: **TP 3 (G1), TP 14 (G2), TP 9 (G2) e TP 16 (G3)**. Fonte: saída fornecida em `atribuicao dos problemas de teste.txt`. Essas atribuições substituem TP 1, TP 8 e TP 15 do contexto anterior. O trecho sobre duas modelagens práticas pertence à primeira atividade e não acrescenta um entregável à segunda.

O arquivo `atribuicao dos metodos.txt` contém o script configurado com as duas matrículas, sem a saída impressa. A reprodução local das duas chamadas `random.choice`, na ordem do script e com semente **1133032 = 568044 + 564988**, em 16/11/2026, produziu **BFGS** e **Fletcher–Reeves (FR)**. Trata-se da reprodução da configuração fornecida, sem mudar matrículas ou escolher variantes arbitrariamente.

Pendências que não podem ser preenchidas por suposição:

- Fórmulas e pontos iniciais conferidos no catálogo original, preservado em `fontes/catalogo_primeira_atividade.pdf` (pp. 4-6); manifesto e recorte da rotina reutilizada em `fontes/`.
- Cinco trabalhos oficiais dos EU/UFC: **não selecionados**.
- Busca escolhida: **Goldstein**, reutilizada com identidade da árvore sintática em relação à rotina anterior. Código em `otimizacao.py`, `busca_linear.py`, `executar.py` e `testar.py`; preparação da entrega em `preparar_entrega.py`. Relatório em `output/pdf/relatorio_parte2.pdf` e notebook `parte 2.ipynb` gerados e verificados. `verificar_entrega.py` verifica rastreabilidade e integração.

Manter BFGS e FR conforme a configuração fornecida. Não confundir os rótulos e descrições do script com validação das hipóteses matemáticas dos métodos; documentar a convenção e as condições efetivamente adotadas na implementação.

## 4. Parte 1 — Pesquisa aplicada nos EU/UFC

Pesquisar nos **anais oficiais dos Encontros Universitários da UFC**, incluindo eventos de iniciação científica, docência e pós-graduação. Selecionar cinco trabalhos com evidências suficientes para a análise.

Cada ficha, limitada a uma página, deve conter:

1. **Identificação:** título completo, autores, orientador, unidade acadêmica/curso e edição dos EU/UFC.
2. **Problema e modelagem:** contexto real ou científico, variáveis de decisão, objetivo de minimização/maximização e restrições, ou indicação de tratamento irrestrito.
3. **Metodologia:** algoritmo ou software empregado e eventual justificativa dos autores quanto a condicionamento ou dimensionalidade.
4. **Apreciação crítica do estudante:** conexão com PNL, limitações teóricas e possibilidade fundamentada de outro método, como Quase-Newton ou região de confiança.

### Rigor das fontes

- Consultar a publicação original; registrar URL, edição/ano e localização da evidência usada.
- Distinguir afirmações dos autores de interpretações e propostas do estudante.
- Quando um campo não estiver explícito, registrar “não informado na fonte consultada” e buscar material complementar oficial quando necessário.
- Não atribuir aos autores um algoritmo, variável ou função objetivo apenas porque parece adequado. Identificar uma reconstrução matemática do estudante como proposta própria.
- Preferir trabalhos que permitam preencher as fichas com evidências; não inventar informações para completar campos.
- Conferir o limite de página na versão diagramada.

## 5. Parte 2 — Métodos multidimensionais e reflexão

Implementar e comparar iterativamente, até um critério de parada documentado:

1. **Gradiente clássico / descida mais íngreme**, obrigatório como linha de base.
2. **Variante Quase-Newton atribuída: BFGS.**
3. **Variante de Gradiente Conjugado não linear atribuída: Fletcher–Reeves (FR).**

Usar buscas lineares implementadas na primeira atividade, sem caixas-pretas de busca 1D. O resultado fornecido atribui **Seção Áurea, Falsa Posição e condições de Goldstein**; essas informações substituem Fibonacci e interpolação quadrática/cúbica do contexto anterior. Localizar e revisar as rotinas antes de declarar reutilização. A escolha da busca para esta atividade permanece pendente; o novo PDF não exige cruzar cada algoritmo com as três buscas anteriores.

### Matriz de experimentos

Para cada problema e método, executar independentemente a partir de A (ponto padrão) e B (reflexão de todas as coordenadas). Se A for o vetor zero, usar B igual ao vetor de componentes −1.

| Problema atribuído | Ponto A | Ponto B |
|---|---|---|
| TP 3 (G1) | (1;1;1) | (−1;−1;−1) |
| TP 14 (G2) | (0,5;0,5) | (−0,5;−0,5) |
| TP 9 (G2) | (−1,2;1) | (1,2;−1) |
| TP 16 (G3) | (3;−1;0;1) | (−3;1;0;−1) |

Total previsto: **4 problemas × 3 métodos × 2 pontos = 24 execuções completas**, antes de testes extras. Não encadear execuções nem usar o ponto final de um método como inicial de outro. Documentar parâmetros comparáveis e diferenças necessárias.

### Parada e interpretação

O PDF sugere verificar a cada iteração, com ligação por **“ou”**:

$$\|\nabla f(x_k)\|\leq10^{-5},\qquad
\frac{|f(x_{k+1})-f(x_k)|}{\max(1,|f(x_k)|)}\leq10^{-7},\qquad k\geq1000.$$

Essas tolerâncias são sugestões; documentar as adotadas. Registrar separadamente parada por gradiente, variação do objetivo, limite de iterações, falha de busca ou valores não finitos. Limite de iterações não prova convergência; pequena variação pode indicar estagnação. Gradiente pequeno não garante mínimo local ou global.

Se o ponto inicial tiver gradiente nulo, registrar a execução e a parada sem fabricar passos nem omitir o caso.

### Questão central do relatório

Explicar por que, no problema convexo G1, os dois pontos iniciais levam ao mesmo minimizador, usando as propriedades da função específica. Não atribuir unicidade a toda função convexa.

Nos problemas G2/G3, investigar se a reflexão alterou mínimo, quadrante, bacia de atração ou número de iterações; verificar evidências de sela ou estagnação. Comparar condicionamento, ziguezague do gradiente e desempenho das variantes. Não fabricar efeitos que não apareceram nos resultados.

## 6. Funções atribuídas e cuidados matemáticos

Os problemas atuais são **TP 3, TP 14, TP 9 e TP 16**. Fórmulas, dimensões e pontos iniciais conferidos no catálogo original recuperado em `../projetos-curso-ciencia-de-dados/programacao nao linear/trabalho 1/PNL_projeto_primeiro_20262 (1).pdf`, copiado para `fontes/catalogo_primeira_atividade.pdf`. TP14 foi conferido visualmente: 0,1[12+u²+(1+v²)/u²+(u²v²+100)/(u⁴v⁴)], domínio uv≠0. TP16 é soma de potências pares de formas afins, portanto convexo, com mínimo único na origem e Hessiana singular nesse ponto.

As fórmulas de TP 1, TP 8 e TP 15 presentes na versão anterior destas instruções pertenciam ao contexto herdado e foram retiradas da especificação atual. Não transferir seus mínimos, pontos iniciais ou alertas de singularidade para os problemas atribuídos.

Não declarar derivadas ou resultados anteriores validados neste ambiente. Conferir gradientes por diferenças finitas em pontos regulares e usar verificações analíticas quando possível. Identificar domínio e eventual não diferenciabilidade das funções efetivamente atribuídas; não interpretar derivada indefinida como gradiente zero.

## 7. Orientações de implementação e evidência

Estas orientações técnicas não devem ser apresentadas como exigências adicionais do professor:

- Implementar explicitamente as atualizações e a busca utilizada, sem substituir o núcleo por um otimizador pronto.
- Documentar a convenção Quase-Newton (Hessiana ou inversa), inicialização e salvaguardas de curvatura/denominadores.
- Documentar a fórmula de beta do conjugado sorteado e seus reinícios. Não trocar PR por PR+ silenciosamente.
- Verificar descida antes da busca; registrar reinícios, atualizações omitidas e regularizações. Não mascarar mudança de algoritmo.
- Para Goldstein, verificar ambas as desigualdades; não confundir com Armijo. Discutir a compatibilidade entre a busca escolhida e as hipóteses teóricas do método.
- Impor limites e tratar valores não finitos com motivos de falha explícitos.
- Evitar inversão explícita de matrizes quando for possível resolver sistemas lineares.
- Preservar toda a sequência $x_k$, objetivo, norma do gradiente, direção, passo, avaliações, salvaguardas e status, além de parâmetros e ponto inicial.
- Produzir tabela por execução com ponto final, objetivo, norma do gradiente quando definida, iterações, avaliações e motivo de parada.
- Usar gráficos de trajetórias/curvas de nível e evolução do objetivo ou gradiente quando ajudarem a análise; identificar A/B e métodos.
- Verificar o caso quadrático de referência, gradiente inicial nulo e salvaguardas/falhas relevantes. Não declarar sucesso sem evidência de execução.

## 8. Entregáveis

Conforme a página 3 do PDF:

1. **Resumos dos EU/UFC:** cinco na modalidade atual, cada um limitado a uma página e com os campos da seção 4.
2. **Relatório dos experimentos:** analisar sequências de pontos dos três métodos a partir de A/B e responder à questão da reflexão.
3. **Manual dentro do relatório:** dependências, entrada dos dados/parâmetros, execução e leitura de saídas/status. Um README isolado não basta.
4. **Matriz de responsabilidades:** o novo enunciado espera preenchimento detalhado. Para trabalho em dupla, identificar tarefas efetivamente realizadas por cada integrante e distinguir o apoio da IA; não inventar nomes ou divisões de tarefas. A remoção dessa seção no relatório anterior não dispensa o requisito atual.
5. **Apêndice de IA:** resumo dos prompts e pelo menos uma situação real de erro produzido pela IA, com identificação e correção fundamentadas.
6. **Código-fonte comentado:** três métodos multidimensionais e buscas reutilizadas, sem caixas-pretas de busca 1D.

Não presumir LaTeX, limite global de páginas, formato de pacote ou canal de envio não especificados. Se houver PDF, compilar e conferir a diagramação, inclusive o teto das fichas, antes de marcar como pronto.

## 9. Registro contínuo de prompts e correções

Manter registros específicos deste segundo trabalho:

| Arquivo | Finalidade |
|---|---|
| `documentacao/auditoria/resumo de prompts.md` | Pedidos relevantes à IA, finalidade, saída e validação |
| `documentacao/auditoria/auditoria critica de erros.md` | Incidentes reais, diagnóstico, correção e evidência posterior |
| `documentacao/auditoria/no que a IA ajudou.md` | Contribuições efetivas da IA e seus limites |

### Prompts

Registrar identificador, data quando conhecida, solicitação literal ou resumo fiel identificado como resumo, finalidade, arquivos afetados e validação realizada/pendente. Incluir correções solicitadas pelo estudante e mudanças de decisão. Não inventar prompts retroativos nem atribuir ao estudante escolhas feitas pelo agente.

### Erros e correções

Para cada incidente real, registrar:

1. Identificador, contexto e prompt relacionado.
2. Conteúdo errado gerado pela IA e arquivo/local afetado.
3. Como foi identificado: conta analítica, teste, mensagem, confronto com fonte ou revisão do estudante.
4. Causa e correção fundamentada, com explicação analítica quando pertinente.
5. Evidência da validação posterior e limitações ainda abertas.

Não inventar erros para cumprir a exigência. Alertas preventivos não são incidentes; falhas de dependências do ambiente não são erros matemáticos ou de algoritmo. Não transferir incidentes anteriores como se tivessem ocorrido aqui.

Sem um erro elegível documentado, manter a auditoria explicitamente pendente. Correção escrita não equivale a correção validada. Atualizar os registros durante o desenvolvimento e incorporar seu conteúdo ao relatório; os Markdown separados não substituem o apêndice.

## 10. Arquivos e continuidade

Na leitura inicial havia `AGENTS.md`, `PNL_projeto_segundo_20262.pdf`, `README.md` e `.git`. Os três registros da seção 9 foram iniciados nesta refatoração. Notebooks, imagens e relatórios citados pelo AGENTS antigo não estavam presentes.

Em 16/11/2026 foram lidos `atribuicao dos metodos.txt` e `atribuicao dos problemas de teste.txt`. Também foi observada a presença de `parte 2.ipynb`, ainda não inspecionado nesta atualização; sua existência não comprova implementação ou execução validada.

Não tratar arquivos planejados como existentes. Atualizar caminhos, decisões e andamento apenas com evidências, preservando as instruções posteriores do estudante.

- [x] Ler as três páginas e conferir visualmente o novo enunciado.
- [x] Refatorar as instruções para o segundo trabalho.
- [x] Iniciar registros de prompts, contribuições e auditoria.
- [x] Incorporar a atribuição dos problemas e reproduzir as variantes da configuração fornecida (BFGS e FR).
- [x] Conferir catálogo e localizar código reutilizável da primeira atividade.
- [ ] Selecionar cinco trabalhos oficiais dos EU/UFC e redigir as fichas.
- [x] Definir organização do código, busca linear e parâmetros.
- [x] Implementar métodos e funções e executar testes matemáticos, de salvaguardas e revisão final de integração.
- [x] Executar as 24 combinações, preservando trajetórias completas, e 24 ensaios adicionais.
- [x] Analisar reflexão, bacias, condicionamento, convergência e falhas da Parte 2.
- [x] Redigir relatório e manual da Parte 2, matriz com contribuições comprovadas e apêndice de IA.
- [ ] Obter declaração dos integrantes para completar a divisão de tarefas humanas na matriz.
- [x] Verificar resultados, notebook executado e todas as páginas do PDF da Parte 2.
- [ ] Verificar diagramação das fichas da Parte 1, ainda não produzidas.
- [ ] Conferir canal, horário e requisitos práticos de envio.

Continuar pelas pendências sem reiniciar o primeiro trabalho, escolher variantes sorteadas por conta própria ou declarar conclusões sem evidência.

### Histórico da interrupção — superado pela retomada registrada abaixo

- **Autorização:** resolver a Parte 2; usuário solicitou interromper e depois autorizou a retomada com “continue”. As pendências deste bloco descrevem o instante da interrupção; o estado final está no bloco seguinte.
- **Ambiente:** `.venv/Scripts/python.exe`, Python 3.13.18; dependências em `requirements.txt`. PyMuPDF falhou por DLL; usar `pypdf` para texto e `pypdfium2` para renderização. `.venv`, caches e `tmp/` estão no `.gitignore`.
- **Resultados preservados:** `resultados/parte2` (24 principais, tol_grad=1e-5, tol_f=1e-7, máximo 1000) e `resultados/parte2_refinamento` (24 independentes, tol_f=0, máximo 20000). JSON grandes compactados sem perda em `.json.gz`; não omitir esses arquivos ao ler as trajetórias. CSV, gráficos principais e metadados disponíveis.
- **Principais:** 2 paradas por gradiente (BFGS TP14 A/B), 19 por variação e 3 por limite (gradiente TP9 B e TP16 A/B). Refinamento: 20 por gradiente e 4 por limite (gradiente TP9 e TP16, A/B). Limites não significam convergência.
- **Refinamento, iterações A/B:** TP3 gradiente 42/42, BFGS 7/7, FR 22/22; TP14 gradiente 20/20, BFGS 28/28, FR 15/15; TP9 gradiente 20000/20000, BFGS 61/45, FR 442/282; TP16 gradiente 20000/20000, BFGS 24/24, FR 611/611.
- **Auditoria real E001:** tolerância NaN era aceita, fazendo TP3 na origem tentar busca com direção nula. Corrigido com validação de finitude. `testar.py` passou após correção, incluindo 18 rejeições NaN/inf; evidências em `resultados/auditoria/E001_antes.json` e `E001_depois.json`. As 48 execuções foram feitas antes dessa correção de validação, com parâmetros finitos; ainda precisam ser reexecutadas/confrontadas com a versão final e seus hashes atualizados.
- **Entrega ainda incompleta:** `parte 2.ipynb` continua vazio. `preparar_entrega.py` foi escrito mas ainda NÃO executado; PDF ainda não existe. Revisar esse script: o bloco de Markdown com fórmulas deve usar string raw para evitar que `\beta`, `\rho` e `\alpha` virem caracteres de controle. Há texto no rascunho afirmando reverificação das 48 execuções: validar isso antes de gerar/entregar, ou corrigir a afirmação.
- **Próximos passos autorizados após retomada:** revisar código e rascunho; reexecutar ensaios finais sem fabricar convergência; gerar notebook/PDF; executar notebook no kernel da `.venv`; renderizar PDF com pypdfium2 e inspecionar todas as páginas; conferir fontes, hashes, legibilidade e registros; atualizar este estado. Não sobrescrever notebook depois de executá-lo sem executá-lo novamente.
- **PDF skill:** já lido. O marcador obrigatório foi executado com sucesso uma vez via `.venv/Scripts/node.exe C:/Users/DEV-ORBI/.codex/plugins/cache/openai-primary-runtime/pdf/26.1112.11011/skills/pdf/container_tools/mark_artifact_operation_started.mjs --operation-kind create --expected-output-count 1 --output-format pdf`. Não repetir para a mesma operação de criação. Node foi instalado apenas como ferramenta no ambiente virtual, não é dependência do programa de otimização.
- **Referência teórica consultada:** Hager e Zhang, A Survey of Nonlinear Conjugate Gradient Methods, https://people.clas.ufl.edu/hager/files/cg_survey.pdf, §§2 e 4. Goldstein não impõe Wolfe forte; não atribuir suas garantias clássicas a FR automaticamente.
- **Pendências humanas:** divisão real de tarefas por integrante não informada. Manter matriz honesta e pendente de declaração. Não incluir pesquisa da Parte 1 nesta solicitação.
- **Git:** nenhuma operação de commit ou push realizada. Preservar alterações anteriores do usuário e arquivos de atribuição.

### Estado final da Parte 2 — 16/11/2026 (P004)

- **Retomada autorizada:** pedido literal “continue”. Correções do gerador de notebook (strings raw para fórmulas e para a célula que imprime quebras de linha) aplicadas antes de gerar a entrega.
- **Execução final:** ensaio principal e refinamento repetidos com o código final, mesmos valores e motivos de parada. Metadados contêm hashes atuais de `otimizacao.py`, `busca_linear.py`, `executar.py` e `testar.py`.
- **Notebook:** `parte 2.ipynb`, nove células de código executadas no kernel da `.venv`, sem erro. Inclui explicações, tabelas, amostras de todas as sequências, gráficos e leitura do refinamento. Não regenerar pelo script depois de executá-lo sem nova execução.
- **Relatório:** `output/pdf/relatorio_parte2.pdf`, 12 páginas. Todas renderizadas com pypdfium2 e inspecionadas visualmente; sem corte, sobreposição ou página indevidamente vazia. Contém derivadas, geometria, métodos, resultados, manual, matriz e auditoria E001. Evidência da revisão em `resultados/revisao_visual_pdf.json`.
- **Verificação final:** `verificar_entrega.py` passou: 48 trajetórias/aceitações, simetria nos problemas pares, quadrantes visitados no TP14, identidade da Goldstein, hashes, notebook executado e conteúdo do PDF. Registro em `resultados/verificacao_entrega.json`.
- **Reprodução:** README.md contém comandos; dependências fixadas em requirements.txt. O manual também está dentro do PDF. Fontes são locais e não exigem o repositório anterior para executar.
- **Resultados limitados:** gradiente clássico no TP9/TP16 A/B não atinge a tolerância em 20.000 passos, explicitamente reportado. Não modificar parâmetros ou método só para declarar sucesso.
- **Pendências externas à implementação:** integrantes devem informar/revisar a divisão real de tarefas; Parte 1 e canal/horário de envio seguem pendentes. Nenhum commit ou push realizado.

### Organização do repositório — 17/11/2026 (P005)

- Arquivos agrupados em `codigo/`, `fontes/atribuicoes/` e `documentacao/auditoria/`, conforme o mapa no início deste documento. Arquivos originais, sequências e evidências preservados.
- Imports do notebook, leitura de hashes, gerador de entrega, comandos do manual e README adaptados aos novos caminhos. Executar a partir da raiz do projeto.
- Rotinas matemáticas e parâmetros preservados. As execuções foram repetidas para registrar a localização atual do código nos hashes; resultados e motivos de parada permanecem iguais.
- Notebook reexecutado e PDF regenerado para refletir os novos caminhos, com nova conferência visual. Verificação integrada em `codigo/verificar_entrega.py`.
