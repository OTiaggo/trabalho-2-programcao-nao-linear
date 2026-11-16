# AGENTS.md — Segundo trabalho de Programação Não Linear

## 1. Finalidade e estado atual

Este arquivo orienta a continuidade do **segundo trabalho** de Programação Não Linear. Leia-o antes de implementar, pesquisar ou redigir entregáveis. Atualização inicial: **16/11/2026**.

**Estado comprovado:** as três páginas de `PNL_projeto_segundo_20262.pdf` foram lidas, com extração de texto e conferência visual. As instruções herdadas do primeiro trabalho foram substituídas. Ainda não foram selecionados trabalhos dos EU/UFC, implementados métodos ou executados experimentos deste segundo trabalho.

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
- Modalidade de referência: **graduação individual**, conforme o histórico informado; não há confirmação de mudança.
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

Para a modalidade atual, produzir **exatamente três fichas**, com **no máximo uma página cada**, e trabalhar com três problemas. O histórico registra **TP 1, TP 8 e TP 15** como os problemas atribuídos. Mantê-los como referência de continuidade, conforme a recomendação do novo PDF; o catálogo e a captura do sorteio anterior não estão neste diretório.

Pendências que não podem ser preenchidas por suposição:

- Variante Quase-Newton: **não informada** (BFGS, DFP ou SR1 com salvaguarda).
- Variante de Gradiente Conjugado não linear: **não informada** (HS, PR ou FR).
- Três trabalhos oficiais dos EU/UFC: **não selecionados**.
- Busca linear a reutilizar, parâmetros, organização do código e formato do relatório: **não definidos**.

Não escolher variantes arbitrariamente como se fossem sorteadas. Enquanto essa informação faltar, avançar na pesquisa, nas funções e na estrutura comum dos experimentos.

## 4. Parte 1 — Pesquisa aplicada nos EU/UFC

Pesquisar nos **anais oficiais dos Encontros Universitários da UFC**, incluindo eventos de iniciação científica, docência e pós-graduação. Selecionar três trabalhos com evidências suficientes para a análise.

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
2. **Uma variante Quase-Newton sorteada:** BFGS, DFP ou SR1 com salvaguarda.
3. **Uma variante de Gradiente Conjugado não linear sorteada:** Hestenes–Stiefel (HS), Polak–Ribière (PR) ou Fletcher–Reeves (FR).

Usar buscas lineares implementadas na primeira atividade, sem caixas-pretas de busca 1D. O histórico menciona Fibonacci, interpolação quadrática/cúbica e Goldstein; localizar e revisar as rotinas. O novo PDF não exige cruzar cada algoritmo com as três buscas anteriores.

### Matriz de experimentos

Para cada problema e método, executar independentemente a partir de A (ponto padrão) e B (reflexão de todas as coordenadas). Se A for o vetor zero, usar B igual ao vetor de componentes −1.

| Problema histórico | Ponto A | Ponto B |
|---|---|---|
| TP 1 | $(8,9)^T$ | $(-8,-9)^T$ |
| TP 8 | $(0,0)^T$ | $(-1,-1)^T$ |
| TP 15 | $(-1{,}2;1{,}0)^T$ | $(1{,}2;-1{,}0)^T$ |

Total previsto: **3 problemas × 3 métodos × 2 pontos = 18 execuções completas**, antes de testes extras. Não encadear execuções nem usar o ponto final de um método como inicial de outro. Documentar parâmetros comparáveis e diferenças necessárias.

### Parada e interpretação

O PDF sugere verificar a cada iteração, com ligação por **“ou”**:

$$\|\nabla f(x_k)\|\leq10^{-5},\qquad
\frac{|f(x_{k+1})-f(x_k)|}{\max(1,|f(x_k)|)}\leq10^{-7},\qquad k\geq1000.$$

Essas tolerâncias são sugestões; documentar as adotadas. Registrar separadamente parada por gradiente, variação do objetivo, limite de iterações, falha de busca ou valores não finitos. Limite de iterações não prova convergência; pequena variação pode indicar estagnação. Gradiente pequeno não garante mínimo local ou global.

Se o ponto inicial tiver gradiente nulo, registrar a execução e a parada sem fabricar passos nem omitir o caso.

### Questão central do relatório

Explicar por que, no problema convexo G1, os dois pontos iniciais levam ao mesmo minimizador, usando as propriedades da função específica. Não atribuir unicidade a toda função convexa.

