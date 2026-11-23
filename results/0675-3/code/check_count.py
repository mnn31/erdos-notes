# Checks of the weighted conic count (Lemmas 8-10 of WRITEUP.md) for sample p, B.
# N(r) = sum_{|x|,|y|<B, x^2+y^2 = r mod p} (B-|x|)(B-|y|).
# Verifies: (i) N(r) equals the Fourier expansion with -Kl; (ii) |N(r) - (p+1)B^4/p^2| is below the
# pointwise bound 3^{1/4} p^{3/4} B^2, the Hoelder bound (3p^3)^{1/4} Wmax^{1/4} B^{3/2}, and the analytic
# bound on Wmax; (iii) reports the true max error / (sqrt p * B^2).
# Run: python3 -I check_count.py   (numpy; ~1 min)
import math, numpy as np

def dcount(A):
    d = np.zeros(A+1, dtype=np.int64)
    for i in range(1, A+1): d[i::i] += 1
    return d

def kl_all(p):
    x = np.arange(1, p)
    inv = np.array([pow(int(v), p-2, p) for v in x])
    K = np.zeros(p)
    for s in range(1, p):
        K[s] = np.cos(2*np.pi*((x + s*inv) % p)/p).sum()
    return K

for (p, B) in [(43, 8), (103, 20), (211, 40), (307, 60), (499, 100), (499, 200), (1019, 150), (1019, 400)]:
    assert p % 4 == 3 and 2*B - 1 <= p
    xs = np.arange(-B+1, B)
    w = (B - np.abs(xs)).astype(np.float64)
    # direct count
    N = np.zeros(p)
    sq = (xs*xs) % p
    for i, x2 in enumerate(sq):
        np.add.at(N, (x2 + sq) % p, w[i]*w)
    # Fourier side
    h = np.arange(p)
    D = np.array([np.exp(2j*np.pi*hh*np.arange(B)/p).sum() for hh in h])
    what = (np.abs(D)**2)/p
    assert abs(what.sum() - B) < 1e-6 and abs(what[0] - B*B/p) < 1e-9
    K = kl_all(p)
    inv4 = pow(4, p-2, p)
    hh, kk = np.meshgrid(h, h, indexing='ij')
    m = (hh*hh + kk*kk) % p
    Wgt = np.outer(what, what)
    main = (p+1)*B**4/p**2
    maxerr = 0; Wmax_all = 0
    for r in range(1, p):
        s = (r*m*inv4) % p
        Kv = np.where(m == 0, 0.0, K[s])
        F = main - (Wgt*Kv).sum() + Wgt[0, 0]*0  # (h,k)=(0,0) term is main; others carry -Kl
        assert abs(F - N[r]) < 1e-6*max(1, N[r]), (p, B, r, F, N[r])
        maxerr = max(maxerr, abs(N[r] - main))
        Wv = np.bincount(s[m != 0].ravel(), weights=Wgt[m != 0].ravel(), minlength=p)
        Wmax_all = max(Wmax_all, Wv.max())
    T = math.isqrt((p-1)//2)
    D2 = dcount(p)
    Dp = int((4*D2[1:p]**2).max())
    Wmax_bound = Dp*(B*B/p)**2 + 2*B*B/T
    point = 3**0.25 * p**0.75 * B*B
    hold = (3*p**3)**0.25 * Wmax_all**0.25 * B**1.5
    hold_an = (3*p**3)**0.25 * Wmax_bound**0.25 * B**1.5
    assert Wmax_all <= Wmax_bound + 1e-9 and maxerr <= hold + 1e-6 and maxerr <= point + 1e-6
    print("p=%4d B=%3d main=%10.1f max|err|=%9.1f  err/(sqrt(p)B^2)=%.3f  pointwise=%.3g  Hoelder(true Wmax)=%.3g  Hoelder(bound)=%.3g  Wmax=%.3g<=%.3g"
          % (p, B, main, maxerr, maxerr/(math.sqrt(p)*B*B), point, hold, hold_an, Wmax_all, Wmax_bound))
print("Fourier identity and all three error bounds verified on these (p,B).")
