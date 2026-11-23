# phi(6) >= 6: exact certificate.
# (1) all 1-factorizations of K6 are isomorphic to GK6 (labelled enumeration + explicit permutations)
# (2) polynomial identity  d1*d4*(d1-d4) = sum_k c_k * det(G[R_k,C_k])  for the Gram matrix G(d) of GK6,
#     checked (a) symbolically with sympy and (b) independently by exact Fraction evaluation on the grid {0,1,2,3}^5
#     (a polynomial of degree <=3 in each variable vanishing on S^5, |S|=4, is identically zero).
import itertools
from fractions import Fraction as Fr
n=6
E=[frozenset(e) for e in itertools.combinations(range(n),2)]
PM=[frozenset(m) for m in itertools.combinations(E,3) if len(set().union(*m))==6]
facts=[]
def rec(rem,ch):
    if not rem: facts.append(frozenset(ch)); return
    e=min(rem,key=sorted)
    for m in PM:
        if e in m and m<=rem: rec(rem-m,ch+[m])
rec(frozenset(E),[])
INF=5
GK6=frozenset(frozenset([frozenset({INF,k}),frozenset({(k+1)%5,(k-1)%5}),frozenset({(k+2)%5,(k-2)%5})]) for k in range(5))
act=lambda p,f: frozenset(frozenset(frozenset(p[v] for v in e) for e in m) for m in f)
orbit={act(p,GK6) for p in itertools.permutations(range(6))}
print('labelled 1-factorizations of K6:',len(facts),'; orbit of GK6 under S6:',len(orbit),'; equal sets:',set(facts)==orbit)
assert set(facts)==orbit and GK6 in orbit
cls=lambda i,j:(3*(i+j))%5
def Gram(d):  # d: list of 5 numbers; G_ij = x_i.x_j where x_i = p_i - p_inf
    return [[d[i] if i==j else Fr(d[i]+d[j]-d[cls(i,j)],2) for j in range(5)] for i in range(5)]
def det3(M): return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
CERT=[(Fr(1,3),(0,1,2),(0,1,2)),(Fr(-1,3),(0,1,2),(0,1,4)),(Fr(2,3),(0,1,2),(0,2,4)),(Fr(1,3),(0,1,2),(1,2,3)),
(Fr(1,3),(0,1,2),(1,2,4)),(Fr(-1,3),(0,1,3),(0,1,4)),(Fr(-2,3),(0,1,3),(0,3,4)),(Fr(-1,3),(0,1,3),(1,2,4)),
(Fr(-2,3),(0,1,3),(1,3,4)),(Fr(1,3),(0,1,3),(2,3,4)),(Fr(1,3),(0,1,4),(0,2,4)),(Fr(1,3),(0,1,4),(0,3,4)),
(Fr(-1,3),(0,2,4),(1,2,3)),(Fr(2,3),(0,2,4),(1,2,4)),(Fr(1,3),(0,2,4),(1,3,4)),(Fr(-1,3),(0,3,4),(0,3,4)),
(Fr(-1,3),(0,3,4),(1,3,4)),(Fr(-1,3),(0,3,4),(2,3,4)),(Fr(-2,3),(1,2,3),(1,2,4)),(Fr(2,3),(1,3,4),(2,3,4))]
bad=0
for d in itertools.product(range(4),repeat=5):
    G=Gram(list(d))
    s=sum(c*det3([[G[r][cc] for cc in C] for r in R]) for c,R,C in CERT)
    if s!=d[1]*d[4]*(d[1]-d[4]): bad+=1
print('grid check {0..3}^5 failures:',bad)
import sympy as sp
x=sp.symbols('d0:5')
Gs=sp.Matrix(5,5,lambda i,j: x[i] if i==j else sp.Rational(1,2)*(x[i]+x[j]-x[cls(i,j)]))
tot=sum(sp.Rational(c.numerator,c.denominator)*Gs.extract(list(R),list(C)).det() for c,R,C in CERT)
print('sympy: expand(sum - d1*d4*(d1-d4)) =',sp.expand(tot-x[1]*x[4]*(x[1]-x[4])))
assert bad==0
