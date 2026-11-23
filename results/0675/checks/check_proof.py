# Independent checks for PROOF.md (run: python3 -I check_proof.py)
import math, numpy as np

def primes(n):
    s = bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2, int(n**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

def Esieve(L):
    E = np.zeros(L+1, dtype=bool)
    x = 0
    while x*x <= L:
        ys = np.arange(0, math.isqrt(L - x*x)+1)
        E[x*x + ys*ys] = True
        x += 1
    E[0] = False
    return E

# 1. Lemma A (conic count) and Lemma B (half-range witness) for p = 3 mod 4, p < PMAX
PMAX = 1500
E = Esieve(2*PMAX*PMAX)
worst = 0.0
for p in primes(PMAX):
    if p % 4 != 3: continue
    sq = [(x*x) % p for x in range(p)]
    cnt = [0]*p
    for x in range(p):
        for y in range(p):
            pass
    # count solutions of x^2+y^2=r via convolution of square counts
    c = [0]*p
    for v in sq: c[v] += 1
    for u in range(p):
        if c[u]:
            for v in range(p):
                if c[v]: cnt[(u+v) % p] += c[u]*c[v]
    assert all(cnt[r] == p+1 for r in range(1, p)), p
    half = (p-1)//2
    for r in range(1, p):
        w = None
        for y in range(1, half+1):
            t = (r - y*y) % p
            for x in range(0, half+1):
                if (x*x) % p == t: w = (x, y); break
            if w: break
        assert w is not None, (p, r)
        x, y = w
        a = x*x + y*y; b = x*x + (p-y)**2
        assert 1 <= a < b and E[a] and E[b]
        assert a % p == r and b % p == r and (b-a) % (p*p) != 0
        assert b <= 5*(p-1)**2/4
        worst = max(worst, b/(p*p))
print("Lemmas A,B verified for all p=3 mod 4 below", PMAX, "; max b/p^2 =", round(worst,4))

# 2. Brute force: minimal shift t_n for small n, and divisibility by 3, 7
L = 3*10**7
E = Esieve(L + 100)
ts = np.arange(1, L+1)
mask = np.ones(L, dtype=bool)
res = {}
for n in range(1, 41):
    mask &= (E[1+n: L+1+n] == E[n])  # condition for a=n: E[n+t]==E[n], t=1..L
    idx = np.flatnonzero(mask)
    res[n] = int(idx[0])+1 if idx.size else None
print("n, minimal t_n (searched t<=3e7), t mod 3, t mod 7:")
for n in range(1, 41):
    t = res[n]
    print(n, t, None if t is None else (t % 3, t % 7))
# predicted by Lemma C: 3 | t once n >= 5, 7 | t once n >= 45
for n in range(5, 41):
    if res[n] is not None: assert res[n] % 3 == 0, n
print("3 | t_n for all 5<=n<=40 with t_n found: OK")

# 3. theta(y;4,3)/y for a few y
for y in [10**4, 10**5, 10**6]:
    th = sum(math.log(q) for q in primes(y) if q % 4 == 3)
    print("theta(%d;4,3)/y = %.4f" % (y, th/y))

# 4. ALL shifts t<=3e7 (not only the minimal one): from which n are they all divisible by 3, by 7?
mask = np.ones(L, dtype=bool)
first_all = {3: None, 7: None}
for n in range(1, 32):
    mask &= (E[1+n: L+1+n] == E[n])
    idx = np.flatnonzero(mask) + 1
    for q in (3, 7):
        ok = bool(np.all(idx % q == 0))
        if ok and first_all[q] is None: first_all[q] = n
        if not ok: first_all[q] = None
print("least n0<=31 s.t. every n-shift t<=3e7 (n0<=n<=31) is divisible by q:", first_all)
# exact Lemma-7 threshold for p=3,7,11 (smallest n with two E-elements <=n in every nonzero class mod p, distinct mod p^2)
for p in (3, 7, 11, 19, 23):
    first = {}; thr = {}
    for m in range(1, 10**6):
        if not E[m] or m % p == 0: continue
        r = m % p
        if r in thr: continue
        if r not in first: first[r] = m % (p*p)
        elif m % (p*p) != first[r]: thr[r] = m
        if len(thr) == p-1: break
    print("p=%d exact threshold %d, bound 5(p-1)^2/4 = %.1f" % (p, max(thr.values()), 5*(p-1)**2/4))
