"""Parte 2 de PNL: funções e métodos explícitos, sem otimizadores prontos."""
from dataclasses import dataclass, asdict
import numpy as np
from busca_linear import goldstein


def tp3(x):
    u, v, w = x
    return u*u + 2*v*v + 3*w*w - 2*u*v


def grad3(x):
    u, v, w = x
    return np.array([2*u-2*v, 4*v-2*u, 6*w])


def hess3(x):
    return np.array([[2., -2., 0.], [-2., 4., 0.], [0., 0., 6.]])


def tp9(x):
    u, v = x
    return 1000*(v-u*u)**2 + (1-u)**2


def grad9(x):
    u, v = x
    r = v-u*u
    return np.array([-4000*u*r+2*(u-1), 2000*r])


def hess9(x):
    u, v = x
    return np.array([[12000*u*u-4000*v+2, -4000*u], [-4000*u, 2000.]])


def tp14(x):
    u, v = x
    if u == 0 or v == 0:
        return float('inf')
    return .1*(12+u*u+(1+v*v)/u**2+1/(u*u*v*v)+100/(u**4*v**4))


def grad14(x):
    u, v = x
    if u == 0 or v == 0:
        raise ValueError('TP 14 fora do domínio: eixos excluídos.')
    return .1*np.array([
        2*u-2*(1+v*v)/u**3-2/(u**3*v*v)-400/(u**5*v**4),
        2*v/u**2-2/(u*u*v**3)-400/(u**4*v**5)])


def hess14(x):
    u, v = x
    return .1*np.array([
        [2+6*(1+v*v)/u**4+6/(u**4*v*v)+2000/(u**6*v**4),
         -4*v/u**3+4/(u**3*v**3)+1600/(u**5*v**5)],
        [-4*v/u**3+4/(u**3*v**3)+1600/(u**5*v**5),
         2/u**2+6/(u*u*v**4)+2000/(u**4*v**6)]])


def tp16(x):
    u, v, w, z = x
    return (u+10*v)**2+5*(w-z)**2+(v-2*w)**4+10*(u-z)**4


def grad16(x):
    u, v, w, z = x
    a, b, c, d = u+10*v, w-z, v-2*w, u-z
    return np.array([2*a+40*d**3, 20*a+4*c**3,
                     10*b-8*c**3, -10*b-40*d**3])


def hess16(x):
    u, v, w, z = x
    a = np.array([1., 10., 0., 0.])
    b = np.array([0., 0., 1., -1.])
    c = np.array([0., 1., -2., 0.])
    d = np.array([1., 0., 0., -1.])
    return (2*np.outer(a,a)+10*np.outer(b,b)
            +12*(v-2*w)**2*np.outer(c,c)+120*(u-z)**2*np.outer(d,d))


@dataclass
class Problema:
    nome: str
    grupo: str
    f: object
    grad: object
    hess: object
    inicial: tuple


PROBLEMAS = {
    'TP3': Problema('TP3', 'G1', tp3, grad3, hess3, (1.,1.,1.)),
    'TP14': Problema('TP14', 'G2', tp14, grad14, hess14, (.5,.5)),
    'TP9': Problema('TP9', 'G2', tp9, grad9, hess9, (-1.2,1.)),
    'TP16': Problema('TP16', 'G3', tp16, grad16, hess16, (3.,-1.,0.,1.)),
}
METODOS = ('Gradiente', 'BFGS', 'FR')


@dataclass
class Parametros:
    tol_grad: float = 1e-5
    tol_f: float = 1e-7
    max_iter: int = 1000
    c_goldstein: float = .1
    passo_inicial: float = 1.
    max_busca: int = 100
    curvatura_relativa: float = 1e-10
    descida_relativa: float = 1e-12


def refletir(x):
    x = np.asarray(x, dtype=float)
    return -np.ones_like(x) if np.all(x == 0) else -x


