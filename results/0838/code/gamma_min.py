# Rigorous (interval-arithmetic) verification of Lemma 11: gamma(rho) > gamma(1) for rho in (1, 20].
# Combined with symmetry gamma(1/rho)=gamma(rho) and the analytic bound for rho>=20 (Lemma 11(b)),
# this shows rho=1 is the unique minimiser of gamma on (0,inf).
import sympy as sp
from mpmath import iv, mp
iv.prec = 120; mp.prec = 120

y, r, t = sp.symbols('y r t', positive=True)
L2 = sp.log(2)
phi = lambda x: ((1+x)*sp.log(1+x) - x*sp.log(x))/L2
Phi = lambda x: ((1+x)**2/2*sp.log(1+x) - (1+x)**2/4 + sp.Rational(1, 4) - x**2/2*sp.log(x) + x**2/4)/L2
# symbolic sanity: Phi' = phi, Phi(0+) = 0
assert sp.simplify(sp.diff(Phi(y), y) - phi(y)) == 0
assert sp.limit(Phi(y), y, 0, '+') == 0
N = Phi(r) + r**2*Phi(1/r)
gam = N/phi(r)**2
g = gam.subs(r, sp.exp(t))
# evenness g(-t)=g(t) (Lemma 10), checked symbolically/numerically
assert abs(float((g - g.subs(t, -t)).subs(t, sp.Rational(37, 100)).evalf(50))) < 1e-40
g2 = sp.diff(g, t, 2)

from sympy.printing.pycode import MpmathPrinter
IVMOD = [{'log': iv.log, 'exp': iv.exp, 'mpf': iv.mpf, 'sqrt': iv.sqrt}]
def ivfun(var, expr):
    return sp.lambdify(var, expr, modules=IVMOD, printer=MpmathPrinter({'fully_qualified_modules': False}))
f_N = ivfun(r, N); f_phi = ivfun(r, phi(r)); f_g2 = ivfun(t, g2)

gam1 = f_N(iv.mpf(1)) / f_phi(iv.mpf(1))**2
print("gamma(1) enclosure:", gam1, " (1-1/(4ln2) =", 1 - 1/(4*mp.log(2)), ")")
G1hi = gam1.b

# Part A: on [1+delta, 20], N and phi are increasing in rho (Lemma 11(c)), so on [a,b]
# gamma >= N(a)/phi(b)^2.  Adaptive subdivision until the bound exceeds gamma(1).
delta = iv.mpf('0.05')
a0 = 1 + mp.mpf('0.05'); B = mp.mpf(20)
stack = [(a0, B)]; done = 0; maxdepth = 0
while stack:
    a, b = stack.pop()
    lo = (f_N(iv.mpf(a)) / f_phi(iv.mpf(b))**2).a
    if lo > G1hi:
        done += 1
    else:
        m = (a + b)/2
        assert b - a > mp.mpf('1e-12'), (a, b)
        stack.append((a, m)); stack.append((m, b))
print(f"Part A: [1.05, 20] covered by {done} intervals on each of which N(a)/phi(b)^2 > gamma(1): OK")

# Part B: g''(t) > 0 on [0, ln(1.05)] (interval evaluation on a uniform subdivision).
T = mp.log(mp.mpf('1.05')) * (1 + mp.mpf('1e-6'))
K = 400; minlo = None
for k in range(K):
    ta = T*k/K; tb = T*(k+1)/K
    if k == 0: ta = mp.mpf('1e-30')   # g'' is analytic at 0; avoid 0 only for log-free safety
    val = f_g2(iv.mpf([ta, tb]))
    assert val.a > 0, (k, val)
    minlo = val.a if minlo is None else min(minlo, val.a)
val0 = f_g2(iv.mpf([0, T/K]))
print(f"Part B: g''(t) > 0 on (0, ln 1.05]: min interval lower bound = {mp.nstr(minlo, 8)}; enclosure on [0,T/{K}]: {val0}")
print("ALL OK")
