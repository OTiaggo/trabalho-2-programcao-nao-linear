"""Executa a matriz independente e exporta sequências, custos e gráficos."""
import argparse
import csv
import hashlib
import gzip
import json
import platform
from pathlib import Path
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from otimizacao import PROBLEMAS, METODOS, Parametros, minimizar, refletir
from testar import validar, verificar_execucao


def salvar_json(path, obj):
    """JSON padrão: não finitos viram null; o status conserva o motivo."""
    def limpar(x):
        if isinstance(x,dict): return {k:limpar(v) for k,v in x.items()}
        if isinstance(x,(tuple,list)): return [limpar(v) for v in x]
        if isinstance(x,(float,np.floating)) and not np.isfinite(x): return None
        return x
    texto = json.dumps(limpar(obj),ensure_ascii=False,indent=2,allow_nan=False)
    if len(texto)>4_000_000:
        with gzip.open(str(path)+'.gz','wt',encoding='utf-8') as f:
            f.write(texto)
    else:
        path.write_text(texto,encoding='utf-8')


def diagnosticar(r):
    p = PROBLEMAS[r['problema']]
    eig = np.linalg.eigvalsh(p.hess(np.array(r['x_final'])))
    r['autovalores_hessiana_final'] = eig.tolist()
    r['condicao_hessiana_final'] = float(np.max(np.abs(eig))/np.min(np.abs(eig))) if np.min(np.abs(eig))>0 else None
    r['eventos'] = dict(Counter(e for s in r['passos'] for e in s['eventos']))
    dirs = [np.array(s['direcao']) for s in r['passos'] if s['status']=='aceito']
    cos = [float(a@b/(np.linalg.norm(a)*np.linalg.norm(b))) for a,b in zip(dirs,dirs[1:])]
    r['cosseno_mediano_direcoes'] = float(np.median(cos)) if cos else None
    r['fracao_direcoes_opostas'] = float(np.mean(np.array(cos)<0)) if cos else None


def figuras(resultados, destino):
    cores = dict(zip(METODOS, ('#2864a0','#d77a19','#20976b')))
    for nome,p in PROBLEMAS.items():
        casos = [r for r in resultados if r['problema']==nome]
        fig,axes = plt.subplots(1,2,figsize=(10,3.5))
        for r in casos:
            t=r['trajetoria']; k=[v['k'] for v in t]
            label=r['metodo']+' '+r['ponto']
            style='-' if r['ponto']=='A' else '--'
            axes[0].semilogy(k,np.maximum([v['f'] for v in t],1e-30),style,color=cores[r['metodo']],label=label)
            axes[1].semilogy(k,np.maximum([v['norma_grad'] for v in t],1e-30),style,color=cores[r['metodo']],label=label)
        axes[0].set_ylabel('f(xk)'); axes[1].set_ylabel('Norma do gradiente')
        axes[1].axhline(1e-5,color='gray',linewidth=.7)
        for ax in axes: ax.set_xlabel('Iteração k'); ax.grid(alpha=.2)
        axes[1].legend(fontsize=7)
        fig.suptitle(nome+' - objetivos e estacionariedade (A: sólida; B: tracejada)')
        fig.tight_layout(); fig.savefig(destino/(nome+'_evolucao.png'),dpi=160); plt.close(fig)
        # Para 3D/4D, declarar a projeção; não fingir curvas de nível em R^n.
        fig,axes=plt.subplots(1,2,figsize=(10,4))
        for ax,ponto in zip(axes,('A','B')):
            selecionados=[r for r in casos if r['ponto']==ponto]
            todos=np.array([v['x'][:2] for r in selecionados for v in r['trajetoria']])
            lo=todos.min(axis=0); hi=todos.max(axis=0); margem=np.maximum((hi-lo)*.12,.15)
            if len(p.inicial)==2:
                xx=np.linspace(lo[0]-margem[0],hi[0]+margem[0],240)
                yy=np.linspace(lo[1]-margem[1],hi[1]+margem[1],240)
                X,Y=np.meshgrid(xx,yy)
                with np.errstate(all='ignore'):
                    Z=np.array([[p.f(np.array([u,v])) for u in xx] for v in yy])
                finite=Z[np.isfinite(Z)]
                levels=np.geomspace(max(float(finite.min())+1e-4,1e-4),max(float(np.percentile(finite,90)),1.),18)
                ax.contour(X,Y,Z,levels=levels,colors='gray',alpha=.45,linewidths=.5)
            for r in selecionados:
                xs=np.array([v['x'] for v in r['trajetoria']])
                ax.plot(xs[:,0],xs[:,1],'.-',ms=2,lw=.8,color=cores[r['metodo']],label=r['metodo'])
                ax.scatter(*xs[0,:2],marker='s',s=22,color=cores[r['metodo']])
                ax.scatter(*xs[-1,:2],marker='x',s=36,color=cores[r['metodo']])
            ax.set(xlabel='x1',ylabel='x2',title=ponto+(' - projeção em (x1,x2)' if len(p.inicial)>2 else ' - curvas de nível'))
            ax.set_xlim(lo[0]-margem[0],hi[0]+margem[0]); ax.set_ylim(lo[1]-margem[1],hi[1]+margem[1]); ax.legend(fontsize=7); ax.grid(alpha=.15)
        fig.suptitle(nome+' - trajetórias; quadrado: início, cruz: fim')
        fig.tight_layout(); fig.savefig(destino/(nome+'_trajetorias.png'),dpi=160); plt.close(fig)


