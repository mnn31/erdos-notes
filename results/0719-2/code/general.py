# Checks for Theorem B (n = r+4) in WRITEUP.md. Exact integer arithmetic only.
# Run: python3 -I general.py
import itertools, math, random, sys
def C(n,k): return math.comb(n,k)
# (1) XOR construction of SQS(2^k): every triple of F_2^k in exactly one XOR-zero 4-set
for k in (3,4,5):
    N=2**k; cnt={}
    for q in itertools.combinations(range(N),4):
        if q[0]^q[1]^q[2]^q[3]==0:
            for tr in itertools.combinations(q,3): cnt[tr]=cnt.get(tr,0)+1
    ok = len(cnt)==C(N,3) and set(cnt.values())=={1}
    print(f"XOR SQS(2^{k}={N}): triples covered {len(cnt)}/{C(N,3)}, multiplicities {sorted(set(cnt.values()))}, exact={ok}")
# (2) mod-N packing P: 3-subsets of Z_N with sum = 0 mod N
for N in range(6,65):
    P=[t for t in itertools.combinations(range(N),3) if sum(t)%N==0]
    pairs=set(); good=True
    for t in P:
        for pr in itertools.combinations(t,2):
            if pr in pairs: good=False
            pairs.add(pr)
    b=len(P); D=C(N,3)
    assert good, N
    assert 6*b >= N*(N-3), N
    assert 4*b*(N-4) >= D, N
print("mod-N packings N=6..64: pairwise <=1 intersections, |P|>=N(N-3)/6, 4|P|(N-4)>=C(N,3): all OK")
print("  sizes:", {N: len([t for t in itertools.combinations(range(N),3) if sum(t)%N==0]) for N in (8,10,14,16)})
# polynomial 3N^2-25N+46 >= 0 for N>=6
assert all(3*N*N-25*N+46>=0 for N in range(6,10**4)); print("3N^2-25N+46>=0 for 6<=N<10^4 (and the polynomial is increasing for N>=5)")
# (3) find an SQS(10) and SQS(14) by exact-cover search, verify
def sqs(N, seed=0):
    rnd=random.Random(seed); T=list(itertools.combinations(range(N),3))
    covered=set(); blocks=[]
    sys.setrecursionlimit(10000)
    def rec():
        # pick first uncovered triple
        for t in T:
            if t not in covered: break
        else: return True
        cands=[x for x in range(N) if x not in t]; rnd.shuffle(cands)
        for x in cands:
            q=tuple(sorted(t+(x,))); trs=list(itertools.combinations(q,3))
            if any(s in covered for s in trs): continue
            for s in trs: covered.add(s)
            blocks.append(q)
            if rec(): return True
            blocks.pop()
            for s in trs: covered.discard(s)
        return False
    return blocks if rec() else None
for N in (10,):
    B=sqs(N)
    cnt={}
    for q in B:
        for tr in itertools.combinations(q,3): cnt[tr]=cnt.get(tr,0)+1
    print(f"SQS({N}) found: {len(B)} blocks, exact cover of all {C(N,3)} triples: {len(cnt)==C(N,3) and set(cnt.values())=={1}}")
    print("  blocks:", B)
