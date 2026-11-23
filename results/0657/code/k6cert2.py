import sympy as sp, itertools, numpy as np
from scipy.optimize import linprog
d=sp.symbols('d0:5')
cls=lambda i,j:(3*(i+j))%5
G=sp.Matrix(5,5,lambda i,j: d[i] if i==j else sp.Rational(1,2)*(d[i]+d[j]-d[cls(i,j)]))
mins=[]
for r in itertools.combinations(range(5),3):
    for c in itertools.combinations(range(5),3):
        if r<=c:
            m=sp.expand(G.extract(list(r),list(c)).det())
            if m!=0: mins.append(((r,c),m))
mons=sorted(set().union(*[sp.Poly(m,*d).monoms() for _,m in mins]))
A=np.array([[float(sp.Poly(m,*d).coeff_monomial(mo)) for (_,m) in mins] for mo in mons])
target=sp.expand(d[1]*d[4]*(d[1]-d[4]))
b=np.array([float(sp.Poly(target,*d).coeff_monomial(mo)) for mo in mons])
N=len(mins); print('minors',N,'monomials',len(mons),'rank',np.linalg.matrix_rank(A))
res=linprog(np.ones(2*N),A_eq=np.hstack([A,-A]),b_eq=b,bounds=(0,None),method='highs')
x=res.x[:N]-res.x[N:]
S=[i for i in range(N) if abs(x[i])>1e-9]
print('LP support',len(S))
As=sp.Matrix([[sp.Poly(mins[s][1],*d).coeff_monomial(mo) for s in S] for mo in mons])
bs=sp.Matrix([sp.Poly(target,*d).coeff_monomial(mo) for mo in mons])
sol,params=As.gauss_jordan_solve(bs)
sol=sol.subs({p:0 for p in params})
tot=0
for s,c in zip(S,sol):
    print(c, mins[s][0]); tot+=c*mins[s][1]
print('check', sp.expand(tot-target))
