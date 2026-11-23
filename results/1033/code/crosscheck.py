"""Numerical cross-checks (NOT part of the proof):
 (1) face-enumeration value v(f,T) vs. multistart SLSQP on the relaxed polytope;
 (2) random + locally optimized search in the ORIGINAL 7-parameter butterfly space
     (d != e allowed, triangle types counted only if present) for violations of
        D <= max(alpha_b, (tau+2)^2/48).
"""
import sys; sys.path.insert(0, '.')
import numpy as np, sympy as sp
from scipy.optimize import minimize
from qpfaces import enumerate_faces, f, T, X
faces, _, G, DD = enumerate_faces(['a','b','c','us','u','C1','C2'], ())
lam = [(A, sp.lambdify((f, T), list(xs.values()), 'math')) for A, xs in faces]
gfun = sp.lambdify((*X, f, T), list(G.values()), 'math')
Dfun = sp.lambdify((*X, f), DD, 'math')
def v_faces(fv, Tv):
    best = -1
    for A, fn in lam:
        try: x = fn(fv, Tv)
        except ZeroDivisionError: continue
        if min(gfun(*x, fv, Tv)) >= -1e-12 and abs(sum(x[:4]) - 1) < 1e-9:
            best = max(best, Dfun(*x, fv))
    return best
def v_slsqp(fv, Tv, rng, starts=40):
    cons = [{'type': 'ineq', 'fun': (lambda x, i=i: gfun(*x, fv, Tv)[i])} for i in range(7)]
    cons.append({'type': 'eq', 'fun': lambda x: x[0] + x[1] + x[2] + x[3] - 1})
    best = -1
    for _ in range(starts):
        x0 = np.r_[rng.dirichlet(np.ones(4)), 0.0]; x0[4] = rng.random()*x0[3]
        r = minimize(lambda x: -Dfun(*x, fv), x0, constraints=cons, method='SLSQP', options={'ftol': 1e-14, 'maxiter': 500})
        if r.success and min(gfun(*r.x, fv, Tv)) > -1e-9: best = max(best, -r.fun)
    return best
rng = np.random.default_rng(7)
worst = 0
for k in range(150):
    fv, Tv = rng.random(), 0.4 + 0.6*rng.random()
    a1, a2 = v_faces(fv, Tv), v_slsqp(fv, Tv, rng)
    worst = max(worst, a2 - a1)
print(f"(1) max over 150 random (f,T) of [SLSQP value - face-enumeration value] = {worst:.3e}  (should be <= ~1e-9)")
# (2) original parametrisation
ab = 0.2501326600333574580318
def tau_D(p):
    a,b,c,d,e = p[:5]; fac, fde = p[5], p[6]
    da=b+fac*c+d+e; db=a+c; dc=b+fac*a; dd=a+fde*e; de=a+fde*d
    D = a*b+b*c+fac*a*c+a*d+a*e+fde*d*e
    sums = []
    if min(a,b,c) > 0 and fac > 0: sums.append(da+db+dc)
    if min(a,d,e) > 0 and fde > 0: sums.append(da+dd+de)
    return (max(sums) if sums else None), D
def viol(p):
    t, D = tau_D(p)
    if t is None: return D - 0.25
    return D - max(ab, (t+2)**2/48)
best = -1; bestp = None
for k in range(20000):
    w = rng.dirichlet(np.ones(5)*rng.choice([0.3, 1, 3])); p = np.r_[w, rng.random(2)]
    # randomly zero some parts / densities to explore degenerate strata
    if rng.random() < 0.2: p[rng.integers(0, 5)] = 0; p[:5] /= p[:5].sum()
    vv = viol(p)
    if vv > best: best, bestp = vv, p
print(f"(2a) best violation over 20000 random blow-ups: {best:.3e}")
def negviol(q):
    w = np.abs(q[:5]); w = w/w.sum(); p = np.r_[w, np.clip(q[5:], 0, 1)]
    return -viol(p)
from scipy.optimize import minimize as mz
bestl = -1
for k in range(300):
    q0 = np.r_[rng.dirichlet(np.ones(5)), rng.random(2)]
    r = mz(negviol, q0, method='Nelder-Mead', options={'xatol': 1e-12, 'fatol': 1e-15, 'maxiter': 4000})
    bestl = max(bestl, -r.fun)
print(f"(2b) best violation after 300 Nelder-Mead local searches: {bestl:.3e}  (proof says <= 0)")
