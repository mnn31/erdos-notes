import sympy as sp, itertools
d=sp.symbols('d0:5')
cls=lambda i,j:(3*(i+j))%5   # edge {i,j} of K5 on Z5 lies in M_k, k=(i+j)/2; M_k misses k
D=lambda i,j: 0 if i==j else d[cls(i,j)]
G=sp.Matrix(4,4,lambda a,b: sp.Rational(1,2)*(D(0,a+1)+D(0,b+1)-D(a+1,b+1)))
mins=[sp.expand(G.extract(list(r),list(c)).det()) for r in itertools.combinations(range(4),3) for c in itertools.combinations(range(4),3)]
GB=sp.groebner([m for m in mins if m!=0],*d,order='grevlex')
print(len(GB.exprs))
for g in GB.exprs: print(sp.factor(g))
