import math, itertools, bisect
def primes_upto(n):
    s=[True]*(n+1); s[0]=False
    if n>=1: s[1]=False
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=[False]*len(s[i*i::i])
    return [i for i in range(n+1) if s[i]]
PP=primes_upto(10000)
def pf(a):
    out=set();d=2
    while d*d<=a:
        while a%d==0: out.add(d);a//=d
        d+=1
    if a>1: out.add(a)
    return out
def construct(n,d):
    x=math.isqrt(n); N=sum(1 for q in PP if q<=x); m=N-d
    if m<1: return None
    p=lambda k: PP[k-1]
    r=[p(N+1+j) for j in range(m+1)]
    path=[]
    for i in range(1,m+1): path+=[r[m+1-i],p(i)]
    path.append(r[0])
    C=[path[0],path[-1]]+[path[k]*path[k+1] for k in range(len(path)-1)]
    if max(C)>n: return None
    A=set(C)|{q for q in PP if q<=n and q not in path}
    return N,m,path,sorted(A)
tested=0
for n in range(30,62):
    for d in range(0,4):
        c=construct(n,d)
        if not c: continue
        N,m,path,A=c
        Pn=[q for q in PP if q<=n]
        assert len(A)==len(Pn)+1
        fac=[pf(a) for a in A]
        minr=None
        for r in range(0,len(Pn)+1):
            if any(sum(1 for F in fac if F<=set(S))>r for S in itertools.combinations(Pn,r)):
                minr=r;break
        assert minr==2*m+1,(n,d,minr,m)
        tested+=1
print('exhaustive cases',tested)
# path-only check for larger n
t2=0
for n in [200,300,500,1000,2000,5000]:
    for d in range(0,3):
        c=construct(n,d)
        if not c: continue
        N,m,path,A=c
        if len(path)>17: continue
        Aset=set(A)
        Cel=[a for a in A if not (a in PP and a not in path)]
        fac=[pf(a) for a in Cel]
        for r in range(len(path)+1):
            for S in itertools.combinations(path,r):
                Ss=set(S); cnt=sum(1 for F in fac if F<=Ss)
                assert (cnt<=r) or r==len(path), (n,d,S)
        t2+=1
print('path-only cases',t2)
