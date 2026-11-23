import random, math
def sieve(n):
    b=bytearray([1])*(n+1); b[0]=b[1]=0
    for i in range(2,int(n**.5)+1):
        if b[i]: b[i*i::i]=bytearray(len(b[i*i::i]))
    return b
N=3_000_000
isp=sieve(N); primes=[i for i in range(N+1) if isp[i]]
# 1) C_small: max over 3<=q<20000 of least prime = 1 mod q
best=0;arg=None
for q in range(3,20000):
    p=q+1
    while p<=N and not isp[p]: p+=q
    assert p<=N
    if p>best: best=p;arg=q
print("C_small = max least prime 1 mod q, q<20000:",best,"at q=",arg)
# 2) Jacobi-character identity
def jacobi(a,n):
    assert n>0 and n%2==1
    a%=n; r=1
    while a:
        while a%2==0:
            a//=2
            if n%8 in (3,5): r=-r
        a,n=n,a
        if a%4==3 and n%4==3: r=-r
        a%=n
    return r if n==1 else 0
def legendre(a,p):
    v=pow(a%p,(p-1)//2,p); return 0 if v==0 else (1 if v==1 else -1)
def chi(D,n):
    eps=1 if D>0 else -1; m=abs(D); e=0
    while m%2==0: m//=2; e+=1
    assert n%2==1 and math.gcd(n,m)==1
    v=1
    if eps==-1: v*= (-1)**((n-1)//2)
    v*= ((-1)**((n*n-1)//8))**e
    v*= jacobi(n,m)
    v*= (-1)**(((n-1)//2)*((m-1)//2))
    return v
random.seed(1); bad=0; cnt=0
for _ in range(3000):
    D=random.choice([-1,1])*random.randint(1,10**7)
    q=8*abs(D)
    for p in random.sample(primes[1:5000],30):
        if q%p==0: continue
        cnt+=1
        if chi(D,p)!=legendre(D,p): bad+=1
    # homomorphism + periodicity spot check
    for _ in range(5):
        a=random.randrange(1,10**9)|1; b=random.randrange(1,10**9)|1
        if math.gcd(a,q)>1 or math.gcd(b,q)>1: continue
        assert chi(D,a)*chi(D,b)==chi(D,a*b)
        assert chi(D,a)==chi(D,a+q*random.randint(1,50))
print("chi(p)=Legendre checks:",cnt,"failures:",bad)
