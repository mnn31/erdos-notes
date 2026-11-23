# phi(7) <= 9: certified 7-point configuration (Krawczyk existence proof + interval separation of distance classes)
import sympy as sp, itertools, json, sys
sys.path.insert(0,'.')
from krawczyk import certify, dist_check, overlap
x1,x2,A,B,u,v=zs=sp.symbols('x1 x2 A B u v')
P=[(x1,0),(x2,-A),(1,-A-B),(-x1,0),(-x2,-A),(-1,-A-B),(u,v)]
d2=lambda i,j: sp.expand((P[i][0]-P[j][0])**2+(P[i][1]-P[j][1])**2)
ch=(0,1,0)
forced=[]
for k,(i,j) in zip(range(3),[(1,2),(0,2),(0,1)]):
    forced.append(((k,k+3),(i,j)))
for k,(i,j) in zip(range(3),[(1,2),(0,2),(0,1)]):
    forced.append(((k+3*ch[k],6),(i,j+3)))
# reflection: |p_i p_j| = |p_i' p_j'| and |p_i p_j'| = |p_i' p_j| hold identically
eqs=[d2(*a)-d2(*b) for a,b in forced]
z0=[0.798162, -0.531418, 1.49406, -0.450565, 1.266744, 0.450565]
ok,X,z=certify(list(zs),eqs,z0,P,rad=1e-40)
print('Krawczyk inclusion verified:',ok)
print('root (30 digits):',[sp.N(str(t),30) for t in z])
Dd=dist_check(P,list(zs),X)
E=list(Dd)
# union-find over forced equalities and identically-equal pairs
par={e:e for e in E}
def f(e):
    while par[e]!=e: e=par[e]
    return e
def un(a,b): par[f(a)]=f(b)
for a,b in forced: un(tuple(sorted(a)),tuple(sorted(b)))
for a,b in itertools.combinations(E,2):
    if sp.expand(d2(*a)-d2(*b))==0: un(a,b)
classes={}
for e in E: classes.setdefault(f(e),[]).append(e)
classes=list(classes.values())
print('number of forced classes:',len(classes))
for c in classes: print(' ',c, [ (float(Dd[e].a)) for e in c][:1])
sep=all(not overlap(Dd[a],Dd[b]) for c1,c2 in itertools.combinations(classes,2) for a in c1 for b in c2)
print('distinct classes have disjoint distance intervals:',sep)
match=all(len(set(sum(c,())))==2*len(c) for c in classes)
print('every class is a matching (=> no isosceles triangle, degenerate included):',match)
minD=min(float(Dd[e].a) for e in E); print('min squared distance lower bound:',minD)
assert ok and sep and match and minD>0
json.dump({'variables':[str(s) for s in zs],'root_30_digits':[str(sp.N(str(t),30)) for t in z],
 'points':[[str(a),str(b)] for a,b in P],'equations':[str(e) for e in eqs],'classes':classes},open('../out/seven_points_9.json','w'),indent=1)
print('OK: 7 points, no isosceles, exactly',len(classes),'distinct distances')
