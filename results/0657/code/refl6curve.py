import numpy as np, itertools
from scipy.optimize import brentq
def F(x1,x2,x3=1.0):
    A2=4*x3**2-(x1-x2)**2; B2=4*x1**2-(x2-x3)**2; AB2=4*x2**2-(x1-x3)**2
    C=AB2-A2-B2
    return 4*A2*B2-C**2, A2,B2,AB2,C
def pts(x1,x2,x3=1.0):
    _,A2,B2,AB2,C=F(x1,x2,x3)
    A=np.sqrt(A2); B=np.sqrt(B2)*np.sign(C) # 2AB=C
    y1=0; y2=-A; y3=y2-B
    P=[(x1,y1),(x2,y2),(x3,y3),(-x1,y1),(-x2,y2),(-x3,y3)]
    return np.array(P)
def score(P):
    n=len(P); D={}
    for i,j in itertools.combinations(range(n),2): D[(i,j)]=np.sum((P[i]-P[j])**2)
    mn=min(D.values())
    iso=min(min(abs(D[(a,b)]-D[(a,c)]),abs(D[(a,b)]-D[(b,c)]),abs(D[(a,c)]-D[(b,c)])) for a,b,c in itertools.combinations(range(n),3))
    vals=sorted(D.values()); 
    cl=[]; 
    for v in vals:
        if not cl or abs(v-cl[-1][0])>1e-9: cl.append([v,1])
        else: cl[-1][1]+=1
    return iso/mn, cl
out=[]
for x1 in np.linspace(-3,3,601):
    xs=np.linspace(-3,3,2001)
    fv=[F(x1,x2)[0] if min(F(x1,x2)[1:4])>0 else np.nan for x2 in xs]
    for k in range(len(xs)-1):
        if np.isfinite(fv[k]) and np.isfinite(fv[k+1]) and fv[k]*fv[k+1]<0:
            x2=brentq(lambda t:F(x1,t)[0],xs[k],xs[k+1],xtol=1e-14)
            if min(F(x1,x2)[1:4])>0 and abs(x1)>1e-6 and abs(x2)>1e-6:
                P=pts(x1,x2); s,cl=score(P)
                out.append((s,x1,x2,len(cl)))
out.sort(reverse=True)
for o in out[:10]: print(o)
