"""Validações matemáticas, salvaguardas e contrato das trajetórias."""
import json
from pathlib import Path
import numpy as np
from busca_linear import goldstein
from otimizacao import (PROBLEMAS, METODOS, Parametros, Problema, minimizar,
                        refletir, atualizar_bfgs, tp3, grad3, hess3, grad16)


def validar():
    verificacoes = {}
    rng = np.random.default_rng(20261116)
    for nome, p in PROBLEMAS.items():
        pontos = [np.array(p.inicial), refletir(p.inicial)]
        pontos += [np.array(p.inicial)+rng.uniform(-.15,.15,len(p.inicial)) for _ in range(4)]
        erros_g, erros_h = [], []
        for x in pontos:
            e = np.eye(len(x))
            h = 1e-5
            g_fd = np.array([(p.f(x+h*ei)-p.f(x-h*ei))/(2*h) for ei in e])
            H_fd = np.column_stack([(p.grad(x+h*ei)-p.grad(x-h*ei))/(2*h) for ei in e])
            g, H = p.grad(x), p.hess(x)
            erros_g.append(float(np.max(np.abs(g-g_fd))/max(1.,np.max(np.abs(g)))))
            erros_h.append(float(np.max(np.abs(H-H_fd))/max(1.,np.max(np.abs(H)))))
            assert np.allclose(H,H.T)
        assert max(erros_g) < 1e-7, (nome,erros_g)
        assert max(erros_h) < 1e-7, (nome,erros_h)
        verificacoes[nome] = {'pontos': [x.tolist() for x in pontos],
                              'max_erro_gradiente': max(erros_g), 'max_erro_hessiana': max(erros_h)}
    assert np.allclose(refletir([0,0,0]), [-1,-1,-1])
    assert np.allclose(refletir([0,1]), [0,-1])
    assert np.all(np.linalg.eigvalsh(hess3(None)) > 0)
    assert np.allclose(grad16(np.zeros(4)), 0)
    for metodo in METODOS:
        r = minimizar(PROBLEMAS['TP3'],metodo,[0,0,0])
        assert r['status']=='gradiente' and r['iteracoes']==0 and not r['passos']
        r = minimizar(PROBLEMAS['TP3'],metodo,[1,1,1],Parametros(tol_f=0))
        assert r['status']=='gradiente' and np.linalg.norm(r['x_final'])<2e-5
    for a in (.01,1.,100.):
        r = goldstein(lambda t:(t-2)**2, -4., alfa_inicial=a)
        assert .4-1e-12 <= r['alfa'] <= 3.6+1e-12
        assert r['cota_inferior'] <= r['valor'] <= r['cota_superior']
    try:
        goldstein(lambda t:t*t,0.)
    except ValueError:
        pass
    else:
        raise AssertionError('Direção nula aceita.')
    H = np.eye(2)
    for y in (np.zeros(2), np.array([-1.,0.])):
        nova, evento = atualizar_bfgs(H,np.array([1.,0.]),y,1e-10)
        assert np.array_equal(nova,H) and evento=='bfgs_omitida_curvatura'
    nova, evento = atualizar_bfgs(H,np.array([1.,1.]),np.array([2.,3.]),1e-10)
    assert np.allclose(nova@np.array([2.,3.]),[1.,1.])
    assert np.min(np.linalg.eigvalsh(nova))>0
    r = minimizar(PROBLEMAS['TP14'],'BFGS',[0,.5])
    assert r['status']=='valor_nao_finito' and r['iteracoes']==0
    r = minimizar(PROBLEMAS['TP3'],'BFGS',[1,1,1],Parametros(max_busca=1))
    assert r['status']=='falha_busca' and r['iteracoes']==0
    # Sem mínimo na linha: Goldstein deve falhar com limite, preservando tentativas.
    linear = Problema('linear','teste',lambda x: -x[0],lambda x:np.array([-1.]),lambda x:np.zeros((1,1)),(0.,))
    r = minimizar(linear,'Gradiente',[0],Parametros(max_busca=5))
    assert r['status']=='falha_busca' and len(r['passos'][0]['tentativas'])==6
    verificacoes['casos_especiais'] = 'gradiente nulo, reflexão da origem, curvatura BFGS, secante, domínio e falha limitada: OK'
    # Regressão E001: NaN/inf não podem desativar silenciosamente as paradas.
    rejeitados = []
    for campo in ('tol_grad','tol_f','c_goldstein','passo_inicial','curvatura_relativa','descida_relativa'):
        for valor in (float('nan'),float('inf'),-float('inf')):
            try:
                minimizar(PROBLEMAS['TP3'],'Gradiente',[0,0,0],Parametros(**{campo:valor}))
            except ValueError:
                rejeitados.append(campo+':'+str(valor))
            else:
                raise AssertionError('Parâmetro não finito aceito: '+campo)
    verificacoes['E001_regressao'] = {'rejeicoes_corretas':len(rejeitados),'casos':rejeitados}
    return verificacoes


def verificar_execucao(r):
    p = PROBLEMAS[r['problema']]
    assert len(r['trajetoria']) == r['iteracoes']+1
    for a,b in zip(r['trajetoria'],r['trajetoria'][1:]):
        assert b['f'] <= a['f']
    for passo in r['passos']:
        if passo['status'] != 'aceito':
            continue
        k = passo['k']
        a,b = r['trajetoria'][k:k+2]
        assert np.allclose(np.array(a['x'])+passo['alfa']*np.array(passo['direcao']),b['x'])
        assert passo['gTd'] < 0
        gs = passo['goldstein']
        assert gs['cota_inferior'] <= b['f'] <= gs['cota_superior']
        assert np.isclose(p.f(np.array(b['x'])),b['f'])
        assert np.allclose(p.grad(np.array(b['x'])),b['gradiente'])
        if r['metodo']=='FR' and passo['beta_fr'] is not None:
            g,old = np.array(a['gradiente']),np.array(r['trajetoria'][k-1]['gradiente'])
            assert np.isclose(passo['beta_fr'], (g@g)/(old@old))


if __name__ == '__main__':
    destino = Path('resultados/parte2')
    destino.mkdir(parents=True,exist_ok=True)
    v = validar()
    (destino/'validacao.json').write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(v,indent=2,ensure_ascii=False))
