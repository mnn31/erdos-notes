import numpy as np, pickle, itertools
from scipy.optimize import least_squares
reps=pickle.load(open('../out/nf7_reps.pkl','rb')); f=reps[0]
rng=np.random.default_rng(7)
pairs=[(m[0],e) for m in f for e in m[1:]]
def pts(z):
    c=z[:10]+1j*z[10:]
    return np.vstack([[0,0],[1,0],c.reshape(5,2)])
def sq(P,e): v=P[e[0]]-P[e[1]]; return v[0]**2+v[1]**2
def res(z):
    P=pts(z); r=np.array([sq(P,a)-sq(P,b) for a,b in pairs]); return np.concatenate([r.real,r.imag])
out=[]
for t in range(400):
    s=least_squares(res,rng.normal(size=20),xtol=1e-15,ftol=1e-15,gtol=1e-15)
    if np.max(np.abs(s.fun))<1e-11:
        P=pts(s.x); dv=np.array([sq(P,m[0]) for m in f])
        gap=min(abs(a-b) for a,b in itertools.combinations(dv,2)); mn=min(abs(dv))
        out.append((gap/max(abs(dv)),mn/max(abs(dv)),np.round(dv,4)))
out.sort(key=lambda o:-o[0]); print(len(out))
for o in out[:6]: print(o)
