"""Gera notebook e relatório PDF a partir de resultados já verificados.

Não executa minimização ao importar. Execute após executar.py e o refinamento.
"""
import gzip
import json
from pathlib import Path
from xml.sax.saxutils import escape
import numpy as np
import nbformat as nbf
import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                               TableStyle, PageBreak, Image, KeepTogether)
from otimizacao import PROBLEMAS, METODOS

RAIZ=Path(__file__).resolve().parents[1]
BASE=RAIZ/'resultados/parte2'
REF=RAIZ/'resultados/parte2_refinamento'


def ler(pasta, nome):
    p=pasta/nome
    if Path(str(p)+'.gz').exists():
        with gzip.open(str(p)+'.gz','rt',encoding='utf-8') as f: return json.load(f)
    return json.loads(p.read_text(encoding='utf-8'))


def casos(pasta,nome):
    return [ler(pasta,f'{nome}_{m}_{p}.json') for m in METODOS for p in ('A','B')]


ANALISES={
    'TP3': [
        'O mínimo global único é a origem. A Hessiana constante tem autovalores 3−√5, 3+√5 e 6, todos positivos, e condição espectral 7,8541. A coercividade garante existência; a definição positiva garante unicidade. Assim, ambos os pontos pertencem à região de atração observada do mesmo mínimo. A conclusão usa esta função específica, não apenas convexidade.',
        'A simetria f(−x)=f(x), o gradiente ímpar e a inicialização H0=I tornam as trajetórias refletidas para os algoritmos implementados. Os custos, passos e números de iterações A/B coincidem. Com parada apenas por gradiente, BFGS necessita 7 passos, FR 22 e gradiente 42. A parada sugerida por variação encerra mais cedo (6, 18 e 28), ainda com norma acima de 10⁻⁵.',
        'No gradiente clássico, 88,9% dos pares de direções consecutivas do experimento principal têm produto interno negativo (cosseno mediano −0,406): há alternância compatível com ziguezague. Goldstein é inexata; não se afirma ortogonalidade exata entre direções consecutivas.'
    ],
    'TP14': [
        'A função exclui x1=0 e x2=0. Ela depende somente dos quadrados: a reflexão de todas as coordenadas preserva o custo e reflete as trajetórias. Nas execuções, A permanece no primeiro quadrante e B no terceiro. Ambos chegam a soluções com o mesmo valor, mas coordenadas de sinais opostos. Isso é evidência de duas bacias visitadas; apenas dois pontos não constituem um mapa completo das bacias.',
        'Há quatro mínimos globais: (±1,74345209; ±2,02969471), com sinais independentes e f*=1,74415200559. Para demonstrar unicidade por quadrante, faça a=log|x1| e b=log|x2|: o objetivo é soma de exponenciais de formas afins com Hessiana positiva definida e é coercivo em (a,b). Logo tem um único minimizador nessas variáveis. A simetria fornece os quatro pontos. Goldstein só verifica valores amostrados: não se deve deduzir que qualquer execução preservará quadrante.',
        'No refinamento, FR exige 15 passos, gradiente 20 e BFGS 28 em ambos os pontos. BFGS não foi o mais rápido neste caso: a primeira direção é muito grande e H0=I não incorpora a escala inicial. A condição final é cerca de 2,836. Não houve convergência observada para sela.'
    ],
    'TP9': [
        'O mínimo global é (1;1), pois ambos os quadrados não negativos só se anulam nesse ponto. A equação g2=0 implica x2=x1² e então g1=0 implica x1=1: este é o único ponto estacionário, portanto nenhuma sela finita pode ser destino estacionário desta função. A reflexão do ponto inicial não produz simetria do objetivo.',
        'No experimento principal o gradiente a partir de B atinge 1.000 iterações com f=0,12955 e norma 0,56842. A partir de A ele para por variação em 102 passos; isso não comprova a tolerância de gradiente. Mesmo com 20.000 passos, o gradiente clássico não atinge 10⁻⁵ em A ou B. O vale curvo é estreito e a Hessiana no mínimo tem autovalores aproximadamente 0,399936 e 10001,6001, condição 25008. Há alternância de direções em 91,1% (A) e 86,7% (B) dos pares do ensaio principal.',
        'BFGS atinge a tolerância do gradiente em 61 passos (A) e 45 (B); FR em 442 (A) e 282 (B), com reinícios declarados. A reflexão mudou o custo de aproximação, sem evidência de mínimo diferente. Não se deve concluir que FR foi melhor porque parou antes no ensaio com variação: os gradientes finais não eram comparáveis.'
    ],
    'TP16': [
        'Apesar do rótulo G3, esta função é convexa: é soma de quadrados e quartas potências de funções afins. Seu mínimo único é zero na origem. Anular os quatro termos força x1=−10x2, x3=x4, x2=2x3 e x1=x4; logo todas as coordenadas são zero. Convexidade e unicidade excluem mínimos locais distintos ou selas estacionárias.',
        'A Hessiana na origem tem autovalores 0, 0, 20 e 202. Ela é singular; a condição espectral é infinita e a função não é fortemente convexa na vizinhança do mínimo. Nas direções degeneradas o crescimento é de quarta ordem. Um gradiente pequeno pode ocorrer ainda a uma distância visível da origem, por isso os pontos finais também são apresentados.',
        'A/B produzem trajetórias refletidas e exatamente os mesmos custos e contagens. O gradiente não atinge a tolerância em 20.000 passos. BFGS a atinge em 24 e FR em 611. No ensaio principal, BFGS e FR param por variação em 21 e 72 passos com gradientes acima do limiar. Os gráficos e os autovalores finais documentam degenerescência e lentidão; não indicam uma nova bacia ou sela.'
    ]
}


