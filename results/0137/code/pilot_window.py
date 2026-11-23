# Pilot: for all n <= N and all 3 <= k <= KMAX, is n(n+1)...(n+k-1) powerful?
# ms[m] = largest prime p with p || m (0 if m powerful). Window [n,n+k) can only be
# powerful if every term has ms < k (a prime >= k divides at most one term).
import sys
from sympy import factorint
N=int(sys.argv[1]); KMAX=int(sys.argv[2])
spf=list(range(N+KMAX+1))
i=2
while i*i<=N+KMAX:
    if spf[i]==i:
        for j in range(i*i,N+KMAX+1,i):
            if spf[j]==j: spf[j]=i
    i+=1
ms=[0]*(N+KMAX+1)
for m in range(2,N+KMAX+1):
    x=m; best=0
    while x>1:
        p=spf[x]; e=0
        while x%p==0: x//=p; e+=1
        if e==1 and p>best: best=p
    ms[m]=best
ms[1]=0
hits=[]; cand=0
for n in range(1,N+1):
    run_max=0
    for k in range(1,KMAX+1):
        v=ms[n+k-1]
        if v>run_max: run_max=v
        if k>=3 and run_max<k:
            cand+=1
            P=1
            for t in range(n,n+k): P*=t
            if all(e>=2 for e in factorint(P).values()):
                hits.append((n,k))
print("N",N,"KMAX",KMAX,"candidate windows",cand,"hits",hits)