class Avaliador:
    """Contagens separadas: funções e gradientes realmente calculados."""
    def __init__(self, problema):
        self.p = problema
        self.nf = self.ng = 0

    def f(self, x):
        self.nf += 1
        with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
            try:
                v = float(self.p.f(x))
            except (OverflowError, ZeroDivisionError):
                v = float('inf')
        return v if np.isfinite(v) else float('inf')

    def grad(self, x):
        self.ng += 1
        with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
            g = np.asarray(self.p.grad(x), dtype=float)
        if not np.isfinite(g).all():
            raise FloatingPointError('Gradiente não finito.')
        return g


class Linha:
    """Cache de f(x+alfa*d); guarda tentativas inclusive se a busca falhar."""
    def __init__(self, av, x, d, f0):
        self.av, self.x, self.d = av, x, d
        self.cache = {0.: f0}
        self.tentativas = []

    def __call__(self, alfa):
        alfa = float(alfa)
        if alfa not in self.cache:
            self.cache[alfa] = self.av.f(self.x+alfa*self.d)
        self.tentativas.append({'alfa': alfa, 'f': self.cache[alfa]})
        return self.cache[alfa]


def atualizar_bfgs(H, s, y, limite):
    """BFGS para INVERSA da Hessiana; omite atualização sem curvatura segura."""
    sy = float(s@y)
    escala = float(np.linalg.norm(s)*np.linalg.norm(y))
    if not np.isfinite(sy) or sy <= limite*escala or sy <= 0:
        return H, 'bfgs_omitida_curvatura'
    rho = 1/sy
    V = np.eye(len(s))-rho*np.outer(s,y)
    nova = V@H@V.T+rho*np.outer(s,s)
    nova = (nova+nova.T)/2
    if not np.isfinite(nova).all():
        return H, 'bfgs_omitida_nao_finita'
    try:
        np.linalg.cholesky(nova)
    except np.linalg.LinAlgError:
        return H, 'bfgs_omitida_nao_positiva'
    return nova, 'bfgs_atualizada'