def criar_notebook():
    n=nbf.v4.new_notebook()
    n.metadata={'kernelspec':{'display_name':'Python 3 (PNL)','language':'python','name':'python3'}}
    cells=[nbf.v4.new_markdown_cell('''# Parte 2 - Métodos multidimensionais e reflexão

**Tiago Oliveira Lima (564988) e Noberto Frota Oliveira Nogueira (568044)** · UFC · Ricardo Coelho · 16/11/2026.

Implementações em `codigo/otimizacao.py` e `codigo/busca_linear.py`. Não há otimizador pronto nem busca 1D de biblioteca. A busca Goldstein é reutilizada do código anterior e sua origem está em `fontes/manifesto.json`. As 24 execuções principais usam os critérios sugeridos; 24 execuções adicionais isolam a parada por gradiente. A Parte 1 não faz parte deste notebook.

Execute todas as células a partir desta pasta. O relatório inclui manual, análise e limites. A distribuição de responsabilidades foi declarada pelo usuário em 17/11/2026 e está registrada ao final.'''),
        nbf.v4.new_markdown_cell(r'''## Funções e pontos iniciais

Catálogo original: `fontes/catalogo_primeira_atividade.pdf`, páginas 4-6. A potência e os denominadores do TP14 foram conferidos visualmente.

|TP|Função|A|B|
|---|---|---|---|
|3|$x_1^2+2x_2^2+3x_3^2-2x_1x_2$|(1,1,1)|(-1,-1,-1)|
|14|$0.1[12+x_1^2+(1+x_2^2)/x_1^2+(x_1^2x_2^2+100)/(x_1^4x_2^4)]$|(.5,.5)|(-.5,-.5)|
|9|$1000(x_2-x_1^2)^2+(1-x_1)^2$|(-1.2,1)|(1.2,-1)|
|16|$(x_1+10x_2)^2+5(x_3-x_4)^2+(x_2-2x_3)^4+10(x_1-x_4)^4$|(3,-1,0,1)|(-3,1,0,-1)|

TP14: domínio $x_1x_2\ne0$. TP16: mínimo com Hessiana singular.

## Algoritmos

Gradiente: $d_k=-g_k$. BFGS inversa: $H_0=I$, $d_k=-H_kg_k$, $H_{k+1}=(I-\rho sy^T)H_k(I-\rho ys^T)+\rho ss^T$, $\rho=(s^Ty)^{-1}$, $s=x_{k+1}-x_k$, $y=g_{k+1}-g_k$. Atualização omitida se não houver curvatura segura.

FR: $\beta=\|g_{k+1}\|^2/\|g_k\|^2$, $d_{k+1}=-g_{k+1}+\beta d_k$. Reinício a cada dimensão n e quando faltar descida; cada evento é registrado.

Goldstein: $f_k+(1-c)\alpha g_k^Td_k\le f(x_k+\alpha d_k)\le f_k+c\alpha g_k^Td_k$, $c=0.1$. Esta busca não impõe Wolfe forte; os resultados são experimentais, sem atribuir automaticamente a garantia teórica clássica de FR.'''),
        nbf.v4.new_code_cell('from pathlib import Path\nimport sys\nsys.path.insert(0, str(Path.cwd() / "codigo"))\nfrom testar import validar\nvalidacao = validar()\nvalidacao'),
        nbf.v4.new_markdown_cell('## Matriz principal\n\nParada por gradiente ≤ 1e-5 **ou** variação relativa ≤ 1e-7 **ou** 1000 passos. Variação e limite não são certificados de convergência.'),
        nbf.v4.new_code_cell('from executar import executar\nresultados = executar([])'),
        nbf.v4.new_code_cell('''from IPython.display import HTML, display, Image
from html import escape
cab = ['TP','Método','A/B','Ponto final','f','Norma g','k','f/g','Parada']
linhas = []
for r in resultados:
    v=[r['problema'],r['metodo'],r['ponto'],str(r['x_final']),f"{r['f_final']:.8g}",f"{r['norma_grad_final']:.4g}",r['iteracoes'],str(r['avaliacoes_f'])+'/'+str(r['avaliacoes_g']),r['status']]
    linhas.append('<tr>'+''.join('<td>'+escape(str(x))+'</td>' for x in v)+'</tr>')
display(HTML('<table><tr>'+''.join('<th>'+x+'</th>' for x in cab)+'</tr>'+''.join(linhas)+'</table>'))'''),
        nbf.v4.new_markdown_cell('## Sequências de pontos\n\nAmostra de início/fim de cada uma das 24 sequências abaixo. Todos os pontos, direções, passos, avaliações e tentativas de busca estão nos arquivos JSON (ou JSON.gz) em `resultados/parte2`. Não há encadeamento entre métodos.'),
        nbf.v4.new_code_cell(r'''for r in resultados:
    print('\n',r['problema'],r['metodo'],r['ponto'])
    t=r['trajetoria']
    for k in sorted(set(list(range(min(3,len(t))))+list(range(max(0,len(t)-2),len(t))))):
        z=t[k]
        print(z['k'],z['x'],'f=',z['f'],'norma_g=',z['norma_grad'])''')]
    for nome in PROBLEMAS:
        cells += [nbf.v4.new_markdown_cell('## '+nome+' - interpretação\n\n'+'\n\n'.join(ANALISES[nome])),
                  nbf.v4.new_code_cell(f"display(Image(filename='resultados/parte2/{nome}_evolucao.png'))\ndisplay(Image(filename='resultados/parte2/{nome}_trajetorias.png'))")]
    cells += [nbf.v4.new_markdown_cell('''## Refinamento por gradiente

Gerado independentemente com `python codigo/executar.py --tol-f 0 --max-iter 20000 --saida resultados/parte2_refinamento --sem-graficos`. Os 24 registros completos são preservados; esta célula somente os lê para evitar repetir os ensaios adicionais ao abrir o notebook.'''),
              nbf.v4.new_code_cell("from preparar_entrega import casos, REF\nfor nome in ['TP3','TP14','TP9','TP16']:\n    for r in casos(REF,nome):\n        print(nome,r['metodo'],r['ponto'],r['iteracoes'],r['norma_grad_final'],r['status'])"),
              nbf.v4.new_markdown_cell('''## Manual e auditoria

Instalação: `python -m venv .venv`, depois `.venv/Scripts/python -m pip install -r requirements.txt`. Execução: `.venv/Scripts/python codigo/executar.py`. Verificações: `.venv/Scripts/python codigo/testar.py`. O comando `python codigo/preparar_entrega.py` regenera este notebook (sem saídas) e o PDF; reexecute o notebook depois.

Entrada: funções e pontos em `PROBLEMAS`; parâmetros na CLI ou `Parametros`. Uso direto: `minimizar(PROBLEMAS['TP9'], 'BFGS', [-1.2,1.], Parametros())`. Nunca iniciar o próximo método pelo resultado do anterior.

Saída: `resumo.csv` contém uma linha por execução; `TP*_Método_A/B.json[.gz]` contém toda a trajetória e passos; `metadados.json` registra parâmetros, versões e hashes; `validacao.json` contém evidências dos testes. Para gzip: `gzip.open(caminho, 'rt', encoding='utf-8')` e `json.load`.

Status: `gradiente` indica tolerância atingida; `variacao_objetivo` indica apenas pouca mudança; `limite_iteracoes` é inconclusivo; `falha_busca`, `valor_nao_finito` e `derivada_indefinida` são falhas explícitas. Os valores do objetivo são calculados com float64.

**Auditoria E001:** a primeira implementação permitia tol_grad=NaN: `NaN <= 0` é falso e `0 <= NaN` também. No mínimo do TP3 ela tentava busca com direção zero e retornava falha_busca. A correção valida finitude antes de avaliar a função. Os arquivos `resultados/auditoria/E001_antes.json` e `E001_depois.json` e 18 testes de regressão registram antes/depois. Não se trata de erro na derivada, nem afetou as execuções com tolerâncias finitas.

**Responsabilidades (distribuição declarada pelo usuário em 17/11/2026):**

| Responsável | Contribuição |
| --- | --- |
| Tiago Oliveira Lima (564988) | Parte 1: seleção dos trabalhos nos Encontros Universitários e elaboração dos resumos 1, 3 e 5. Parte 2: definição do escopo junto ao assistente (P001–P003); conferência das derivadas analíticas do TP3 e do TP9 contra o catálogo da primeira atividade; conferência da busca de Goldstein recuperada da Atividade 1 e de seus parâmetros (c = 0,1, α inicial = 1); análise dos resultados do TP3 e do TP9 (simetria das trajetórias, ziguezague do gradiente, vale estreito); execução dos comandos do Manual de Uso para checar a reprodutibilidade. |
| Noberto Frota Oliveira Nogueira (568044) | Parte 1: seleção dos trabalhos nos Encontros Universitários e elaboração dos resumos 2 e 4. Parte 2: conferência da atribuição de problemas e métodos (script de sorteio, semente 1133032) e dos pontos A/B; conferência das derivadas do TP14 e do TP16 e das referências analíticas (quatro mínimos do TP14, convexidade e Hessiana singular do TP16); revisão das salvaguardas do BFGS (condição de curvatura) e dos reinícios de Fletcher–Reeves; análise dos resultados do TP14 e do TP16 e redação da resposta à questão investigativa sobre bacias de atração; revisão do erro E001 e leitura final do relatório. |
| IA (Codex) | Apoio na localização e conferência de fontes, recuperação da Goldstein, implementação dos métodos e derivadas, execução de testes e ensaios, geração de gráficos, notebook e relatório e correção de E001. As contribuições humanas foram declaradas pelo usuário. |

A distribuição inclui a Parte 1; suas fichas não integram este notebook nem o relatório da Parte 2. Os registros de prompts, contribuições e E001 estão em `documentacao/auditoria/`.

Referência teórica: [Hager e Zhang, A Survey of Nonlinear Conjugate Gradient Methods, §§2 e 4](https://people.clas.ufl.edu/hager/files/cg_survey.pdf). As garantias de FR discutidas nessa fonte dependem de condições de busca que não são automaticamente impostas por Goldstein.''')]
    n.cells=cells
    nbf.write(n,RAIZ/'parte 2.ipynb')


