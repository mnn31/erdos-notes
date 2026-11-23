# Gram matrix for the GK6 1-factorization, based at vertex inf=5
import sympy as sp, itertools
d=sp.symbols('d0:5')
def cls(i,j):  # class of edge {i,j}, i,j in Z5
    return (3*(i+j))%5
G=sp.zeros(5,5)
for i in range(5):
    for j in range(5):
        G[i,j]= d[i] if i==j else sp.Rational(1,2)*(d[i]+d[j]-d[cls(i,j)])
print(G)
minors=set()
for r in itertools.combinations(range(5),3):
    for c in itertools.combinations(range(5),3):
        m=sp.expand(G.extract(list(r),list(c)).det())
        if m!=0: minors.add(m)
print(len(minors))
import time;t=time.time()
GB=sp.groebner(list(minors),*d,order='grevlex')
print('time',time.time()-t, len(GB.exprs))
for g in GB.exprs: print(sp.factor(g))
