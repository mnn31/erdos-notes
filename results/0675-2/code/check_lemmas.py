"""Numerical sanity checks for the lemmas in WRITEUP.md (675(a), beyond exponent 1/2).
Run: python3 -I code/check_lemmas.py > out/check_lemmas.txt
Checks (all exact or with float tolerance 1e-6):
 L3  : #{x^2+y^2=r} = p+1 (r!=0), =1 (r=0), p = 3 mod 4.
 L4  : g(u,0)^2 = -p for u != 0.
 L5  : C^(h) = -K(1, r*(h1^2+h2^2)/4) for all r != 0, h != 0 (small p: all r,h; larger p: sample).
 L6  : fourth-moment count T <= (p-1)(3p-5)  (brute force, small p), and max_c |K(1,c)| < 3^{1/4} p^{3/4}.
 W   : max_c |K(1,c)| <= 2 sqrt p (Weil; cited, checked here only numerically).
 L7  : sum_h |A_Y(h)|^2 = pY for 1<=Y<=p.
 L8  : rho(m) <= 2^{omega(m)} * #{g: g^2|m} <= d(m)^2, and rho(m) <= d(m), for m <= 10^6.
"""
import math, random
import numpy as np

def primes_upto(N):
    s = np.ones(N+1, bool); s[:2] = False
    for i in range(2, int(N**.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

P3 = [int(p) for p in primes_upto(3000) if p % 4 == 3]
random.seed(675)
ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False; print("FAIL", msg)

def e(x, p):
    return np.exp(2j*np.pi*(np.asarray(x) % p)/p)

# L3 and L4
for p in [q for q in P3 if q < 1000]:
    x = np.arange(p)
    sq = (x*x) % p
    cnt = np.bincount(((sq[:, None] + sq[None, :]) % p).ravel(), minlength=p)
    check(cnt[0] == 1 and np.all(cnt[1:] == p+1), f"L3 p={p}")
    for u in random.sample(range(1, p), min(p-1, 5)):
        g = e(u*sq, p).sum()
        check(abs(g*g + p) < 1e-6*p, f"L4 p={p} u={u}")
print("L3,L4 checked for p = 3 mod 4, p < 1000")

def kl_all(p):
    """K(1,c) for c = 0..p-1 (real)."""
    u = np.arange(1, p)
    inv = np.array([pow(int(v), p-2, p) for v in u])
    c = np.arange(p)
    # K(1,c) = sum_u cos(2 pi (u + c*inv(u))/p)  (imaginary part is 0)
    ph = (u[None, :] + c[:, None]*inv[None, :]) % p
    return np.cos(2*np.pi*ph/p).sum(axis=1)

# L5
for p in [q for q in P3 if q < 200]:
    x = np.arange(p); sq = (x*x) % p
    K = kl_all(p)
    inv4 = pow(4, p-2, p)
    rs = range(1, p) if p < 60 else random.sample(range(1, p), 6)
    for r in rs:
        pts = np.array([(a, b) for a in range(p) for b in range(p) if (sq[a]+sq[b]) % p == r])
        H = [(h1, h2) for h1 in range(p) for h2 in range(p) if (h1, h2) != (0, 0)]
        if p >= 60: H = random.sample(H, 200)
        H = np.array(H)
        Chat = e(-(H @ pts.T), p).sum(axis=1)
        Q = (H[:, 0]**2 + H[:, 1]**2) % p
        check(np.all(Q != 0), f"Q nonzero p={p}")
        pred = -K[(r*Q*inv4) % p]
        check(np.max(np.abs(Chat - pred)) < 1e-6*p, f"L5 p={p} r={r}")
print("L5 checked: p<60 all r,h; 60<p<200 sampled")

# L6 brute T
for p in [q for q in P3 if q < 50]:
    inv = [0]+[pow(v, p-2, p) for v in range(1, p)]
    from collections import Counter
    C = Counter(((a+b) % p, (inv[a]+inv[b]) % p) for a in range(1, p) for b in range(1, p))
    T = sum(v*v for v in C.values())
    check(T <= (p-1)*(3*p-5), f"T p={p} T={T}")
print("L6 fourth-moment count checked for p < 50")

# W and L6 bound
worst_w = 0; worst_k = 0
for p in P3:
    K = kl_all(p)
    m = np.max(np.abs(K[1:]))
    worst_w = max(worst_w, m/(2*math.sqrt(p)))
    worst_k = max(worst_k, m/(3**0.25*p**0.75))
    check(m <= 2*math.sqrt(p)+1e-6, f"Weil p={p}")
    check(m < 3**0.25*p**0.75, f"Kloosterman p={p}")
print(f"max_c|K(1,c)|/(2 sqrt p) over p=3 mod 4 < 3000: {worst_w:.6f}")
print(f"max_c|K(1,c)|/(3^(1/4) p^(3/4)) over p=3 mod 4 < 3000: {worst_k:.6f}")

# L7 Parseval
for p in [q for q in P3 if q < 400]:
    h = np.arange(p)
    for Y in sorted(set([1, 2, p//3, p//2, p-1, p])):
        if Y < 1: continue
        A = e(np.outer(h, np.arange(1, Y+1)), p).sum(axis=1)
        check(abs((np.abs(A)**2).sum() - p*Y) < 1e-6*p*Y, f"L7 p={p} Y={Y}")
print("L7 checked for p < 400")

# L8 representation counts
N = 10**6
rho = np.zeros(N+1, np.int64)
for xx in range(1, int(N**.5)+1):
    ys = np.arange(1, int(math.isqrt(N - xx*xx))+1)
    rho[xx*xx + ys*ys] += 1
d = np.zeros(N+1, np.int64)
for k in range(1, N+1):
    d[k::k] += 1
omega = np.zeros(N+1, np.int64)
for q in primes_upto(N):
    omega[q::q] += 1
sqd = np.zeros(N+1, np.int64)
for g in range(1, int(N**.5)+1):
    sqd[g*g::g*g] += 1
mm = np.arange(1, N+1)
b1 = (2**omega[1:])*sqd[1:]
check(np.all(rho[1:] <= b1), "rho <= 2^omega * #g")
check(np.all(b1 <= d[1:]**2), "2^omega*#g <= d^2")
check(np.all(rho[1:] <= d[1:]), "rho <= d")
print(f"L8 checked m <= {N}: max rho = {rho.max()} at m = {int(np.argmax(rho))}; max d^2 = {int((d[1:]**2).max())}")
print("ALL OK" if ok else "SOME CHECK FAILED")
