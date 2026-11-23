import sys, itertools, numpy as np; sys.path.insert(0,'.')
from graphs import *
from collections import Counter
w=np.exp(1j*np.pi/3)
for n,c in CODES.items():
    _,E=dec(c); T=triangles(n,E); C4=four_cycles(n,E)
    rows=[]
    for a,b,cc,d in C4:
        r=np.zeros(n,complex); r[a]+=1; r[cc]+=1; r[b]-=1; r[d]-=1; rows.append(r)
    R0=np.array(rows)
    cnt=Counter(); good=[]
    for bits in itertools.product([1,-1],repeat=len(T)-1):
        sig=(1,)+bits
        tr=[]
        for (a,b,cc),s in zip(T,sig):
            r=np.zeros(n,complex); r[cc]+=1; r[a]-=1; r[b]-=w**s; r[a]+=w**s; tr.append(r)
        M=np.vstack([R0,np.array(tr)])
        sv=np.linalg.svd(M,compute_uv=False)
        rank=int((sv>1e-9).sum()); k=n-rank
        # kernel
        _,_,Vh=np.linalg.svd(M); K=Vh[rank:].conj().T  # n x k
        # vanishing differences
        coll=any(np.linalg.norm(K[u]-K[v])<1e-9 for u in range(n) for v in range(u+1,n))
        cnt[(k,coll)]+=1
        if not coll: good.append((sig,k))
    print(n,len(T),dict(cnt))
    for g in good[:10]: print('   ',g)
