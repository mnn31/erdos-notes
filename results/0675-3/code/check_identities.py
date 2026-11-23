# Exact checks of the algebraic identities used in WRITEUP.md (Lemmas 3-6).
# Run: python3 -I check_identities.py   (pure python + cmath; ~1 min)
import cmath, math, sys

def primes(n):
    s = bytearray([1])*(n+1); s[0] = s[1] = 0
    for i in range(2, int(n**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

def leg(a, p):
    a %= p
    if a == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

def kl(s, p, E):
    return sum(E[(x + s*pow(x, p-2, p)) % p] for x in range(1, p))

TOL = 1e-6
# Lemma 3: G(s) := sum_{N z = s} psi(Tr z) over F_p(i) equals -Kl(s), and
#          #{z : Tr z = a, N z = s} = 1 - leg(a^2-4s)
# Lemma 4: S_r(h,k) := sum_{x^2+y^2=r} psi(hx+ky) = -Kl(r(h^2+k^2)/4) for (h,k) != 0
for p in [3, 7, 11, 19, 23, 31, 43]:
    E = [cmath.exp(2j*math.pi*u/p) for u in range(p)]
    # elements z = x + i y; Tr z = 2x, N z = x^2 + y^2
    cnt = {}
    for x in range(p):
        for y in range(p):
            key = ((2*x) % p, (x*x + y*y) % p)
            cnt[key] = cnt.get(key, 0) + 1
    for a in range(p):
        for s in range(1, p):
            assert cnt.get((a, s), 0) == 1 - leg(a*a - 4*s, p), (p, a, s)
    K = [None] + [kl(s, p, E) for s in range(1, p)]
    for s in range(1, p):
        G = sum(E[(2*x) % p] for x in range(p) for y in range(p) if (x*x+y*y) % p == s)
        assert abs(G + K[s]) < TOL, (p, s)
    inv4 = pow(4, p-2, p)
    for r in range(1, p):
        pts = [(x, y) for x in range(p) for y in range(p) if (x*x+y*y) % p == r]
        assert len(pts) == p+1
        for h in range(p):
            for k in range(p):
                if h == 0 and k == 0: continue
                S = sum(E[(h*x + k*y) % p] for (x, y) in pts)
                s = (r*(h*h + k*k)*inv4) % p
                assert s != 0
                assert abs(S + K[s]) < TOL, (p, r, h, k)
    print("p=%d: trace-norm count, G=-Kl, S_r(h,k)=-Kl(r(h^2+k^2)/4) all verified" % p)

# Lemma 5: sum_{s != 0} |Kl(s)|^4 <= p^2 (3p - 5); report ratio to p^3 and max|Kl|/sqrt p
for p in [7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83, 101, 103, 107, 131, 199, 211, 307, 401, 499]:
    E = [cmath.exp(2j*math.pi*u/p) for u in range(p)]
    K = [kl(s, p, E) for s in range(1, p)]
    for k in K: assert abs(k.imag) < 1e-6
    m4 = sum(abs(k)**4 for k in K)
    assert m4 <= p*p*(3*p-5) + 1e-6, p
    print("p=%3d  sum|Kl|^4 / (p^2(3p-5)) = %.4f   max|Kl|/sqrt(p) = %.4f  (Weil: <= 2)"
          % (p, m4/(p*p*(3*p-5)), max(abs(k) for k in K)/math.sqrt(p)))

# Lemma 7: r_2(a) <= 4 d(a)^2, and primitive reps <= 4*2^omega(a), for a <= 2*10^5
A = 200000
r2 = [0]*(A+1); r2p = [0]*(A+1)
x = -math.isqrt(A)
for x in range(-math.isqrt(A), math.isqrt(A)+1):
    for y in range(-math.isqrt(A - x*x), math.isqrt(A - x*x)+1):
        a = x*x + y*y
        r2[a] += 1
        if math.gcd(x, y) == 1: r2p[a] += 1
d = [0]*(A+1); om = [0]*(A+1)
for i in range(1, A+1):
    for j in range(i, A+1, i): d[j] += 1
for q in primes(A):
    for j in range(q, A+1, q): om[j] += 1
for a in range(1, A+1):
    assert r2[a] <= 4*d[a]**2, a
    assert r2p[a] <= 4*2**om[a], a
print("r_2(a) <= 4 d(a)^2 and r_2^prim(a) <= 4*2^omega(a) verified for 1 <= a <=", A,
      "; max r_2/(4d^2) =", max(r2[a]/(4*d[a]**2) for a in range(1, A+1)))
