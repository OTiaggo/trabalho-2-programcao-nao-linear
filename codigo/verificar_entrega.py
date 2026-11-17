"""Verificação final de rastreabilidade, resultados, notebook e relatório."""
import ast
import hashlib
import json
from pathlib import Path
import numpy as np
import nbformat
from pypdf import PdfReader
from preparar_entrega import casos, BASE, REF, ler
from otimizacao import PROBLEMAS
from testar import verificar_execucao


def verificar():
    resumo = {}
    for pasta in (BASE, REF):
        meta = ler(pasta,'metadados.json')
        assert meta['numero_execucoes']==24
        for arquivo, valor in meta['hashes_codigo'].items():
            assert hashlib.sha256((Path(__file__).parent/arquivo).read_bytes()).hexdigest()==valor, ('código mudou após execução',pasta,arquivo)
        for nome in PROBLEMAS:
            registros=casos(pasta,nome)
            for r in registros:
                verificar_execucao(r)
                if nome=='TP14':
                    xs=np.array([t['x'] for t in r['trajetoria']])
                    assert np.all(xs>0) if r['ponto']=='A' else np.all(xs<0)
            if nome in ('TP3','TP14','TP16'):
                for a,b in zip(registros[::2],registros[1::2]):
                    assert a['iteracoes']==b['iteracoes'] and a['status']==b['status']
                    assert np.allclose([t['x'] for t in a['trajetoria']],-np.array([t['x'] for t in b['trajetoria']]),rtol=0,atol=1e-14)
                    assert a['f_final']==b['f_final'] and a['avaliacoes_f']==b['avaliacoes_f']
                    assert a['eventos'].get('bfgs_omitida_curvatura',0)==0
        resumo[pasta.name]=meta['status']
    # A rotina reutilizada deve ser verificável sem depender do repositório anterior.
    antigo=ast.parse(Path('fontes/goldstein_original.py.txt').read_text(encoding='utf-8')).body[0]
    novo=next(n for n in ast.parse((Path(__file__).parent/'busca_linear.py').read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name=='goldstein')
    assert ast.dump(antigo,include_attributes=False)==ast.dump(novo,include_attributes=False)
    n=nbformat.read('parte 2.ipynb',as_version=4)
    nbformat.validate(n)
    codigos=[c for c in n.cells if c.cell_type=='code']
    for c in codigos:
        compile(c.source,'notebook','exec')
        assert c.execution_count is not None, 'Célula não executada'
        assert all(o.output_type!='error' for o in c.outputs)
    for c in n.cells:
        assert not any(ord(x)<32 and x not in '\n\t\r' for x in c.source), 'Caractere de controle no notebook'
        if c.cell_type=='markdown': assert '\r' not in c.source
    d=PdfReader('output/pdf/relatorio_parte2.pdf')
    texto='\n'.join(p.extract_text() for p in d.pages)
    for termo in ('TP3','TP9','TP14','TP16','Manual','E001','Norberto','20000'):
        assert termo in texto, ('texto ausente no PDF',termo)
    assert len(d.pages)>=10
    resumo['notebook']={'celulas_codigo_executadas':len(codigos),'erros':0}
    resumo['pdf']={'paginas':len(d.pages),'verificacao_visual':'registrada separadamente após renderização'}
    Path('resultados/verificacao_entrega.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(resumo,ensure_ascii=False,indent=2))


if __name__=='__main__':
    verificar()
