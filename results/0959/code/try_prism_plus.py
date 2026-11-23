# numerical scan (exploration only): prism realisations + one point with >=2 unit neighbours
import numpy as np, itertools
w=np.exp(1j*np.pi/3)
best={}
for th in np.linspace(0.05,6.2,37):
  v=np.exp(1j*th)
  for fam in ('trans','rot'):
    base=[0,1,w,v,1+v,w+v] if fam=='trans' else [0,1,w,v,1+w*w*v,w+w**4*v]
    for (i,j) in itertools.combinations(range(6),2):
      s,t=base[i],base[j]; D=abs(t-s)
      if D>=2 or D<1e-9: continue
      for sg in (1,-1):
        mid=(s+t)/2; h=np.sqrt(max(0,1-D*D/4)); d=mid+sg*1j*(t-s)/D*h
        P=base+[d]
        ds=[abs(P[a]-P[b]) for a,b in itertools.combinations(range(7),2)]
        if min(ds)<1e-6: continue
        u=sum(abs(x-1)<1e-9 for x in ds); nu=[x for x in ds if abs(x-1)>1e-9]
        f2=max(sum(abs(y-x)<1e-9 for y in nu) for x in nu)
        k=(fam,i,j,sg); g=u-f2
        if g>best.get(k,(-1,))[0]: best[k]=(g,u,f2,round(th,3))
for k,vv in sorted(best.items(),key=lambda t:-t[1][0])[:12]: print(k,vv)
