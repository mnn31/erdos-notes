# Independent exact re-verification of the realisations in ../out/configs.json, and congruence classes.
# Arithmetic in Q(sqrt33) as pairs of Fractions (a, b) = a + b*sqrt(33); no sympy simplification is used.
# Usage: python3 -I verify.py
import sys, os, json, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from graphs import *
from qw import mul as qmul, conj as qconj, norm as qnorm, re as qre, sub as qsub
import sympy as sp
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
import mpmath as mp
mp.mp.dps=50
def M(x): return mp.mpf(x.numerator)/x.denominator
S=sp.sqrt(33)
def to_q33(s):
    e=sp.sympify(s); e=sp.expand(e)
    b=e.coeff(S); a=sp.expand(e-b*S)
    assert a.is_rational and b.is_rational, s
    return (Fr(int(a.p),int(a.q)),Fr(int(b.p),int(b.q)))
def A(x,y): return (x[0]+y[0],x[1]+y[1])
def Mq(x,y): return (x[0]*y[0]+33*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def sc(r,x): return (r*x[0],r*x[1])
def sign(x):
    a,b=x
    # sign of a + b*sqrt33
    if b==0: return (a>0)-(a<0)
    if a==0: return (b>0)-(b<0)
    if (a>0)==(b>0): return 1 if a>0 else -1
    # opposite signs: compare a^2 with 33 b^2
    t=a*a-33*b*b
    if t==0: return 0
    return (1 if a>0 else -1) if t>0 else (1 if b>0 else -1)
def fr(s): return Fr(s)
mode=sys.argv[1] if len(sys.argv)>1 else 'main'
cfg=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','out','configs.json' if mode=='main' else 'configs_toy.json')))
if mode!='main': CODES={20:'S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T['}
report=[]
for n,c in CODES.items():
    _,E=dec(c); Es=set(E)
    sols=cfg[str(n)]
    D=[]
    print('='*60); print('n=%d: %d labelled realisations (one triangle orientation fixed, mod rotation+translation)'%(n,len(sols)))
    for k,s in enumerate(sols):
        U=to_q33(s['U']); Vp=to_q33(s['Vp'])
        # |Z|^2 = U^2 + Vp^2/3 must equal 1
        z2=A(Mq(U,U),sc(Fr(1,3),Mq(Vp,Vp)))
        assert z2==(1,0), z2
        vc={int(v):((fr(x[0][0]),fr(x[0][1])),(fr(x[1][0]),fr(x[1][1]))) for v,x in s['vertex_coeffs'].items()}
        d2={}
        for u in range(n):
            for v in range(n):
                if u==v: continue
                a=qsub(vc[v][0],vc[u][0]); b=qsub(vc[v][1],vc[u][1]); g=qmul(a,qconj(b))
                # |a lam + b mu|^2 = |a|^2+|b|^2+2(re(g) U - Vp g1/2)
                val=A(((qnorm(a)+qnorm(b)),Fr(0)), A(sc(2*qre(g),U), sc(-g[1],Vp)))
                d2[(u,v)]=val
        edges_unit=all(d2[e]==(1,0) for e in E)
        distinct=all(sign(d2[(u,v)])>0 for u in range(n) for v in range(u+1,n))
        nonedge_nonunit=all(d2[(u,v)]!=(1,0) for u in range(n) for v in range(u+1,n) if (u,v) not in Es)
        nunit=sum(1 for u in range(n) for v in range(u+1,n) if d2[(u,v)]==(1,0))
        # numeric coordinates: lam=1, mu=conj(Z)=U - i*Vp/sqrt3; p_v = a_v + b_v*mu  (a,b in Q(w))
        Un=M(U[0])+M(U[1])*mp.sqrt(33); Vn=(M(Vp[0])+M(Vp[1])*mp.sqrt(33))/mp.sqrt(3)
        mu=mp.mpc(Un,-Vn); w=mp.exp(1j*mp.pi/3)
        P=[ (M(vc[v][0][0])+M(vc[v][0][1])*w) + (M(vc[v][1][0])+M(vc[v][1][1])*w)*mu for v in range(n)]
        numerr=max(abs(abs(P[a]-P[b])-1) for a,b in E)
        minsep=min(abs(P[a]-P[b]) for a in range(n) for b in range(a+1,n))
        diam=max(abs(P[a]-P[b]) for a in range(n) for b in range(a+1,n))
        print(' realisation %d: |Z|=1 ok; all %d edges unit (exact): %s; all points distinct (exact): %s; non-edges non-unit (exact): %s; #unit pairs=%d; numeric max edge err %s; min sep %s; diam %s'
              %(k,len(E),edges_unit,distinct,nonedge_nonunit,nunit,mp.nstr(numerr,5),mp.nstr(minsep,12),mp.nstr(diam,15)))
        assert edges_unit and distinct and nonedge_nonunit and nunit==len(E)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','out','n%d_real%d.txt'%(n,k)),'w') as f:
            f.write('# n=%d realisation %d; vertex x y (40 digits); exact: p_v = a_v + b_v*mu, mu = U - i*Vp/sqrt3, U=%s, Vp=%s, a_v,b_v in Q(w) given as x+y*w\n'%(n,k,s['U'],s['Vp']))
            for v in range(n):
                f.write('%d %s %s   a=%s+%s*w b=%s+%s*w\n'%(v,mp.nstr(P[v].real,40),mp.nstr(P[v].imag,40),vc[v][0][0],vc[v][0][1],vc[v][1][0],vc[v][1][1]))
        D.append(d2)
    # congruence: realisations k,l give congruent point sets iff exists automorphism phi with d_k(phi u, phi v)=d_l(u,v)
    G=nx.Graph(E); auts=list(GraphMatcher(G,G).isomorphisms_iter())
    # D covers realisations with sigma_0=+; mirror images have identical distances, so congruence classes of point sets
    # = orbits of Aut on distance matrices.
    parent=list(range(len(D)))
    def find(x):
        while parent[x]!=x: x=parent[x]
        return x
    rel=[]
    for k in range(len(D)):
        for l in range(len(D)):
            for phi in auts:
                if all(D[k][(phi[u],phi[v])]==D[l][(u,v)] for u in range(n) for v in range(n) if u!=v):
                    rel.append((k,l)); parent[find(k)]=find(l); break
    classes=len({find(x) for x in range(len(D))})
    stab=[sum(1 for phi in auts if all(D[k][(phi[u],phi[v])]==D[k][(u,v)] for u in range(n) for v in range(n) if u!=v)) for k in range(len(D))]
    print(' |Aut G|=%d; pairs (k,l) related by an automorphism: %s'%(len(auts),sorted(set(rel))))
    print(' symmetry (stabiliser) sizes:',stab,' => number of congruence classes of point sets =',classes)
    report.append((n,len(D),len(auts),classes))
print(report)
