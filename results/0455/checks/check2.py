import random, math, sys
sys.path.insert(0,'')
def sieve(n):
    b=bytearray([1])*(n+1); b[0]=b[1]=0
    for i in range(2,int(n**.5)+1):
        if b[i]: b[i*i::i]=bytearray(len(b[i*i::i]))
    return b
N=40_000_000
isp=sieve(N); small=[p for p in range(3,2000) if isp[p]]
def legendre(a,p):
    v=pow(a%p,(p-1)//2,p); return 0 if v==0 else (1 if v==1 else -1)
def pstar(D,A):  # least odd prime p, p∤A, with (D/p) != -1  (root exists)
    for p in small:
        if A%p==0: continue
        if legendre(D,p)!=-1: return p
# Theorem A runs: F(t)=x+t d+t(t-1)
worst=0; viol=0; runs=0
for x in range(3,200000,2):
    if not isp[x]: continue
    for d in range(2,3000,2):
        n=0
        while True:
            v=x+n*d+n*(n-1)
            if v>=N or not isp[v]: break
            n+=1
        if n>=3:
            runs+=1
            if x<=n: continue
            D=(d-1)**2-4*x; assert D%8==5
            ps=pstar(D,1)
            if not n<ps: viol+=1; print("VIOL",x,d,n,ps)
            worst=max(worst,n)
print("thmA runs n>=3:",runs,"violations:",viol,"max n:",worst)
# general QL with random a,b,c
viol=0;tests=0
random.seed(7)
for _ in range(400000):
    a=random.randint(1,60); b=random.randint(-300,300); c=random.randint(3,20000)
    n=0
    while True:
        v=a*n*n+b*n+c
        if v<=1 or v>=N or not isp[v]: break
        n+=1
    if n>=3 and min(a*t*t+b*t+c for t in range(n))>n:
        tests+=1
        D=b*b-4*a*c; ps=pstar(D,2*a)
        if not n<ps: viol+=1; print("VIOL",a,b,c,n,ps)
print("QL tests:",tests,"violations:",viol)
# block identity check
for _ in range(2000):
    h=random.randint(1,6); T=random.randint(2,8)
    blk=[random.randint(0,6)*2 for _ in range(h)]
    e=blk*(T+1); g=[random.randint(1,50)*2]
    for j in range(h*T): g.append(g[-1]+e[j])
    x=[random.randint(1,1000)*2+1]
    for j in range(h*T): x.append(x[-1]+g[j])
    E=sum(blk); M=sum((h-1-r)*blk[r] for r in range(h))
    for t in range(T+1):
        assert x[t*h]==x[0]+t*(h*g[0]+M)+h*E*t*(t-1)//2
print("block identity ok")