Nos problemas G2/G3, investigar se a reflexão alterou mínimo, quadrante, bacia de atração ou número de iterações; verificar evidências de sela ou estagnação. Comparar condicionamento, ziguezague do gradiente e desempenho das variantes. Não fabricar efeitos que não apareceram nos resultados.

## 6. Funções herdadas e cuidados matemáticos

As fórmulas seguintes vêm do contexto anterior, não de um catálogo incluído no novo PDF. Conferi-las com o catálogo quando disponível e validar a implementação atual.

### TP 1

$$f_1(x)=4(x_1-5)^2+(x_2-6)^2,$$
$$\nabla f_1=(8(x_1-5),2(x_2-6))^T,\qquad \nabla^2 f_1=\operatorname{diag}(8,2).$$

Mínimo único de referência: $(5,6)^T$, valor zero. Usar para conferir os métodos.

### TP 8

$$f_8(x)=[1{,}5-x_1(1-x_2)]^2+[2{,}25-x_1(1-x_2^2)]^2+[2{,}625-x_1(1-x_2^3)]^2.$$

O histórico alerta que Newton clássico não fornece descida estrita no ponto padrão. Isso não exige incluir Newton clássico neste segundo trabalho.

### TP 15

$$f_{15}(x)=\left[10(x_1-x_2^2)^2+(x_1-1)^2\right]^{1/4}.$$

A potência se aplica à soma inteira. A função não é diferenciável em $(1,1)^T$ e $(1,-1)^T$, onde a expressão interna se anula. Não avaliar derivadas com potências negativas de zero nem interpretar falha de derivada como gradiente zero. Registrar e analisar eventual chegada à região singular, especialmente agora que serão executadas trajetórias completas.

Não declarar derivadas ou resultados anteriores validados neste ambiente. Conferir gradientes por diferenças finitas em pontos regulares e usar verificações analíticas quando possível.

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

1. **Resumos dos EU/UFC:** três na modalidade atual, cada um limitado a uma página e com os campos da seção 4.
2. **Relatório dos experimentos:** analisar sequências de pontos dos três métodos a partir de A/B e responder à questão da reflexão.
3. **Manual dentro do relatório:** dependências, entrada dos dados/parâmetros, execução e leitura de saídas/status. Um README isolado não basta.
4. **Matriz de responsabilidades:** o novo enunciado espera preenchimento detalhado. Para trabalho individual, identificar tarefas efetivamente realizadas por Tiago e distinguir o apoio da IA. A remoção dessa seção no relatório anterior não dispensa o requisito atual.
5. **Apêndice de IA:** resumo dos prompts e pelo menos uma situação real de erro produzido pela IA, com identificação e correção fundamentadas.
6. **Código-fonte comentado:** três métodos multidimensionais e buscas reutilizadas, sem caixas-pretas de busca 1D.

Não presumir LaTeX, limite global de páginas, formato de pacote ou canal de envio não especificados. Se houver PDF, compilar e conferir a diagramação, inclusive o teto das fichas, antes de marcar como pronto.

## 9. Registro contínuo de prompts e correções

Manter registros específicos deste segundo trabalho:

| Arquivo | Finalidade |
|---|---|
| `resumo de prompts.md` | Pedidos relevantes à IA, finalidade, saída e validação |
| `auditoria critica de erros.md` | Incidentes reais, diagnóstico, correção e evidência posterior |
| `no que a IA ajudou.md` | Contribuições efetivas da IA e seus limites |

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

Não tratar arquivos planejados como existentes. Atualizar caminhos, decisões e andamento apenas com evidências, preservando as instruções posteriores do estudante.

- [x] Ler as três páginas e conferir visualmente o novo enunciado.
- [x] Refatorar as instruções para o segundo trabalho.
- [x] Iniciar registros de prompts, contribuições e auditoria.
- [ ] Obter o resultado do sorteio das variantes.
- [ ] Conferir catálogo e localizar código reutilizável da primeira atividade.
- [ ] Selecionar três trabalhos oficiais dos EU/UFC e redigir as fichas.
- [ ] Definir organização do código, busca linear e parâmetros.
- [ ] Implementar e validar os três métodos e as funções.
- [ ] Executar as 18 combinações, preservando trajetórias completas.
- [ ] Analisar reflexão, bacias, condicionamento, convergência e falhas.
- [ ] Redigir relatório, manual, matriz de responsabilidades e apêndice de IA.
- [ ] Verificar resultados e diagramação, incluindo o limite das fichas.
- [ ] Conferir canal, horário e requisitos práticos de envio.

Continuar pelas pendências sem reiniciar o primeiro trabalho, escolher variantes sorteadas por conta própria ou declarar conclusões sem evidência.