def executar(args=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tol-grad',type=float,default=1e-5)
    parser.add_argument('--tol-f',type=float,default=1e-7,help='0 desativa parada por variação')
    parser.add_argument('--max-iter',type=int,default=1000)
    parser.add_argument('--saida',default='resultados/parte2')
    parser.add_argument('--sem-graficos',action='store_true')
    opt=parser.parse_args(args)
    destino=Path(opt.saida); destino.mkdir(parents=True,exist_ok=True)
    salvar_json(destino/'validacao.json',validar())
    param=Parametros(tol_grad=opt.tol_grad,tol_f=opt.tol_f,max_iter=opt.max_iter)
    resultados=[]
    for nome,p in PROBLEMAS.items():
        for metodo in METODOS:
            for ponto,x0 in (('A',p.inicial),('B',refletir(p.inicial))):
                r=minimizar(p,metodo,x0,param); r['ponto']=ponto
                verificar_execucao(r); diagnosticar(r)
                resultados.append(r)
                salvar_json(destino/f'{nome}_{metodo}_{ponto}.json',r)
                print(nome,metodo,ponto,r['iteracoes'],r['status'],f"f={r['f_final']:.8g}",f"g={r['norma_grad_final']:.3g}")
    campos=['problema','metodo','ponto','x0','x_final','f_final','norma_grad_final','iteracoes','avaliacoes_f','avaliacoes_g','status','eventos','condicao_hessiana_final','cosseno_mediano_direcoes','fracao_direcoes_opostas']
    with (destino/'resumo.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=campos); w.writeheader()
        for r in resultados: w.writerow({k:r[k] for k in campos})
    hashes={nome:hashlib.sha256((Path(__file__).parent/nome).read_bytes()).hexdigest() for nome in ('otimizacao.py','busca_linear.py','executar.py','testar.py')}
    salvar_json(destino/'metadados.json',{'python':platform.python_version(),'numpy':np.__version__,'matplotlib':matplotlib.__version__,'parametros':vars(param),'hashes_codigo':hashes,'numero_execucoes':len(resultados),'status':dict(Counter(r['status'] for r in resultados))})
    if not opt.sem_graficos: figuras(resultados,destino)
    return resultados


if __name__=='__main__':
    executar()
