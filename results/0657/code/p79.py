import sympy as sp, numpy as np, pickle, itertools
reps=pickle.load(open('../out/k7_8class_reps.pkl','rb')); f=reps[79]
b1,b2,c1,c2,u,v=sy=sp.symbols('b1 b2 c1 c2 u v')
# centre origin; p0=(1,0)=a, p1=-a, p2=b, p3=-b, p5=c, p6=-c, p4=q
P={0:(1,0),1:(-1,0),2:(b1,b2),3:(-b1,-b2),5:(c1,c2),6:(-c1,-c2),4:(u,v)}
d2=lambda e: sp.expand((P[e[0]][0]-P[e[1]][0])**2+(P[e[0]][1]-P[e[1]][1])**2)
eqs=[]
for m in f:
    for e in m[1:]:
        r=sp.expand(d2(m[0])-d2(e))
        if r!=0: eqs.append(r)
print(len(eqs),'non-automatic equations')
for e in eqs: print(' ',e)
# numeric solution from the free search, mapped: centre=(0.5,0), scale 2
pts=np.array([[0,0],[1,0],[0.112443,0.022529],[0.887557,-0.022529],[0.602832,-0.489311],[0.601754,-0.374639],[0.398246,0.374639]])
pts=(pts-[0.5,0])*2; pts[:,0]*=-1  # p0 -> (1,0)
z0=[pts[2,0],pts[2,1],pts[5,0],pts[5,1],pts[4,0],pts[4,1]]
J=sp.Matrix(eqs).jacobian(sy)
fe=sp.lambdify(sy,eqs); print('residual at mapped point',np.max(np.abs(fe(*z0))))
Jn=np.array(sp.lambdify(sy,J)(*z0),dtype=float); print('Jacobian sing vals',np.linalg.svd(Jn,compute_uv=False))
import time
E=list(dict.fromkeys(eqs))
t=time.time(); GB=sp.groebner(E,*sy,order='grevlex'); print('GB',len(GB.exprs),time.time()-t)
for g in GB.exprs: print('  ',sp.factor(g))
