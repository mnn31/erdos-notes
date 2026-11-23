# Independent second check of the near-miss hits: sympy factorint of 2^k-1, Kummer carry count.
from sympy import factorint, isprime
def carries(a, b, p):
    c = cnt = 0
    while a or b or c:
        s = a % p + b % p + c
        c = 1 if s >= p else 0; cnt += c
        a //= p; b //= p
    return cnt
import json, sys
FAC = {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    if r['b'] == 2: FAC.setdefault(r['d'], []).extend(r['primes'])
def fac2(k):
    # factorization of 2^k-1 assembled from cyclotomic pieces, then verified by multiplication
    from sympy import divisors
    f = {}
    for d in divisors(k):
        for p in FAC[d]: f[p] = f.get(p, 0) + 1
    return f
hits = [(137, 16141961986503368055107762054812561012816), (149, 128187607486771957240347442690809417317798185),
        (227, 101300084359891653057791615262224317072042311693978602118916606877065),(67, 23206563898901803639), (101, 137177249633792241973877360183),
        (41, 285920731515), (11, 713), (9, 147), (4, 6)]
for k, j in hits:
    n = 2**k; i = 2
    f = factorint(n - 1) if k <= 101 else fac2(k)
    assert all(isprime(p) for p in f)
    prod = 1
    for p, e in f.items(): prod *= p**e
    assert prod == n - 1
    assert i < j <= n // 2
    # primes > i dividing C(n,2) = 2^(k-1)(2^k-1): exactly the primes of 2^k-1
    vp = {p: carries(j, n - j, p) for p in f}
    v2_cnj = carries(j, n - j, 2); v2_cn2 = carries(2, n - 2, 2)
    print(f"k={k} n=2^{k} j={j} 2^k-1={'*'.join(f'{p}^{e}' if e>1 else str(p) for p,e in sorted(f.items()))}"
          f" v_p(C(n,j))={vp} v_2(C(n,2))={v2_cn2} v_2(C(n,j))={v2_cnj}"
          f" gcd=2^{min(v2_cn2, v2_cnj)} near_miss={all(v == 0 for v in vp.values())}")
