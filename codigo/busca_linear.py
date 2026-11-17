"""Goldstein reutilizada do notebook da primeira atividade.

Fonte: projetos-curso-ciencia-de-dados/programacao nao linear/trabalho 1/
parte 2.ipynb, célula que define goldstein. Corpo preservado, inclusive
limites, validações, histórico e as DUAS desigualdades de aceitação.
O manifesto de fontes registra os hashes da origem e desta função.
"""
import numpy as np


def goldstein(phi, derivada0, c=0.1, alfa_inicial=1., max_iter=100):
    f0 = phi(0.)
    if not np.isfinite(derivada0) or derivada0 >= 0 or not np.isfinite(f0):
        raise ValueError("Goldstein exige custo finito e direção de descida estrita.")
    if not 0 < c < 0.5 or not np.isfinite(alfa_inicial) or alfa_inicial <= 0:
        raise ValueError("Parâmetros inválidos para Goldstein.")
    a, b, alfa = 0., None, float(alfa_inicial)
    historico = []
    for etapa in range(1,max_iter+1):
        valor = phi(alfa)
        inferior = f0 + (1-c)*alfa*derivada0
        superior = f0 + c*alfa*derivada0
        historico.append({"alfa":alfa, "custo":valor, "cota_inferior":inferior, "cota_superior":superior})
        if np.isfinite(valor) and inferior <= valor <= superior:
            return {"alfa":alfa, "valor":valor, "intervalo_final":[a,b],
                    "iteracoes":etapa, "historico":historico,
                    "motivo":"ambas as condições de Goldstein satisfeitas",
                    "cota_inferior":inferior, "cota_superior":superior}
        if not np.isfinite(valor) or valor > superior:
            b = alfa
        else:
            a = alfa
        proximo = 2*alfa if b is None else (a+b)/2
        if not np.isfinite(proximo) or proximo == alfa or proximo <= 0:
            raise RuntimeError("Passo inválido ou intervalo estagnado em Goldstein.")
        alfa = proximo
    raise RuntimeError("Goldstein não satisfeita no limite de tentativas.")
