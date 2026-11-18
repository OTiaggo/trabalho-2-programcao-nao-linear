"""Executa os ensaios principais e de refinamento da Parte 2."""

import argparse

from executar import executar


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()

    print('Executando os 24 ensaios principais...', flush=True)
    executar([])

    print('Executando os 24 ensaios de refinamento...', flush=True)
    executar([
        '--tol-f', '0',
        '--max-iter', '20000',
        '--saida', 'resultados/parte2_refinamento',
        '--sem-graficos',
    ])
