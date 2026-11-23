"""Certified windows of the main proposition, with D(n) computed exactly.
Run: python3 -I code/window.py > out/window.txt   (about 1-2 min, ~200MB RAM)
For each n, Y = floor(sqrt(n/8)), D(n) = max_{m<=n} #{(x,y) in Z_{>=1}^2 : x^2+y^2 = m}.
Criterion (Prop. 9 in WRITEUP.md): p = 3 mod 4, p >= sqrt(n/2), and (p+1) Y^2 / p^2 >= kappa_p + 2 D(n)
  kappa_p = 2 sqrt(p)          (Weil, cited)            -> P_W(n)
  kappa_p = 3^(1/4) p^(3/4)    (Lemma 6, elementary)    -> P_K(n)
The criterion is monotone in p (LHS decreasing, RHS increasing), so it holds for all p in
[sqrt(n/2), P(n)] once it holds at P(n). Also printed: 1 + 2 sqrt(n/5) (PROOF.md part 1 range).
"""
import math
import numpy as np

NMAX = 10**8
rho = np.zeros(NMAX+1, np.uint16)
for x in range(1, math.isqrt(NMAX)+1):
    ys = np.arange(1, math.isqrt(NMAX - x*x)+1, dtype=np.int64)
    rho[x*x + ys*ys] += 1          # values distinct for fixed x, so no collisions
D = np.maximum.accumulate(rho)

def is_prime(m):
    if m < 2: return False
    if m % 2 == 0: return m == 2
    r = math.isqrt(m); f = 3
    while f <= r:
        if m % f == 0: return False
        f += 2
    return True

def largest_ok(n, kappa):
    Y = math.isqrt(n // 8)          # floor(sqrt(n/8)) (n//8 then isqrt is the same floor)
    Dn = int(D[n])
    lo = math.isqrt(n//2)
    while lo*lo*2 < n: lo += 1      # smallest integer >= sqrt(n/2)
    def ok(p): return (p+1)*Y*Y/(p*p) >= kappa(p) + 2*Dn
    if not ok(lo): return None, Y, Dn, lo
    a, b = lo, lo
    while ok(b): a, b = b, 2*b
    while b - a > 1:
        c = (a+b)//2
        if ok(c): a = c
        else: b = c
    p = a
    while p >= lo and not (p % 4 == 3 and is_prime(p)): p -= 1
    return (p if p >= lo else None), Y, Dn, lo

weil = lambda p: 2*math.sqrt(p)
klo = lambda p: 3**0.25 * p**0.75
print(f"{'n':>12} {'D(n)':>5} {'sqrt(n/2)':>10} {'1+2sqrt(n/5)':>12} {'sqrt n':>9} {'P_W(n)':>9} {'logP_W/logn':>11} {'P_K(n)':>9} {'logP_K/logn':>11}")
for n in [10**k for k in range(4, 9)] + [2*10**7, 5*10**7]:
    pw, Y, Dn, lo = largest_ok(n, weil)
    pk, *_ = largest_ok(n, klo)
    f = lambda q: f"{q:>9}" if q else f"{'none':>9}"
    g = lambda q: f"{math.log(q)/math.log(n):>11.4f}" if q else f"{'-':>11}"
    print(f"{n:>12} {Dn:>5} {math.sqrt(n/2):>10.1f} {1+2*math.sqrt(n/5):>12.1f} {math.sqrt(n):>9.1f} {f(pw)} {g(pw)} {f(pk)} {g(pk)}")
print("first n (multiples of 10^4, n <= 10^8) with P_W(n) > 1+2sqrt(n/5):")
for n in range(10**4, NMAX+1, 10**4):
    pw, *_ = largest_ok(n, weil)
    if pw and pw > 1 + 2*math.sqrt(n/5):
        print("  n =", n, "P_W =", pw); break
print("first n (multiples of 10^5, n <= 10^8) with P_K(n) > 1+2sqrt(n/5):")
for n in range(10**5, NMAX+1, 10**5):
    pk, *_ = largest_ok(n, klo)
    if pk and pk > 1 + 2*math.sqrt(n/5):
        print("  n =", n, "P_K =", pk); break
else:
    print("  none up to 10^8")
