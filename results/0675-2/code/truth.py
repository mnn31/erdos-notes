"""Direct (brute-force) checks against the proposition.
Run: python3 -I code/truth.py > out/truth.txt   (well under a minute)
(1) Weighted count check: for several (n,p), compute N_w(r) = sum_{x,y in [2,2Y]} w(x)w(y) [x^2+y^2 = r mod p]
    exactly for every r != 0, with w(x) = #{(a,b) in [1,Y]^2 : a+b = x}, Y = floor(sqrt(n/8)), and compare with the
    proved lower bound Y^2 * ((p+1)Y^2/p^2 - kappa) using kappa = exact max_c |K(1,c)| (and Weil 2 sqrt p).
(2) True range: for n in a list, the largest P such that EVERY prime p = 3 mod 4 with sqrt(n/2) <= p <= P has
    >= 3 distinct elements of E cap [1,n] in every nonzero class mod p (so the contradiction argument applies),
    compared with the certified P_W(n) from window.py.
"""
import math
import numpy as np

def primes3(lo, hi):
    s = np.ones(hi+1, bool); s[:2] = False
    for i in range(2, int(hi**.5)+1):
        if s[i]: s[i*i::i] = False
    return [int(p) for p in np.nonzero(s)[0] if p >= lo and p % 4 == 3]

def kl_max(p):
    u = np.arange(1, p); inv = np.array([pow(int(v), p-2, p) for v in u])
    best = 0.0
    for c in range(1, p):
        best = max(best, abs(np.cos(2*np.pi*((u + c*inv) % p)/p).sum()))
    return best

print("(1) weighted counts: min_r N_w(r) vs proved lower bound")
for n, p in [(10**6, 983), (10**6, 1499), (10**7, 5179), (4*10**6, 2003)]:
    Y = math.isqrt(n//8)
    x = np.arange(2, 2*Y+1)
    w = Y - np.abs(x - (Y+1))                      # = #{a+b=x, 1<=a,b<=Y}
    assert w.min() >= 1 and w.max() == Y
    assert (2*Y)**2*2 <= n
    # distribution of x^2 mod p weighted by w
    f = np.bincount((x*x) % p, weights=w.astype(float), minlength=p)
    # N_w(r) = sum_{s+t=r} f(s) f(t): cyclic convolution mod p
    F = np.fft.fft(f); Nw = np.real(np.fft.ifft(F*F))
    km = kl_max(p)
    lb_exact = Y*Y*((p+1)*Y*Y/p**2 - km)
    lb_weil = Y*Y*((p+1)*Y*Y/p**2 - 2*math.sqrt(p))
    print(f"  n={n} p={p} Y={Y}: min_r N_w = {Nw[1:].min():.1f}, max_r N_w = {Nw[1:].max():.1f}, "
          f"main = {(p+1)*Y**4/p**2:.1f}, LB(kappa exact={km:.2f}) = {lb_exact:.1f}, LB(Weil) = {lb_weil:.1f}, "
          f"ok={Nw[1:].min() > lb_exact}")

print("(2) true range of 'every nonzero class mod p has >= 3 elements of E in [1,n]'")
for n in [10**4, 10**5, 10**6, 10**7]:
    inE = np.zeros(n+1, bool)
    for a in range(0, math.isqrt(n)+1):
        b = np.arange(a, math.isqrt(n - a*a)+1)
        inE[a*a + b*b] = True
    inE[0] = False
    Eel = np.nonzero(inE)[0]
    lo = math.isqrt(n//2)
    while 2*lo*lo < n: lo += 1
    P_true = None; first_bad = None
    for p in primes3(lo, n):
        cnt = np.bincount(Eel % p, minlength=p)
        if cnt[1:].min() >= 3:
            P_true = p
        else:
            first_bad = p; break
    print(f"  n={n}: sqrt(n/2)={math.sqrt(n/2):.1f}, n^(2/3)={n**(2/3):.1f}, all p in [sqrt(n/2), {P_true}] good; "
          f"first bad p = {first_bad} (log_n = {math.log(first_bad)/math.log(n):.4f})")
