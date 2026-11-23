# Independent numerical cross-check (NOT part of the proof): random-start least squares for unit-distance
# realisations of each graph; report the distinct congruence signatures (sorted distance multiset) found.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import least_squares
from graphs import *
rng=np.random.default_rng(12345)
tries=int(sys.argv[1]) if len(sys.argv)>1 else 3000
only=[int(x) for x in sys.argv[2:]] or list(CODES)
for n,c in CODES.items():
    if n not in only: continue
    _,E=dec(c); E=np.array(E); iu=np.triu_indices(n,1)
    def res(x):
        P=x.reshape(n,2); d=P[E[:,0]]-P[E[:,1]]; return (d**2).sum(1)-1
    sigs=[]; conv=0; inj=0
    for t in range(tries):
        r=least_squares(res,rng.normal(size=2*n)*1.2,xtol=1e-15,ftol=1e-15,gtol=1e-15,max_nfev=3000)
        if np.max(np.abs(r.fun))>1e-10: continue
        conv+=1
        P=r.x.reshape(n,2); D=np.sqrt(((P[:,None]-P[None])**2).sum(-1))[iu]
        if D.min()<1e-3: continue
        inj+=1
        s=np.sort(D)
        if not any(np.max(np.abs(s-q))<1e-6 for q in sigs): sigs.append(s)
    print('n=%d tries=%d converged=%d injective=%d distinct congruence signatures=%d'%(n,tries,conv,inj,len(sigs)),
          [(round(q.min(),6),round(q.max(),6),int((np.abs(q-1)<1e-7).sum())) for q in sigs])
    sys.stdout.flush()
