# Consistency check of Lemma 2 / Prop 13: for n <= 31, every n-shift t <= 2*10^7 is divisible by every
# prime p = 3 mod 4 with F*(p) <= n (F*(3)=5, F*(7)=26, F*(11)=50 from fstar.py).
# Run: python3 -I shift_check.py   (numpy, ~1 GB RAM peak, ~1 min)
import math, numpy as np
L = 2*10**7
E = np.zeros(L+64, dtype=bool)
for x in range(0, math.isqrt(L+63)+1):
    ys = np.arange(0, math.isqrt(L+63 - x*x)+1); E[x*x + ys*ys] = True
E[0] = False
Fstar = {3: 5, 7: 26, 11: 50}
mask = np.ones(L, dtype=bool)     # mask[t-1] : t is an n-shift
for n in range(1, 32):
    mask &= (E[1+n: L+1+n] == E[n])
    ts = np.flatnonzero(mask) + 1
    forced = [p for p, F in Fstar.items() if F <= n]
    for p in forced: assert np.all(ts % p == 0), (n, p)
    print("n=%2d  #shifts<=2e7: %8d  least: %s  forced primes %s divide all of them: OK"
          % (n, ts.size, ts[0] if ts.size else None, forced))

# Lemma 15 (prime powers): if k = v_p(t) then (k odd and p^(k+1) > n) or (k even and p^k * F*(p) > n).
def vp(t, p):
    k = 0
    while t % p == 0: t //= p; k += 1
    return k
mask = np.ones(L, dtype=bool)
for n in range(1, 32):
    mask &= (E[1+n: L+1+n] == E[n])
    ts = np.flatnonzero(mask) + 1
    for t in ts[:5000]:
        for p in (3, 7, 11):
            k = vp(int(t), p)
            assert (k % 2 == 1 and p**(k+1) > n) or (k % 2 == 0 and p**k * Fstar[p] > n), (n, t, p, k)
print("Lemma 15 (prime-power constraint) holds for p in {3,7,11} on all checked n-shifts, n <= 31")