def criar_pdf():
    fontdir=Path(matplotlib.get_data_path())/'fonts/ttf'
    pdfmetrics.registerFont(TTFont('DejaVu',str(fontdir/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(fontdir/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
    styles=getSampleStyleSheet()
    for key in ('Normal','BodyText','Title','Heading1','Heading2','Heading3'):
        styles[key].fontName='DejaVu'
    styles['BodyText'].fontSize=9
    styles['BodyText'].leading=13
    styles['BodyText'].spaceAfter=7
    styles['Title'].fontSize=23
    styles['Title'].leading=29
    styles['Heading1'].fontSize=15
    styles['Heading1'].leading=20
    styles['Heading1'].textColor=colors.HexColor('#24527a')
    styles.add(ParagraphStyle('small',fontName='DejaVu',fontSize=7.2,leading=10,spaceAfter=5))
    styles.add(ParagraphStyle('formula',fontName='DejaVu',fontSize=8.5,leading=13,leftIndent=9,spaceAfter=9,textColor=colors.HexColor('#184f70')))
    story=[]
    def p(text,style='BodyText'): story.append(Paragraph(text,styles[style]))
    def h(text): p(text,'Heading1')
    def br(): story.append(PageBreak())
    def tabela(rows,widths):
        data=[[Paragraph(escape(str(c)),styles['small']) for c in row] for row in rows]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7eff6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#24527a')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f8fa')]),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        story.append(t); story.append(Spacer(1,9))
    p('UFC · Bacharelado em Ciência de Dados','small')
    p('Programação Não Linear<br/>Segunda Atividade Computacional','Title')
    p('Parte 2 - Métodos multidimensionais<br/>e simetria refletida','Heading1')
    p('Tiago Oliveira Lima - matrícula 564988<br/>Noberto Frota Oliveira Nogueira - matrícula 568044<br/>Professor: Ricardo Coelho<br/>16 de novembro de 2026')
    story.append(Spacer(1,12))
    h('Escopo e resultado principal')
    p('Comparam-se gradiente clássico, BFGS e Fletcher-Reeves (FR), todos com a busca Goldstein recuperada da primeira atividade. São 24 execuções principais independentes e 24 adicionais com critério de gradiente. Código, dados completos e gráficos acompanham este relatório. A pesquisa dos EU/UFC (Parte 1) não integra este documento.')
    p('O critério sugerido de variação interrompe várias sequências antes de satisfazer a tolerância do gradiente. No refinamento, BFGS e FR atingem a tolerância nos oito pares problema/ponto; o gradiente clássico atinge o limite de 20.000 passos no TP9 e no TP16. Esses limites são reportados como resultados inconclusivos, sem declarar convergência plena dessas execuções.')
    tabela([['Problema','Grupo / dimensão','Ponto A','Ponto B'],['TP3','G1 / 3','(1;1;1)','(−1;−1;−1)'],['TP14','G2 / 2','(0,5;0,5)','(−0,5;−0,5)'],['TP9','G2 / 2','(−1,2;1)','(1,2;−1)'],['TP16','G3 / 4','(3;−1;0;1)','(−3;1;0;−1)']],[65,110,158,158])
    p('Origem: catálogo da primeira atividade, pp. 4-6, preservado em fontes/catalogo_primeira_atividade.pdf. Métodos: script fornecido em fontes/atribuicoes/atribuicao dos metodos.txt, semente 1133032, BFGS e FR. A seleção não foi alterada. A distribuição de responsabilidades declarada pelo usuário está na seção 6.')
    br(); h('1. Funções, derivadas e geometria')
    p('As derivadas abaixo foram deduzidas para as fórmulas do catálogo e verificadas por diferenças centrais nos pontos A/B e em quatro perturbações determinísticas por problema. As Hessianas são utilizadas apenas no diagnóstico e nos testes, não na construção das direções dos três métodos.')
    p('<b>TP3.</b> Domínio R³. Escrevendo x=(u,v,w):')
    p('f = u² + 2v² + 3w² − 2uv<br/>g = (2u−2v; 4v−2u; 6w)<br/>Hessiana = [[2,−2,0], [−2,4,0], [0,0,6]]','formula')
    p(ANALISES['TP3'][0])
    p('<b>TP9.</b> Domínio R². Escrevendo r=v−u²:')
    p('f = 1000r² + (1−u)²<br/>g = (−4000ur + 2(u−1); 2000r)<br/>Hessiana = [[12000u²−4000v+2, −4000u], [−4000u, 2000]]','formula')
    p(ANALISES['TP9'][0])
    p('A função não é globalmente convexa: por exemplo, em (0;1), a primeira entrada diagonal da Hessiana é −3998. Mesmo assim, o mínimo global único é explícito. Essa distinção evita confundir não convexidade com a existência necessária de vários mínimos.')
    p('<b>TP14.</b> Domínio {(u,v): uv ≠ 0}. Forma expandida equivalente à fração do catálogo:')
    p('f = 0,1[12 + u² + (1+v²)/u² + 1/(u²v²) + 100/(u⁴v⁴)]<br/>g1 = 0,1[2u − 2(1+v²)/u³ − 2/(u³v²) − 400/(u⁵v⁴)]<br/>g2 = 0,1[2v/u² − 2/(u²v³) − 400/(u⁴v⁵)]','formula')
    p('H11 = 0,1[2 + 6(1+v²)/u⁴ + 6/(u⁴v²) + 2000/(u⁶v⁴)]<br/>H12 = H21 = 0,1[−4v/u³ + 4/(u³v³) + 1600/(u⁵v⁵)]<br/>H22 = 0,1[2/u² + 6/(u²v⁴) + 2000/(u⁴v⁶)]','formula')
    br(); h('1. Funções e referências analíticas (continuação)')
    p(ANALISES['TP14'][1])
    p('Para calcular uma referência independente dos algoritmos, tome t=u², z=v². Das duas equações de estacionariedade obtêm-se t²=1+2z e √(1+2z)·z·(z²−1)=200, com z&gt;1. A função do lado esquerdo é estritamente crescente nesse intervalo. A bisseção escalar dessa equação fornece os valores citados; não substitui a busca linear dos experimentos.')
    p('<b>TP16.</b> Domínio R⁴. Escrevendo a=u+10v, b=w−z, c=v−2w e d=u−z:')
    p('f = a² + 5b² + c⁴ + 10d⁴<br/>g = (2a+40d³; 20a+4c³; 10b−8c³; −10b−40d³)','formula')
    p('Se A=(1,10,0,0), B=(0,0,1,−1), C=(0,1,−2,0) e D=(1,0,0,−1), então<br/>Hessiana = 2AAᵀ + 10BBᵀ + 12c²CCᵀ + 120d²DDᵀ.','formula')
    p(ANALISES['TP16'][0]); p(ANALISES['TP16'][1])
    p('<b>Validação das derivadas.</b> Passo h=10⁻⁵; erro medido por max|analítico−diferença| / max(1,max|analítico|). O limiar foi 10⁻⁷. A semente das perturbações é 20261116.')
    v=ler(BASE,'validacao.json')
    tabela([['TP','Maior erro gradiente','Maior erro Hessiana']]+[[n,f"{v[n]['max_erro_gradiente']:.3e}",f"{v[n]['max_erro_hessiana']:.3e}"] for n in PROBLEMAS],[80,205,206])
    p('Os testes verificam ainda o mínimo quadrático, gradiente inicial zero, reflexão da origem, identidade secante BFGS, rejeição de curvatura não positiva, exclusão dos eixos no TP14, falha limitada de busca e parâmetros não finitos. Cada passo aceito das 48 execuções é confrontado com sua direção, novo ponto, gradiente e ambas as cotas de Goldstein.')
    br(); h('2. Métodos e protocolo experimental')
    p('<b>Gradiente clássico:</b> d_k=−g_k. <b>BFGS:</b> usa-se a aproximação H_k da inversa da Hessiana, iniciada por I em cada execução, e d_k=−H_k g_k. Defina s=x_(k+1)−x_k e y=g_(k+1)−g_k. Com ρ=1/(sᵀy):')
    p('H_(k+1) = (I−ρsyᵀ) H_k (I−ρysᵀ) + ρssᵀ','formula')
    p('A atualização só ocorre se sᵀy&gt;10⁻¹⁰||s||||y|| e sᵀy&gt;0. A matriz é simetrizada; valores não finitos ou falha de Cholesky fazem a atualização ser omitida, conservando H_k. Não há inversão explícita. Nenhuma atualização foi omitida nos ensaios principais ou de refinamento; todos os eventos permanecem nos arquivos.')
    p('<b>Fletcher-Reeves:</b> β_k=||g_(k+1)||²/||g_k||², d_(k+1)=−g_(k+1)+β_k d_k. Há reinício d=−g a cada n passos, onde n é a dimensão, e quando a direção perde descida. Essa é a fórmula FR com reinícios declarados, sem substituição por PR ou PR+.')
    p('Antes da busca exige-se gᵀd &lt; −10⁻¹²||g||||d||. Caso contrário, reinicia-se por −g; no BFGS também se restaura H=I. As avaliações de f e g são contadas separadamente. O cache evita recalcular f_k ao avaliar α=0. Avaliações de Hessiana para análise não entram nessas contagens.')
    p('<b>Busca reutilizada:</b> Goldstein, c=0,1, α inicial=1, máximo de 100 tentativas. O limite inferior começa em zero; sem extremo superior, duplica-se o passo; com intervalo, usa-se seu ponto médio. Aceitação:')
    p('f_k + (1−c)αg_kᵀd_k ≤ f(x_k+αd_k) ≤ f_k + cαg_kᵀd_k','formula')
    p('A rotina é idêntica à função recuperada do notebook anterior: a comparação da árvore sintática confirmou identidade. O recorte original e o manifesto com hashes acompanham o código. As outras buscas atribuídas na atividade anterior não precisam ser cruzadas com todos os métodos nesta atividade.')
    p('Goldstein não impõe condição sobre a derivada no ponto aceito. Portanto não se transfere automaticamente a teoria clássica de FR com Wolfe forte, nem se garante curvatura positiva de BFGS apenas por Armijo/Goldstein. As salvaguardas tratam essas ocorrências e limitam laços. A distinção entre condições de busca e garantias de FR é discutida por Hager e Zhang [3, §§2 e 4].')
    p('<b>Ensaio principal:</b> ||g||≤10⁻⁵ OU |f_novo−f_antigo|/max(1,|f_antigo|)≤10⁻⁷ OU k≥1000. Gradiente tem prioridade se dois testes forem satisfeitos no mesmo passo. <b>Refinamento:</b> mesmas funções, busca, métodos e pontos, com tol_f=0 (critério desativado) e máximo de 20.000 passos. Todos os ensaios começam novamente de A/B. Limite não prova convergência; gradiente pequeno é apenas estacionariedade numérica, interpretada à luz da geometria.')
    for nome in PROBLEMAS:
        br(); h('3. Resultados - '+nome)
        p('Ensaio principal. Vetores são apresentados com seis algarismos significativos; os arquivos de dados mantêm precisão de float64. G: gradiente; V: variação do objetivo; L: limite. f/g: avaliações de função/gradiente.','small')
        rows=[['Método / ponto','Ponto final','f final','||g||','k','f/g','Fim']]
        for r in casos(BASE,nome):
            rows.append([r['metodo']+' '+r['ponto'],'; '.join(f'{x:.6g}' for x in r['x_final']),f"{r['f_final']:.5g}",f"{r['norma_grad_final']:.3g}",r['iteracoes'],str(r['avaliacoes_f'])+'/'+str(r['avaliacoes_g']),{'gradiente':'G','variacao_objetivo':'V','limite_iteracoes':'L'}[r['status']]])
        tabela(rows,[77,143,60,51,36,83,41])
        p('<b>Refinamento independente (tol_f=0).</b> A diferença de desempenho é comparada com a mesma tolerância do gradiente.','small')
        rows=[['Método / ponto','f final','||g||','k','f/g','Fim']]
        for r in casos(REF,nome):
            rows.append([r['metodo']+' '+r['ponto'],f"{r['f_final']:.5g}",f"{r['norma_grad_final']:.3g}",r['iteracoes'],str(r['avaliacoes_f'])+'/'+str(r['avaliacoes_g']),'G' if r['status']=='gradiente' else 'L'])
        tabela(rows,[100,85,75,55,115,61])
        for text in ANALISES[nome][1 if nome=='TP3' else 0:]: p(text,'small')
        story.append(Image(str(BASE/(nome+'_evolucao.png')),width=491,height=172))
    br(); h('4. Trajetórias e sequências completas')
    p('Cada arquivo TP*_Método_A/B.json (ou .json.gz) contém trajetória x_k completa, f_k, gradiente, norma e contagens; a lista passos contém d_k, gᵀd, α, tentativas de busca, β de FR, eventos e atualizações BFGS. O notebook mostra as primeiras e últimas amostras de cada execução. Os gráficos abaixo são do ensaio principal; o refinamento tem suas próprias sequências completas. Projeções em duas coordenadas não descrevem toda a geometria em três ou quatro dimensões.')
    for nome in ('TP3','TP14'):
        story.append(Image(str(BASE/(nome+'_trajetorias.png')),width=491,height=196))
        story.append(Spacer(1,12))
    br(); h('4. Trajetórias (continuação)')
    for nome in ('TP9','TP16'):
        story.append(Image(str(BASE/(nome+'_trajetorias.png')),width=491,height=196))
        story.append(Spacer(1,12))
    p('A reflexão tem três efeitos distintos nesta suíte: preserva o mínimo e reflete o percurso no TP3/TP16; seleciona mínimos simétricos distintos no TP14; e muda o esforço para chegar ao mesmo mínimo no TP9. Não se observou chegada a sela. O número de iterações deve ser lido junto com o motivo de parada, o gradiente final e as avaliações, sobretudo quando se compara o ensaio sugerido com o refinamento.')
    br(); h('5. Manual de uso e reprodução')
    p('<b>Ambiente.</b> Python 3.13.18, NumPy 2.5.5 e Matplotlib 3.11.2. Dependências fixadas em requirements.txt. As bibliotecas numéricas são usadas para álgebra linear, gráficos e arquivos; o núcleo dos métodos e a busca estão implementados explicitamente. Não é necessário acesso ao repositório anterior para executar esta entrega.')
    p('Na pasta do projeto, em PowerShell:<br/>python -m venv .venv<br/>.venv/Scripts/python -m pip install -r requirements.txt<br/>.venv/Scripts/python codigo/testar.py<br/>.venv/Scripts/python codigo/executar.py','formula')
    p('Para reproduzir a análise adicional:<br/>.venv/Scripts/python codigo/executar.py --tol-f 0 --max-iter 20000 --saida resultados/parte2_refinamento --sem-graficos<br/>Para gerar o relatório e o notebook:<br/>.venv/Scripts/python codigo/preparar_entrega.py','formula')
    p('O último comando recria o notebook sem saídas; execute todas as células em seguida para repovoá-las. O notebook entregue já foi executado. Para executar em lote, instale o kernel no ambiente e use nbclient, conforme README.md. As células principais recalculam os 24 casos e os gráficos; as células de refinamento leem os dados já gerados.')
    p('<b>Entrada dos dados.</b> PROBLEMAS, em codigo/otimizacao.py, define função, gradiente, Hessiana de diagnóstico e ponto inicial. A reflexão é gerada por refletir; se todas as coordenadas forem zero, B recebe −1 em cada componente. Na CLI, --tol-grad, --tol-f, --max-iter e --saida controlam tolerâncias, limite e destino. A API Parametros também permite c_goldstein, passo_inicial, max_busca, curvatura_relativa e descida_relativa. Valores não finitos são rejeitados.')
    p('Exemplo individual em Python, na raiz do projeto:<br/>import sys; sys.path.insert(0, "codigo")<br/>from otimizacao import PROBLEMAS, Parametros, minimizar<br/>r = minimizar(PROBLEMAS["TP9"], "BFGS", [-1.2, 1.0], Parametros())<br/>print(r["status"], r["x_final"], r["norma_grad_final"])','formula')
    tabela([['Arquivo / status','Como ler'],['resumo.csv','Uma linha por execução: ponto final, objetivo, norma, iterações, avaliações e motivo.'],['TP*_Método_A/B.json[.gz]','Registro completo. Use json.load; para gzip, gzip.open(path,"rt",encoding="utf-8"). Arquivos grandes são compactados sem perda.'],['validacao.json / metadados.json','Testes, parâmetros, versões, contagem de casos e hashes do código.'],['gradiente','Norma dentro da tolerância; interpretar com as propriedades da função.'],['variacao_objetivo','Pequena mudança; não comprova mínimo nem tolerância de gradiente.'],['limite_iteracoes','Execução encerrada sem certificação de convergência.'],['falha_busca / valor_nao_finito / derivada_indefinida','Falha registrada com detalhe; tentativas disponíveis, sem fabricar passo.']],[190,301])
    br(); h('6. Responsabilidades e auditoria de IA')
    p('A matriz registra a distribuição de trabalhos declarada pelo usuário em 17/11/2026 e distingue o apoio da IA. As tarefas da Parte 1 são incluídas nessa declaração; as fichas não integram este relatório da Parte 2.')
    tabela([["Responsável","Contribuição"],["Tiago Oliveira Lima (564988)","Parte 1: seleção dos trabalhos nos Encontros Universitários e elaboração dos resumos 1, 3 e 5. Parte 2: definição do escopo junto ao assistente (P001–P003); conferência das derivadas analíticas do TP3 e do TP9 contra o catálogo da primeira atividade; conferência da busca de Goldstein recuperada da Atividade 1 e de seus parâmetros (c = 0,1, α inicial = 1); análise dos resultados do TP3 e do TP9 (simetria das trajetórias, ziguezague do gradiente, vale estreito); execução dos comandos do Manual de Uso para checar a reprodutibilidade."],["Noberto Frota Oliveira Nogueira (568044)","Parte 1: seleção dos trabalhos nos Encontros Universitários e elaboração dos resumos 2 e 4. Parte 2: conferência da atribuição de problemas e métodos (script de sorteio, semente 1133032) e dos pontos A/B; conferência das derivadas do TP14 e do TP16 e das referências analíticas (quatro mínimos do TP14, convexidade e Hessiana singular do TP16); revisão das salvaguardas do BFGS (condição de curvatura) e dos reinícios de Fletcher–Reeves; análise dos resultados do TP14 e do TP16 e redação da resposta à questão investigativa sobre bacias de atração; revisão do erro E001 e leitura final do relatório."],["IA (Codex)","Apoio na localização e conferência de fontes, recuperação da Goldstein, implementação dos métodos e derivadas, execução de testes e ensaios, geração de gráficos, notebook e relatório e correção de E001. As contribuições humanas foram declaradas pelo usuário."]],[115,376])
    p('<b>Prompts.</b> P001 (resumo fiel): ler o novo enunciado e adaptar as instruções, preservando registros de prompts e correções. P002 (resumo fiel): incorporar os arquivos de atribuição adicionados. P003 (literal): “resolva a parte 2 do trabalho [PNL_projeto_segundo_20262.pdf](PNL_projeto_segundo_20262.pdf)”. Identificação do colega fornecida pelo usuário, atualizada em 17/11/2026: Noberto Frota Oliveira Nogueira (568044). Os registros detalhados estão nos Markdown do projeto.')
    p('<b>E001 - validação de tolerância não finita.</b> Na primeira versão de minimizar, a IA validou tol_grad somente com tol_grad≤0. O teste com TP3, x0=(0,0,0) e tol_grad=NaN foi aceito e retornou falha_busca, tentando direção nula. Isso era incorreto: a entrada deve ser rejeitada antes da avaliação da função. Em aritmética IEEE, tanto NaN≤0 quanto 0≤NaN são falsas, de modo que o erro atravessava a validação e desativava a parada por gradiente.')
    p('A correção verifica np.isfinite em todos os parâmetros reais antes de comparar tolerâncias; valida também limites inteiros e faixas das salvaguardas. A regressão rejeita NaN, +inf e −inf nos seis parâmetros reais (18 casos). O teste estacionário com tolerância válida continua parando sem busca nem passo. Evidências preservadas: resultados/auditoria/E001_antes.json e E001_depois.json. O incidente foi de validação de entrada; não alterou derivadas nem os resultados com parâmetros finitos. As 48 execuções foram verificadas novamente com o código corrigido.')
    p('<b>Limites.</b> Dois pontos por problema não caracterizam integralmente as bacias. Não se garante convergência de FR somente com Goldstein. As quatro execuções do gradiente limitadas a 20.000 passos permanecem inconclusivas. O código não usa um método diferente para ocultar essa dificuldade. As fichas da Parte 1 não integram este relatório; a distribuição de tarefas foi informada pelo usuário.')
    h('Referências e evidências')
    p('[1] Ricardo Coelho. Segunda Atividade Computacional, fontes/PNL_projeto_segundo_20262.pdf, pp. 2-3. Fonte dos métodos, reflexão, parada e entregáveis.<br/>[2] Catálogo da Primeira Atividade, fontes/catalogo_primeira_atividade.pdf, pp. 4 (TP3), 5 (TP9), 6 (TP14 e TP16). Cópia e hashes em fontes/manifesto.json.<br/>[3] W. W. Hager; H. Zhang. A Survey of Nonlinear Conjugate Gradient Methods, versão revisada em 2005, §§2 e 4. <link href="https://people.clas.ufl.edu/hager/files/cg_survey.pdf" color="#24527a">people.clas.ufl.edu/hager/files/cg_survey.pdf</link>.<br/>[4] Implementação anterior de Goldstein: recorte preservado em fontes/goldstein_original.py.txt e origem registrada no manifesto. Igualdade sintática verificada localmente.','small')
    output=RAIZ/'output/pdf/relatorio_parte2.pdf'; output.parent.mkdir(parents=True,exist_ok=True)
    def rodape(canvas,doc):
        canvas.setFont('DejaVu',7)
        canvas.setFillColor(colors.HexColor('#526477'))
        canvas.drawString(52,28,'PNL · Parte 2 · Tiago Oliveira Lima e Noberto Frota Oliveira Nogueira · 16/11/2026')
        canvas.drawRightString(A4[0]-52,28,str(doc.page))
    doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=52,leftMargin=52,topMargin=42,bottomMargin=44,title='PNL - Parte 2: Métodos multidimensionais e reflexão',author='Tiago Oliveira Lima e Noberto Frota Oliveira Nogueira; apoio de IA declarado')
    doc.build(story,onFirstPage=rodape,onLaterPages=rodape)
    print('PDF:',output)


if __name__=='__main__':
    criar_notebook()
    criar_pdf()
