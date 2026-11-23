import numpy as np, pickle, itertools, sys
from scipy.optimize import least_squares
reps=pickle.load(open('../out/k7_8class_reps.pkl','rb'))
E=list(itertools.combinations(range(7),2))
for k in map(int,sys.argv[1:]):
    f=reps[k]; print('pattern',k,[ [tuple(e) for e in m] for m in f])
    pairs=[(m[0],e) for m in f for e in m[1:]]
    def res(z):
        Pp=np.vstack([[0,0],[1,0],z.reshape(5,2)])
        L=lambda e: np.sum((Pp[e[0]]-Pp[e[1]])**2)
        return np.array([L(a)-L(b) for a,b in pairs])
    rng=np.random.default_rng(1); sols=[]
    for t in range(300):
        s=least_squares(res,rng.normal(size=10)*1.5,xtol=1e-15,ftol=1e-15,gtol=1e-15)
        Pp=np.vstack([[0,0],[1,0],s.x.reshape(5,2)])
        D=np.array([np.sum((Pp[a]-Pp[b])**2) for a,b in E]); mx=D.max()
        if np.max(np.abs(s.fun))/mx<1e-12:
            cv=sorted(np.mean([np.sum((Pp[e[0]]-Pp[e[1]])**2) for e in m]) for m in f)
            gap=min(b-a for a,b in zip(cv,cv[1:]))/mx
            if gap>1e-6:
                J=np.linalg.svd(np.array([ (res(s.x+1e-6*np.eye(10)[i])-res(s.x-1e-6*np.eye(10)[i]))/2e-6 for i in range(10)]).T,compute_uv=False)
                sols.append((gap,Pp,np.array(cv)/mx,J))
    sols.sort(key=lambda s:-s[0]); print(' valid sols',len(sols))
    if sols:
        g,Pp,cv,J=sols[0]; print(' gap',g); print(' points\n',np.round(Pp,6)); print(' class values/max',np.round(cv,6)); print(' jac sing vals',np.round(J,8))
        # collinearity / symmetry check
        c=Pp-Pp.mean(0); print(' second singular value of centered pts',np.linalg.svd(c,compute_uv=False))