def minimizar(problema, metodo, x0, parametros=None):
    """Uma execução independente. tol_f=0 desativa parada por variação.

    FR mantém beta = ||g_novo||²/||g_antigo||²; reinicia a cada n passos
    e se a direção perder descida. Estes reinícios são parte declarada
    da implementação, registrados em cada passo.
    """
    p = parametros or Parametros()
    if metodo not in METODOS:
        raise ValueError('Método desconhecido.')
    # NaN passa despercebido por testes como "tol <= 0". Validar finitude
    # antes de qualquer comparação ou avaliação evita falso diagnóstico de busca.
    reais = (p.tol_grad, p.tol_f, p.c_goldstein, p.passo_inicial,
             p.curvatura_relativa, p.descida_relativa)
    if not np.isfinite(reais).all():
        raise ValueError('Parâmetros reais devem ser finitos.')
    if not isinstance(p.max_iter, int) or not isinstance(p.max_busca, int):
        raise ValueError('Limites de iterações devem ser inteiros.')
    if not 0 <= p.curvatura_relativa < 1 or not 0 <= p.descida_relativa < 1:
        raise ValueError('Salvaguardas relativas devem pertencer a [0,1).')
    if p.tol_grad <= 0 or p.tol_f < 0 or p.max_iter < 0:
        raise ValueError('Tolerâncias/limite inválidos.')
    if not 0 < p.c_goldstein < .5 or p.max_busca < 1 or p.passo_inicial <= 0:
        raise ValueError('Parâmetros de busca inválidos.')
    x = np.array(x0, dtype=float, copy=True)
    if x.shape != (len(problema.inicial),) or not np.isfinite(x).all():
        raise ValueError('Ponto inicial com dimensão ou valores inválidos.')
    av = Avaliador(problema)
    f = av.f(x)
    traj, passos = [], []
    H = np.eye(len(x))
    d_anterior = g_anterior = None
    status, detalhe = 'limite_iteracoes', ''
    if np.isfinite(f):
        try:
            g = av.grad(x)
        except (ValueError, FloatingPointError) as erro:
            g = None
            status, detalhe = 'derivada_indefinida', str(erro)
    else:
        g = None
        status = 'valor_nao_finito'
    def registrar(k):
        traj.append({'k': k, 'x': x.tolist(), 'f': f,
                     'gradiente': None if g is None else g.tolist(),
                     'norma_grad': None if g is None else float(np.linalg.norm(g)),
                     'avaliacoes_f': av.nf, 'avaliacoes_g': av.ng})
    registrar(0)
    if g is not None:
        for k in range(p.max_iter+1):
            if np.linalg.norm(g) <= p.tol_grad:
                status = 'gradiente'
                break
            if k == p.max_iter:
                status = 'limite_iteracoes'
                break
            eventos, beta = [], None
            if metodo == 'Gradiente':
                d = -g
            elif metodo == 'BFGS':
                d = -H@g
            else:
                if k == 0 or k % len(x) == 0:
                    d = -g
                    eventos.append('fr_inicial' if k == 0 else 'fr_reinicio_periodico')
                else:
                    beta = float((g@g)/(g_anterior@g_anterior))
                    d = -g+beta*d_anterior
            gtd = float(g@d)
            if not np.isfinite(d).all() or gtd >= -p.descida_relativa*np.linalg.norm(g)*np.linalg.norm(d):
                d = -g
                eventos.append('reinicio_sem_descida')
                if metodo == 'BFGS':
                    H = np.eye(len(x))
                gtd = float(g@d)
            linha = Linha(av, x, d, f)
            passo = {'k': k, 'x': x.tolist(), 'direcao': d.tolist(),
                     'gTd': gtd, 'beta_fr': beta, 'eventos': eventos}
            try:
                r = goldstein(linha, gtd, p.c_goldstein, p.passo_inicial, p.max_busca)
            except (RuntimeError, ValueError, FloatingPointError) as erro:
                status, detalhe = 'falha_busca', str(erro)
                passo.update(status=status, tentativas=linha.tentativas)
                passos.append(passo)
                break
            alfa = r['alfa']
            novo_x, novo_f = x+alfa*d, r['valor']
            passo.update(alfa=alfa, goldstein=r, tentativas=linha.tentativas)
            if not np.isfinite(novo_x).all() or not np.isfinite(novo_f):
                status = 'valor_nao_finito'
                passo['status'] = status
                passos.append(passo)
                break
            try:
                novo_g = av.grad(novo_x)
            except (ValueError, FloatingPointError) as erro:
                status, detalhe = 'derivada_indefinida', str(erro)
                x, f, g = novo_x, novo_f, None
                registrar(k+1)
                passo['status'] = status
                passos.append(passo)
                break
            if metodo == 'BFGS':
                s, y = novo_x-x, novo_g-g
                H, evento = atualizar_bfgs(H, s, y, p.curvatura_relativa)
                eventos.append(evento)
                passo.update(s=s.tolist(), y=y.tolist(), sTy=float(s@y), H_seguinte=H.tolist())
            variacao = abs(novo_f-f)/max(1.,abs(f))
            g_anterior, d_anterior = g.copy(), d.copy()
            x, f, g = novo_x, novo_f, novo_g
            registrar(k+1)
            passo.update(status='aceito', variacao_relativa_f=variacao,
                         avaliacoes_f=av.nf, avaliacoes_g=av.ng)
            passos.append(passo)
            if np.linalg.norm(g) <= p.tol_grad:
                status = 'gradiente'
                break
            if p.tol_f > 0 and variacao <= p.tol_f:
                status = 'variacao_objetivo'
                break
    return {'problema': problema.nome, 'metodo': metodo, 'x0': list(map(float,x0)),
            'parametros': asdict(p), 'status': status, 'detalhe': detalhe,
            'iteracoes': len(traj)-1, 'x_final': x.tolist(), 'f_final': f,
            'norma_grad_final': None if g is None else float(np.linalg.norm(g)),
            'avaliacoes_f': av.nf, 'avaliacoes_g': av.ng,
            'trajetoria': traj, 'passos': passos}
