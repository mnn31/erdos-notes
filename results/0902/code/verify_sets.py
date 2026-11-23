"""Exact brute-force S_4 check (no Lemma 2 reduction) of explicit connection sets.
Usage: python3 -I verify_sets.py m k r d K file   (file lines 'S: s1 s2 ...')
For each S: builds the full tournament x->y iff x^{-1}y in S on all n vertices, checks
S is a valid tournament connection set, then checks EVERY K-subset of vertices has a
common dominator outside it. Prints per-set verdict."""
import sys, itertools
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
def group(m,k,r,d):
    els=[(x,y,w) for x in range(m) for y in range(k) for w in range(d)]
    idx={e:i for i,e in enumerate(els)}
    def mul(a,b):
        (x1,y1,w1),(x2,y2,w2)=a,b
        return ((x1+pow(r,y1,m)*x2)%m,(y1+y2)%k,(w1+w2)%d)
    n=len(els); M=[[idx[mul(a,b)] for b in els] for a in els]
    inv=[next(j for j in range(n) if M[i][j]==0) for i in range(n)]
    return n,M,inv
def check(n,M,inv,S,K):
    Ss=set(S)
    assert 0 not in Ss and len(Ss)==(n-1)//2
    assert all((inv[g] in Ss)!=(g in Ss) for g in range(1,n)), "not a tournament set"
    inn=[0]*n
    for z in range(n):
        for v in range(n):
            if M[inv[z]][v] in Ss: inn[v]|=1<<z
    full=(1<<n)-1; bad=0
    for A in itertools.combinations(range(n),K):
        b=full
        for v in A: b&=inn[v]
        if b==0: bad+=1
    return bad
m,k,r,d,K=map(int,sys.argv[1:6])
n,M,inv=group(m,k,r,d)
for line in open(sys.argv[6]):
    if not line.startswith('S:'): continue
    S=list(map(int,line.split()[1:]))
    bad=check(n,M,inv,S,K)
    print(("S_%d HOLDS" if bad==0 else "S_%d FAILS (%d undominated %d-sets)")%((K,) if bad==0 else (K,bad,K)), "S=",S, flush=True)
