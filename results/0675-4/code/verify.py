# Independent checks for WRITEUP.md (pure Python + numpy). Run: python3 -I verify.py [path-to-merged-search-output]
import math, sys, random, functools
print = functools.partial(print, flush=True)
import numpy as np

def primes(n):
    s = bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2, int(n**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

def vp(m, p):
    k = 0
    while m % p == 0: m //= p; k += 1
    return k

def inE_factor(m):
    """m>=1: True iff every prime q=3 mod 4 divides m to an even power (trial division)."""
    q = 2
    while q*q <= m:
        if m % q == 0:
            k = 0
            while m % q == 0: m //= q; k += 1
            if q % 4 == 3 and k % 2: return False
        q += 1 if q == 2 else 2
    return not (m > 1 and m % 4 == 3)

def inE_bruteforce(m):
    x = 0
    while x*x <= m:
        y = math.isqrt(m - x*x)
        if x*x + y*y == m: return True
        x += 1
    return False

def Esieve(L):
    E = np.zeros(L+1, dtype=bool); x = 0
    while x*x <= L:
        ys = np.arange(0, math.isqrt(L-x*x)+1); E[x*x+ys*ys] = True; x += 1
    E[0] = False
    return E

# ---- 0. Lemma 0 (Fermat-Euler characterization) brute-force check
for m in range(1, 20001):
    assert inE_factor(m) == inE_bruteforce(m), m
print("[0] Lemma 0 (valuation characterization of E) agrees with brute force for 1<=m<=20000")

# ---- 1. verify claimed least shifts from the C search (n-shift property only, by factoring)
if len(sys.argv) > 1:
    rows = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
    best = {}
    for n, t in rows: best[n] = t
    for n, t in sorted(best.items()):
        for a in range(1, n+1):
            assert inE_factor(a) == inE_factor(a+t), (n, t, a)
        # and t fails for n+1 unless next row has the same t
    print("[1] every (n, t_n) in", sys.argv[1], "is an n-shift (checked by trial-division factorization);",
          "max n =", max(best))
    # minimality for t <= 3e7 by an independent numpy brute force
    L = 3*10**7; E = Esieve(L+200); mask = np.ones(L, dtype=bool); ok = 0
    for n in range(1, max(best)+1):
        mask &= (E[1+n:L+1+n] == E[n]); idx = np.flatnonzero(mask)
        tmin = int(idx[0])+1 if idx.size else None
        if tmin is not None:
            assert tmin == best[n], (n, tmin, best[n]); ok = n
        else:
            assert best[n] > L, (n, best[n])
    print("[1b] numpy brute force (t<=3e7) agrees with the C search on minimal shifts for n<=%d" % ok)
    for n, t in sorted(best.items()):
        if n == max(best) or best.get(n+1) != t:
            f = {}; m = t
            for p in primes(10**6):
                while m % p == 0: f[p] = f.get(p, 0)+1; m //= p
            print("    t = %d is the least shift for n up to %d ; factorization %s%s" %
                  (t, n, " * ".join("%d^%d" % (p, e) if e > 1 else str(p) for p, e in sorted(f.items())),
                   "" if m == 1 else " * %d" % m))

# ---- 2. Forcing lemma (Lemma 5/6 of the write-up): one-sided shifts of E cap [1,N]
L = 2*10**7; E = Esieve(L+3000)
Es = [a for a in range(1, 3000) if E[a]]
for N in [5, 8, 12, 16, 20, 24, 28]:
    mask = np.ones(L, dtype=bool)
    for a in Es:
        if a > N: break
        mask &= E[1+a:L+1+a]           # t in [1,L] with a+t in E
    ts = np.flatnonzero(mask)+1
    # predicted: q^(j+1) | t whenever the thresholds of Lemma 5 hold, for all q=3 mod 4
    for q in [p for p in primes(200) if p % 4 == 3]:
        e = 0
        while True:
            j = e
            thr = q**(j+1) if j % 2 == 1 else q**j * 5*(q-1)**2/4
            if thr <= N: e += 1
            else: break
        if e: assert np.all(ts % q**e == 0), (N, q, e)
    # largest n such that every one-sided t (<=L) is a genuine n-shift
    nmax = 0
    for n in range(1, N+1):
        bad = [b for b in range(1, n+1) if not E[b]]
        if all(np.all(~E[b + ts]) for b in bad): nmax = n
        else: break
    guaranteed = math.isqrt(int(4*N/5))
    print("[2] N=%5d: %7d one-sided t<=%.0e; forced prime powers verified; all are n-shifts for n<=%d (Lemma 6 guarantees n<=%d)"
          % (N, len(ts), L, nmax, guaranteed))
    assert nmax >= min(guaranteed, N)

# ---- 2b. Lemma 4 (witness pairs) for all q = 3 mod 4, q < 400
for q in [p for p in primes(400) if p % 4 == 3]:
    h = (q-1)//2
    for r in range(1, q):
        w = next(((x, y) for y in range(1, h+1) for x in range(0, h+1) if (x*x+y*y-r) % q == 0), None)
        assert w is not None, (q, r)
        x, y = w; a = x*x+y*y; b = x*x+(q-y)**2
        assert E[a] and E[b] and a % q == r == b % q and (b-a) % (q*q) and b <= 5*(q-1)**2/4
print("[2b] Lemma 4 witness pairs exist with b <= 5(q-1)^2/4 for all q = 3 mod 4 below 400 and all r != 0")

# ---- 3. Dickson construction (Theorem 2), carried out for small n: t = 4*M*x with all 1+4(M/a)x prime
def is_prime(m):
    if m < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29,31,37,41]:
        if m % p == 0: return m == p
    d, s = m-1, 0
    while d % 2 == 0: d //= 2; s += 1
    for b in [2,3,5,7,11,13,17,19,23,29,31,37,41]:   # deterministic below 3.3e24
        y = pow(b, d, m)
        if y in (1, m-1): continue
        for _ in range(s-1):
            y = y*y % m
            if y == m-1: break
        else: return False
    return True

