import numpy as np, pickle, itertools
from scipy.optimize import least_squares
reps=pickle.load(open('../out/nf7_reps.pkl','rb'))
rng=np.random.default_rng(1)
for k,f in enumerate(reps):
    def res(z):
        P=np.vstack([[0,0],[1,0],z.reshape(5,2)])
        L=lambda e: np.sum((P[e[0]]-P[e[1]])**2)
        r=[]
        for m in f: r+=[L(m[0])-L(m[1]),L(m[0])-L(m[2])]
        return np.array(r)
    best=[]
    for t in range(400):
        s=least_squares(res,rng.normal(size=10)*1.5,xtol=1e-15,ftol=1e-15,gtol=1e-15)
        P=np.vstack([[0,0],[1,0],s.x.reshape(5,2)])
        D=[np.sum((P[a]-P[b])**2) for a,b in itertools.combinations(range(7),2)]
        mn=min(D); sc=np.max(np.abs(s.fun))/mn
        cl=[np.mean([np.sum((P[e[0]]-P[e[1]])**2) for e in m]) for m in f]
        gap=min(abs(a-b) for a,b in itertools.combinations(cl,2))/max(cl)
        best.append((sc,gap,mn/max(D)))
    best.sort()
    print(k,'best scaled residuals',[ (round(a,9),round(b,4),round(c,4)) for a,b,c in best[:4]])
