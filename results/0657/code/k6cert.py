# find target = d1*d4*(d1-d4) as Q-linear combination of 3x3 minors of G
import sympy as sp, itertools
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
import sys
for target in [d[1]*d[4]*(d[1]-d[4])]:
    target=sp.expand(target)
    # search single minors, then sparse combos via LP-ish: solve least-support by trying small subsets
    A=sp.Matrix([[sp.Poly(m,*d).coeff_monomial(mo) for (_,m) in mins] for mo in mons])
    b=sp.Matrix([sp.Poly(target,*d).coeff_monomial(mo) for mo in mons])
    for k in range(1,4):
        found=None
        for S in itertools.combinations(range(len(mins)),k):
            As=A[:,list(S)]
            try:
                sol,params=As.gauss_jordan_solve(b)
            except ValueError: continue
            found=(S,sol);break
        if found:
            S,sol=found
            print('support size',k)
            for s,c in zip(S,sol): print(' coeff',c,'minor rows',mins[s][0][0],'cols',mins[s][0][1])
            break
