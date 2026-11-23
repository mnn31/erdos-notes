# Independent brute force: list windows (n,k), k in {3,4,5,6,7,10,11}, n+k-1 <= N, such that no prime
# p >= k divides any term exactly once ("rough-powerful" windows), and full hits (product powerful).
import sys
N=int(sys.argv[1]); KS=[3,4,5,6,7,10,11]
spf=list(range(N+1))
i=2
while i*i<=N:
    if spf[i]==i:
        for j in range(i*i,N+1,i):
            if spf[j]==j: spf[j]=i
    i+=1
ms=[0]*(N+1); fac=[None]*(N+1)
for m in range(2,N+1):
    x=m; best=0
    while x>1:
        p=spf[x]; e=0
        while x%p==0: x//=p; e+=1
        if e==1 and p>best: best=p
    ms[m]=best
out=[]
for k in KS:
    for n in range(1,N-k+2):
        if max(ms[n:n+k])<k:
            # full product check
            from collections import Counter
            c=Counter()
            for t in range(n,n+k):
                x=t
                while x>1:
                    p=spf[x]; x//=p; c[p]+=1
            full=all(v>=2 for v in c.values())
            out.append((n,k,full))
for n,k,f in sorted(out): print("RP",n,k,"FULL" if f else "")
