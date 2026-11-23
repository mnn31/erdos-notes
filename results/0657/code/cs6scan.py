import numpy as np
def check(a):
    a1,a2,a3=a
    g12=(a1+a2-4*a3)/2; g13=(a1+a3-4*a2)/2; g23=(a2+a3-4*a1)/2
    m=[a1*a2-g12**2,a1*a3-g13**2,a2*a3-g23**2]
    vals=[4*a1,4*a2,4*a3,2*a1+2*a2-4*a3,2*a1+2*a3-4*a2,2*a2+2*a3-4*a1]
    gap=min(abs(x-y) for i,x in enumerate(vals) for y in vals[i+1:])
    return min(a), min(m), min(vals), gap
best=[]
for t in np.linspace(0.01,20,20000):
    # cubic in a3 with a1=1,a2=t: -5 e1^3+20 e1 e2 -49 e3
    import numpy.polynomial.polynomial as P
    # build via sampling
    xs=np.array([0,1,2,3.]); 
    f=lambda a3: -5*(1+t+a3)**3+20*(1+t+a3)*(t+a3+t*a3)-49*t*a3
    c=np.polyfit(xs,[f(x) for x in xs],3)
    for r in np.roots(c):
        if abs(r.imag)<1e-12 and r.real>0:
            ok=check((1,t,r.real))
            if ok[0]>0 and ok[1]>0 and ok[2]>0: best.append((ok[3],t,r.real,ok))
best.sort(reverse=True); print(len(best)); print(best[:5])
