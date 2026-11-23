import math, random, itertools, bisect
LIM=3_300_000
sv=bytearray([1])*(LIM+1); sv[0]=sv[1]=0
for i in range(2,int(LIM**.5)+1):
    if sv[i]: sv[i*i::i]=bytearray(len(sv[i*i::i]))
P=[i for i in range(LIM+1) if sv[i]]           # P[0]=2 = p_1
def pi(y): return bisect.bisect_right(P,int(y))
def p(k): return P[k-1]
def isqrt(n): return math.isqrt(n)
def min_d(n):
    x=isqrt(n); N=pi(x)
    assert p(2*N+1)<=3*math.sqrt(n), n
    # exact minimal d>=0 with p_i * p_{2N-d+2-i} <= n for i=1..m, m=N-d
    for d in range(0,N):
        m=N-d
        ok=all(p(i)*p(2*N-d+2-i)<=n for i in range(1,m+1))
        if ok: return d,N
    return None,N
def suff_d(n):
    x=isqrt(n); N=pi(x)
    M=max(2*N+2-j-pi(n//p(j)) for j in range(N+1,2*N+2))
    return max(0,M),N
def build(n,d):
    x=isqrt(n); N=pi(x); m=N-d
    r=[p(N+1+j) for j in range(m+1)]
    path=[]
    for i in range(1,m+1): path+= [r[m+1-i], p(i)]
    path.append(r[0])
    C=[path[0],path[-1]]+[path[k]*path[k+1] for k in range(len(path)-1)]
    return path,C
random.seed(1)
worst=0
for e in range(6,13):
    for _ in range(40):
        n=random.randint(10**e,10**(e+1)-1) if e<12 else random.randint(10**12,10**12)
        d0,N=min_d(n); d1,_=suff_d(n)
        assert d1>=d0, (n,d0,d1)
        path,C=build(n,d1)
        assert max(C)<=n and len(set(path))==len(path)==2*(N-d1)+1 and len(set(C))==len(C)
        x=math.sqrt(n)
        # explicit RH-derived bound (Lemma 6): d <= 4 + (3+sqrt3)/(8pi) sqrt(x) log(3x)
        bound=4+(3+math.sqrt(3))/(8*math.pi)*math.sqrt(x)*math.log(3*x)
        assert d1<=bound,(n,d1,bound)
        worst=max(worst,d1/(n**.25*math.log(n)))
    print(e,'ok worst ratio d_suff/(n^1/4 log n) so far',round(worst,4))
