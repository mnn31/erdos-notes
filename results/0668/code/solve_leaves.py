# For each surviving leaf: reduce the unit-length conditions to equations in Z = lambda*conj(mu), solve exactly.
# Usage: python3 -I solve_leaves.py   (writes ../out/configs.json and prints a report)
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from graphs import *
from qw import *
from branch_enum import run
import sympy as sp

def solve2(L, R):
    """Solve 2x2 system over Q(w) given as L=[[a,b],[c,d]], R=[e,f]; return None if singular."""
    (a,b),(c,d)=L; det=sub(mul(a,d),mul(b,c))
    if iszero(det): return None
    di=inv(det)
    x=mul(di,sub(mul(d,R[0]),mul(b,R[1]))); y=mul(di,sub(mul(a,R[1]),mul(c,R[0])))
    return x,y

def analyse_leaf(n,E,T,sig,M):
    B=M.kernel()                      # 3 basis vectors (lists of length n over Q(w))
    k=len(B); assert k==3
    D={e:[sub(Bj[e[1]],Bj[e[0]]) for Bj in B] for e in E}   # edge functional on kernel coords
    # pick e1,e2 with independent functionals (2x2 minor nonzero)
    def indep(f,g):
        for i in range(3):
            for j in range(i+1,3):
                if not iszero(sub(mul(f[i],g[j]),mul(f[j],g[i]))): return (i,j)
        return None
    e1=E[0]; e2=next(e for e in E if indep(D[e1],D[e]))
    i,j=indep(D[e1],D[e2])
    # functional rank must be exactly 2 (translations in kernel): check every D[e] is a combination
    coef={}
    for e in E:
        sol=solve2([[D[e1][i],D[e2][i]],[D[e1][j],D[e2][j]]],[D[e][i],D[e][j]])
        assert sol is not None
        al,be=sol
        # verify on third coordinate (exact)
        m=3-i-j
        assert iszero(sub(D[e][m],add(mul(al,D[e1][m]),mul(be,D[e2][m])))), 'functional rank >2'
        coef[e]=(al,be)
    # vertex coefficients: p_v - p_0 = a_v*lam + b_v*mu ; derive from kernel likewise
    vc={}
    for v in range(n):
        f=[sub(Bj[v],Bj[0]) for Bj in B]
        al,be=solve2([[D[e1][i],D[e2][i]],[D[e1][j],D[e2][j]]],[f[i],f[j]])
        m=3-i-j; assert iszero(sub(f[m],add(mul(al,D[e1][m]),mul(be,D[e2][m]))))
        vc[v]=(al,be)
    # equations: |al|^2+|be|^2+2Re(Z al conj(be)) = 1, Z=U+iV, Vp = sqrt3*V
    # Re(Z*g) = U*re(g) - V*im(g) = U*re(g) - Vp*(g1/2)
    rows=[]
    for e in E:
        al,be=coef[e]; g=mul(al,conj(be))
        rows.append((2*re(g), -g[1], 1-norm(al)-norm(be)))   # cU*U + cV*Vp = rhs
    return e1,e2,coef,vc,rows

def sqdist_expr(a,b,U,Vp):
    # |a*lam+b*mu|^2 with |lam|=|mu|=1, lam*conj(mu)=Z
    g=mul(a,conj(b)); return norm(a)+norm(b)+2*(re(g)*U - Vp*g[1]/2)

TOY={5:'DR{',7:'FoSvw',9:'H{dQXgj',10:'IISpZATaw',12:'KwC[KLQIibDJ',20:'S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T['}
mode=sys.argv[1] if len(sys.argv)>1 else 'main'
CC=CODES if mode=='main' else {k:v for k,v in TOY.items() if k in (9,10,12,20)}
out={}
for n,c in CODES.items() if False else CC.items():
    _,E=dec(c)
    T,C4,M0,st,pl=run(n,E)
    print('='*70); print('n=%d, |E|=%d, leaves=%d'%(n,len(E),len(st['leaves'])))
    out[n]=[]
    for sig,M in st['leaves']:
        e1,e2,coef,vc,rows=analyse_leaf(n,E,T,sig,M)
        Us,Vs=sp.symbols('U Vp',real=True)
        eqs=set((sp.Rational(a.numerator,a.denominator)*Us+sp.Rational(b.numerator,b.denominator)*Vs
                 -sp.Rational(r.numerator,r.denominator)) for a,b,r in rows)
        eqs=[q for q in eqs if q!=0]
        lin=sp.linsolve(eqs,[Us,Vs])
        print(' leaf %s  base edges e1=%s e2=%s'%(''.join('+' if s>0 else '-' for s in sig),e1,e2))
        print('   distinct nontrivial linear equations in (U, Vp=sqrt3*ImZ):',eqs)
        print('   linear solution set:',lin)
        if not eqs:
            print('   NO equation on Z: every |Z|=1 gives a realisation of the edge lengths (one-parameter family)'); continue
        sols=sp.solve(eqs+[Us**2+Vs**2/3-1],[Us,Vs],dict=True)
        print('   with |Z|=1:',sols)
        for s in sols:
            U=s[Us]; Vp=s[Vs]
            # all squared distances exactly
            d2={}
            for u in range(n):
                for v in range(u+1,n):
                    a=sub(vc[v][0],vc[u][0]); b=sub(vc[v][1],vc[u][1])
                    gg=mul(a,conj(b))
                    expr=sp.nsimplify(0)+sp.Rational(norm(a)+norm(b))+2*(sp.Rational(re(gg))*U - Vp*sp.Rational(gg[1])/2)
                    d2[(u,v)]=sp.simplify(expr)
            Es=set(E)
            edges_ok=all(sp.simplify(d2[e]-1)==0 for e in E)
            minsep=min(d2.values(), key=lambda x: float(x))
            zero_pairs=[p for p,x in d2.items() if sp.simplify(x)==0]
            extra_unit=[p for p,x in d2.items() if p not in Es and sp.simplify(x-1)==0]
            print('   solution U=%s, Vp=%s (cos=%s, sin=%s): all edges unit: %s; coincident pairs: %s; extra unit pairs: %s; min sq-dist %s ~ %.6f'
                  %(U,Vp,U,sp.simplify(Vp/sp.sqrt(3)),edges_ok,zero_pairs,extra_unit,minsep,float(minsep)))
            out[n].append({'sigma':list(sig),'U':str(U),'Vp':str(Vp),
                           'vertex_coeffs':{str(v):[[str(x) for x in vc[v][0]],[str(x) for x in vc[v][1]]] for v in range(n)},
                           'sqdist':{'%d,%d'%p:str(x) for p,x in d2.items()},
                           'edges_ok':edges_ok,'coincident':zero_pairs,'extra_unit':extra_unit})
    sys.stdout.flush()
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','out','configs.json' if mode=='main' else 'configs_toy.json'),'w'),indent=1)
