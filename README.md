# Segunda atividade computacional de Programação Não Linear

Parte 2: gradiente clássico, BFGS e Fletcher–Reeves (FR), com Goldstein
reutilizada da primeira atividade. Tiago Oliveira Lima (564988) e Noberto Frota Oliveira Nogueira (568044).

## Entregáveis

- `parte 2.ipynb`: explicações, execução das 24 combinações, tabelas, amostras
  das sequências, gráficos e interpretação dos ensaios adicionais.
- `output/pdf/relatorio_parte2.pdf`: relatório com derivadas, análise da
  reflexão, resultados, manual de uso, matriz de responsabilidades e auditoria.
- `codigo/otimizacao.py`: funções, gradientes, Hessianas de diagnóstico e os três
  métodos multidimensionais explícitos.
- `codigo/busca_linear.py`: rotina Goldstein recuperada, com as duas desigualdades.
- `resultados/parte2/`: 24 ensaios principais, gráficos, CSV e sequências.
- `resultados/parte2_refinamento/`: 24 ensaios independentes com parada por
  gradiente ou limite de 20.000 passos.
- `fontes/`: catálogo original e evidência da reutilização da busca.
- `resultados/auditoria/`: evidências do erro real E001 e sua correção.
- `fontes/atribuicoes/`: arquivos originais dos sorteios fornecidos pela dupla.
- `documentacao/auditoria/`: registros de prompts, erros e contribuições da IA.

## Organização

```text
.
├── AGENTS.md                    # instruções e continuidade
├── README.md                    # navegação e execução
├── requirements.txt             # dependências
├── parte 2.ipynb                # notebook executado
├── codigo/                      # implementações, testes e geradores
├── fontes/                      # enunciado, catálogo e atribuições
├── documentacao/auditoria/       # registros contínuos da IA
├── resultados/                  # dados, gráficos e verificações
└── output/pdf/                  # relatório final
```

Execute os comandos pela raiz do repositório. `.venv/`, `tmp/` e caches
são arquivos locais ignorados pelo Git.

Os arquivos grandes de trajetória são compactados sem perda em `.json.gz`.
A Parte 1 (pesquisa EU/UFC) não está incluída nos entregáveis desta pasta.
A matriz no notebook e no relatório registra a distribuição de tarefas das
Partes 1 e 2 declarada pelo usuário em 17/11/2026, distinguindo o apoio da IA.

## Executar em PowerShell

Na raiz do repositório, prepare o ambiente com Python 3.13 na primeira vez.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
```

Com o ambiente pronto, execute todos os experimentos com um comando.

```powershell
.venv/Scripts/python codigo/rodar_experimentos.py
```

O comando verifica os métodos e roda os 24 ensaios principais e os 24 de
refinamento. Consulte `resumo.csv` em `resultados/parte2/` e
`resultados/parte2_refinamento/`. Os gráficos ficam em `resultados/parte2/`.

<details>
<summary>Gerar novamente o PDF e o notebook (opcional)</summary>

O primeiro comando recria o PDF e o notebook sem saídas. Os demais executam
o notebook e verificam a entrega.

```powershell
.venv/Scripts/python codigo/preparar_entrega.py
.venv/Scripts/python -m ipykernel install --prefix .venv --name pnl --display-name 'Python (PNL)'
$env:JUPYTER_PATH = (Resolve-Path .venv/share/jupyter).Path
.venv/Scripts/python -c "import nbformat; from nbclient import NotebookClient; p='parte 2.ipynb'; n=nbformat.read(p,as_version=4); NotebookClient(n,timeout=600,kernel_name='pnl').execute(); nbformat.write(n,p)"
.venv/Scripts/python codigo/verificar_entrega.py
```

No Jupyter/VS Code, selecione o interpretador `.venv` e execute todas as
células. As células de refinamento leem os resultados adicionais já gerados.
O PDF também contém o manual; este README não o substitui.

</details>

## Configuração e leitura das saídas

`python codigo/executar.py --help` mostra as opções. `--tol-f 0` desativa a parada por
variação. Para mudar funções/pontos, use `PROBLEMAS` em `codigo/otimizacao.py`.
`Parametros` permite ajustar a busca e as salvaguardas por meio da API:

```python
import sys
sys.path.insert(0, 'codigo')
from otimizacao import PROBLEMAS, Parametros, minimizar
r = minimizar(PROBLEMAS['TP9'], 'BFGS', [-1.2, 1.0], Parametros())
print(r['status'], r['x_final'], r['norma_grad_final'])
```

`resumo.csv` tem uma linha por execução. Cada JSON contém `trajetoria`
(todos os pontos e gradientes) e `passos` (direções, alfas, tentativas,
beta de FR, atualizações BFGS, avaliações e salvaguardas). Exemplo:

```python
import gzip, json
with gzip.open('resultados/parte2_refinamento/TP9_Gradiente_A.json.gz',
               'rt', encoding='utf-8') as arquivo:
    resultado = json.load(arquivo)
print(resultado['trajetoria'][-1])
```

`gradiente` significa tolerância atingida; `variacao_objetivo` e
`limite_iteracoes` não certificam convergência. Falhas de busca, valores
não finitos e derivadas indefinidas são registrados separadamente.

No refinamento, BFGS e FR atingem a tolerância em todos os problemas e
pontos. O gradiente clássico atinge o limite no TP9 e TP16, a partir de
A e B. Os resultados não foram alterados para ocultar essa dificuldade.
Goldstein não impõe Wolfe forte; não se presume automaticamente a garantia
clássica de convergência de FR. Consulte a discussão no relatório.
