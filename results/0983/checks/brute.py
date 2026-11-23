# Brute-force f(pi(n)+1,n) for tiny n using the Lean sInf definition and the Hall (max-min) form.
import itertools, math, sys
def primes_upto(n):
    s=[True]*(n+1); s[0:2]=[False,False][:n+1]
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=[False]*len(s[i*i::i])
    return [i for i in range(n+1) if s[i]]
def pf(a):
    out=set();d=2
    while d*d<=a:
        while a%d==0: out.add(d);a//=d
        d+=1
    if a>1: out.add(a)
    return frozenset(out)
for n in range(2,int(sys.argv[1])+1):
    P=primes_upto(n); k=len(P)+1; s=len([p for p in P if p*p<=n])
    if k>n: continue
    masks={}
    idx={p:i for i,p in enumerate(P)}
    def m(a): return sum(1<<idx[p] for p in pf(a))
    am=[m(a) for a in range(1,n+1)]
    Smasks=list(range(1<<len(P)))
    pc=[bin(x).count('1') for x in Smasks]
    adm_all=set(range(0,len(P)+1)); hall=0
    for A in itertools.combinations(range(n),k):
        best={}
        for S in Smasks:
            c=sum(1 for i in A if am[i]&~S==0)
            r=pc[S]
            if c>r: best[r]=True
        adm=set(best)
        adm_all&=adm
        hall=max(hall,min(adm))
    fl=min(adm_all) if adm_all else None
    print(n,'pi',len(P),'s',s,'f_lean',fl,'f_hall',hall,'2s+1',2*s+1)