def two_sq_prime(p):
    """p prime = 1 mod 4 -> (x,y) with x^2+y^2=p (Cornacchia / Hermite-Serret)."""
    for c in range(2, p):
        s = pow(c, (p-1)//4, p)
        if s*s % p == p-1: break
    a, b = p, s
    r = math.isqrt(p)
    while b > r: a, b = b, a % b
    y = math.isqrt(p - b*b); assert b*b + y*y == p
    return b, y

def two_sq(m):
    """explicit representation for m in E, by factoring (small m only)."""
    rep = (1, 0); q = 2
    def mul(u, v): return (abs(u[0]*v[0]-u[1]*v[1]), u[0]*v[1]+u[1]*v[0])
    while q*q <= m:
        while m % q == 0:
            m //= q
            if q == 2: rep = mul(rep, (1, 1))
            elif q % 4 == 1: rep = mul(rep, two_sq_prime(q))
            else:
                assert m % q == 0; m //= q; rep = mul(rep, (q, 0))
        q += 1
    if m > 1:
        if m == 2: rep = mul(rep, (1, 1))
        else: assert m % 4 == 1; rep = mul(rep, two_sq_prime(m))
    return rep

for n in range(1, 13):   # n=13 needs 8 simultaneous primes; too slow in pure Python
    M = 1
    for p in primes(n):
        e = 1
        while p**e <= n: e += 1
        M *= p**e
    A = [a for a in range(1, n+1) if inE_factor(a)]
    x = 1
    while not all(is_prime(1 + 4*(M//a)*x) for a in A): x += 1
    t = 4*M*x
    for a in range(1, n+1):
        if a in A:
            g = 1 + 4*(M//a)*x
            assert g % 4 == 1 and is_prime(g) and a*g == a+t
            u = two_sq(a); w = two_sq_prime(g)
            X, Y = abs(u[0]*w[0]-u[1]*w[1]), u[0]*w[1]+u[1]*w[0]
            assert X*X + Y*Y == a+t
        else:
            q = next(q for q in primes(a) if q % 4 == 3 and vp(a, q) % 2 == 1)
            assert vp(a+t, q) == vp(a, q)
    print("[3] n=%2d: |E cap [1,n]|=%d, M=%d, least x=%d, t=4Mx=%d is an n-shift (explicit two-square reps / odd q-valuations checked)"
          % (n, len(A), M, x, t))
