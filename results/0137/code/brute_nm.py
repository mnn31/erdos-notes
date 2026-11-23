# Independent brute force for the validation dump: n with n+2 <= N such that some odd term T of
# (n,n+1,n+2) is powerful and the other two terms have no prime >= 11 dividing them exactly once.
import sys
N=int(sys.argv[1]); M=N+3
spf=list(range(M+1)); i=2
while i*i<=M:
    if spf[i]==i:
        for j in range(i*i,M+1,i):
            if spf[j]==j: spf[j]=i
    i+=1
ms=[0]*(M+1)
for m in range(2,M+1):
    x=m; best=0
    while x>1:
        p=spf[x]; e=0
        while x%p==0: x//=p; e+=1
        if e==1 and p>best: best=p
    ms[m]=best
for n in range(1,N-1):
    for T in (n,n+1,n+2):
        if T%2==1 and ms[T]==0 and all(ms[t]<11 for t in (n,n+1,n+2) if t!=T):
            print(n); break
