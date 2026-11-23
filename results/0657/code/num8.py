import numpy as np, pickle, itertools, sys
from scipy.optimize import least_squares
reps=pickle.load(open('../out/k7_8class_reps.pkl','rb'))
sh,nsh,starts=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
rng=np.random.default_rng(100+sh)
E=list(itertools.combinations(range(7),2))
for k in range(sh,len(reps),nsh):
    f=reps[k]
    pairs=[(m[0],e) for m in f for e in m[1:]]
    def res(z):
        Pp=np.vstack([[0,0],[1,0],z.reshape(5,2)])
        L=lambda e: np.sum((Pp[e[0]]-Pp[e[1]])**2)
        return np.array([L(a)-L(b) for a,b in pairs])
    best=(1e9,0,0)
    for t in range(starts):
        s=least_squares(res,rng.normal(size=10)*1.5,xtol=1e-14,ftol=1e-14,gtol=1e-14,max_nfev=400)
        Pp=np.vstack([[0,0],[1,0],s.x.reshape(5,2)])
        D=np.array([np.sum((Pp[a]-Pp[b])**2) for a,b in E]); mx=D.max()
        sc=np.max(np.abs(s.fun))/mx
        cv=sorted(np.mean([np.sum((Pp[e[0]]-Pp[e[1]])**2) for e in m]) for m in f)
        gap=min(b-a for a,b in zip(cv,cv[1:]))/mx
        if sc<1e-9 and gap>1e-5 and (sc,-gap)<(best[0],-best[1]): best=(sc,gap,D.min()/mx)
        if sc<1e-9 and gap>1e-5: best=max(best,(sc,gap,D.min()/mx),key=lambda b:b[1]) if best[0]<1e-9 else (sc,gap,D.min()/mx)
    print(k,'VALID' if best[0]<1e-9 else 'none',best,flush=True)
