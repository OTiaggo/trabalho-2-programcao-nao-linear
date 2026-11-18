# Segunda atividade de Programação Não Linear

Entrega de Tiago Oliveira Lima (564988) e Noberto Frota Oliveira Nogueira (568044).

## Arquivos para avaliação

- `parte1_pnl.pdf`: cinco fichas dos trabalhos dos Encontros Universitários da UFC, uma por página.
- `output/pdf/relatorio_parte2.pdf`: relatório dos experimentos, com manual de execução, matriz de responsabilidades e apêndice sobre o uso de IA.
- `parte 2.ipynb`: notebook com as execuções, tabelas, trajetórias e gráficos.
- `codigo/`: implementação dos métodos multidimensionais e da busca de Goldstein.

Os diretórios `resultados/` e `fontes/` preservam os dados necessários para reproduzir e conferir os experimentos e suas referências. As dependências estão em `requirements.txt`.

## Reprodução

Na raiz do repositório, instale as dependências e execute:

```powershell
python -m pip install -r requirements.txt
python codigo/testar.py
python codigo/verificar_entrega.py
```

O notebook pode ser executado em Jupyter ou VS Code usando o mesmo ambiente Python. O relatório contém os parâmetros, critérios de parada e instruções de leitura dos resultados.
