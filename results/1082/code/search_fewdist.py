# Numerical (heuristic, NOT a proof) search for convex k-gons with exactly d distinct
# intervertex distances. Used only to EXHIBIT candidates; Fishburn's count then shows completeness.
import numpy as np, sys, itertools
from scipy.optimize import least_squares
rng=np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 1)
k=int(sys.argv[1]); d=int(sys.argv[2])
pairs=list(itertools.combinations(range(k),2))
def res(z,assign):
    P=z[:2*k].reshape(k,2); c=np.concatenate([[1.0],z[2*k:]])
    return np.array([np.sum((P[i]-P[j])**2)-c[assign[t]] for t,(i,j) in enumerate(pairs)])
def convex(P):
    h=len(P); c=P.mean(0); ang=np.arctan2(P[:,1]-c[1],P[:,0]-c[0]); o=np.argsort(ang); Q=P[o]
    cr=[np.cross(Q[(i+1)%h]-Q[i],Q[(i+2)%h]-Q[(i+1)%h]) for i in range(h)]
    return all(x>1e-6 for x in cr) or all(x<-1e-6 for x in cr)
found={}
for trial in range(int(sys.argv[4]) if len(sys.argv)>4 else 4000):
    P=rng.normal(size=(k,2)); D2=np.array([np.sum((P[i]-P[j])**2) for i,j in pairs]); P/=np.sqrt(D2.min())
    cs=np.sort(rng.uniform(1,4,size=d-1))
    assign=np.zeros(len(pairs),int)
    for it in range(30):
        D2=np.array([np.sum((P[i]-P[j])**2) for i,j in pairs])
        c=np.concatenate([[1.0],cs]); assign=np.array([np.argmin(abs(x-c)) for x in D2])
        sol=least_squares(res,np.concatenate([P.ravel(),cs]),args=(assign,))
        P=sol.x[:2*k].reshape(k,2); cs=sol.x[2*k:]
    D=np.sqrt(np.array([np.sum((P[i]-P[j])**2) for i,j in pairs]))
    if D.min()<1e-3: continue
    D=D/D.min(); u=np.unique(np.round(D,7))
    if len(u)!=d or np.max(abs(sol.fun))>1e-9 or not convex(P): continue
    sig=tuple(np.round(np.sort(D),5))
    if sig not in found:
        found[sig]=P; print("FOUND",[round(x,8) for x in u],"multiplicities",[int(np.sum(abs(D-x)<1e-6)) for x in u]); sys.stdout.flush()
print("distinct classes found:",len(found))
