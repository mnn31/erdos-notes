# numeric: reflection 6-point family (x3=1, curve F(x1,x2)=0) plus a 7th point q reusing the three size-2 classes
import numpy as np, itertools
from scipy.optimize import least_squares
rng=np.random.default_rng(3)
def six(x1,x2,x3=1.0):
    A2=4*x3**2-(x1-x2)**2; B2=4*x1**2-(x2-x3)**2; AB2=4*x2**2-(x1-x3)**2; C=AB2-A2-B2
    return A2,B2,AB2,C
def build(z):
    x1,x2,A,B,u,v=z
    # p1=(x1,0), p2=(x2,-A), p3=(1,-A-B); mirrors
    P=np.array([(x1,0),(x2,-A),(1,-A-B),(-x1,0),(-x2,-A),(-1,-A-B),(u,v)])
    return P
def dist2(P,i,j): return np.sum((P[i]-P[j])**2)
choices=list(itertools.product([0,1],repeat=3))
results=[]
for ch in choices:
    def res(z):
        P=build(z); r=[]
        # six-point merges: |p_k p_k'|^2 = |p_i p_j|^2
        for k,(i,j) in zip(range(3),[(1,2),(0,2),(0,1)]):
            r.append(dist2(P,k,k+3)-dist2(P,i,j))
        # q reuses class {p_i p_j', p_i' p_j} at vertex p_k or p_k'
        for k,(i,j) in zip(range(3),[(1,2),(0,2),(0,1)]):
            r.append(dist2(P,6,k+3*ch[k])-dist2(P,i,j+3))
        return np.array(r)
    for t in range(300):
        z0=np.concatenate([rng.normal(size=4)*1.5,rng.normal(size=2)*2])
        s=least_squares(res,z0,xtol=1e-15,ftol=1e-15,gtol=1e-15)
        if np.max(np.abs(s.fun))<1e-10:
            P=build(s.x)
            D={e:dist2(P,*e) for e in itertools.combinations(range(7),2)}
            mx=max(D.values())
            iso=min(min(abs(D[(a,b)]-D[(a,c)]),abs(D[(a,b)]-D[(b,c)]),abs(D[(a,c)]-D[(b,c)])) for a,b,c in itertools.combinations(range(7),3))/mx
            vals=sorted(D.values()); ncl=1+sum(1 for a,b in zip(vals,vals[1:]) if b-a>1e-8*mx)
            results.append((iso,ncl,ch,tuple(np.round(s.x,6))))
results.sort(reverse=True)
for r in results[:8]: print(r)
print(len(results))
