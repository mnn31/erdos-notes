# phi(5) <= 5: certified 5-point configuration realizing the near-1-factorization of K5 (Krawczyk).
import sympy as sp, itertools, numpy as np, json, sys
sys.path.insert(0,'.')
from krawczyk import certify, dist_check, overlap
from scipy.optimize import least_squares
a,b,c,e,g,h=zs=sp.symbols('a b c e g h')
X2=3   # extra normalisation (integer, so all coefficients are integers): p1=(10,0), p2=(3,a)
P=[(0,0),(10,0),(X2,a),(b,c),(e,g)]
zs=[a,b,c,e,g]
d2=lambda i,j: sp.expand((P[i][0]-P[j][0])**2+(P[i][1]-P[j][1])**2)
cls=[[tuple(sorted(((k+1)%5,(k-1)%5))),tuple(sorted(((k+2)%5,(k-2)%5)))] for k in range(5)]
eqs=[d2(*m[0])-d2(*m[1]) for m in cls]
fn=sp.lambdify(zs,eqs)
rng=np.random.default_rng(5); best=None
for t in range(3000):
    s=least_squares(lambda z: fn(*z),rng.normal(size=5)*20,xtol=1e-15,ftol=1e-15,gtol=1e-15)
    if np.max(np.abs(s.fun))<1e-12:
        Pn=np.array([[float(sp.sympify(u).subs(dict(zip(zs,s.x)))) for u in p] for p in P])
        D={q:np.sum((Pn[q[0]]-Pn[q[1]])**2) for q in itertools.combinations(range(5),2)}
        cv=sorted(D[m[0]] for m in cls); gap=min(y-x for x,y in zip(cv,cv[1:]))/max(cv)
        if best is None or gap>best[0]: best=(gap,s.x)
print('numeric best relative class gap',best[0])
ok,Xb,z=certify(zs,eqs,list(best[1]),P,rad=1e-40)
print('Krawczyk:',ok)
Dd=dist_check(P,zs,Xb)
classes=[[tuple(sorted(e)) for e in m] for m in cls]
sep=all(not overlap(Dd[x],Dd[y]) for c1,c2 in itertools.combinations(classes,2) for x in c1 for y in c2)
pos=min(float(Dd[q].a) for q in Dd)>0
print('classes separated:',sep,'all squared distances >0:',pos)
print('root:',[str(sp.N(str(t),25)) for t in z])
for cc in classes: print(cc, float(Dd[cc[0]].a))
assert ok and sep and pos
json.dump({'points':[[str(u) for u in p] for p in P],'vars':[str(s) for s in zs],'root_25':[str(sp.N(str(t),25)) for t in z],'classes':classes},open('../out/five_points.json','w'),indent=1)
print('OK: 5 points, no isosceles, 5 distinct distances')
