"""Exact KKT/face enumeration for the reduced butterfly program.

Variables x=(a,b,c,s,u), parameters f (density on ac) and T (= t-1, t = triangle-sum level).
D = ab + bc + f*a*c + a*s + u*s/4,   a+b+c+s = 1.
Inequalities g >= 0:
  a, b, c >= 0;  us: s-u >= 0;  u >= 0;
  C1: T - b - f(a+c) >= 0      (abc triangle sum <= 1+T)
  C2: T - a + (1-f)c - u >= 0  (ade triangle sum <= 1+T)
For an active set A, solve the Lagrange system of D on {sum=1, g_i=0 (i in A)} exactly.
"""
import sympy as sp, itertools
f, T = sp.symbols('f T')
a, b, c, s, u = X = sp.symbols('a b c s u')
D = a*b + b*c + f*a*c + a*s + u*s/4
GALL = {'a': a, 'b': b, 'c': c, 'us': s - u, 'u': u,
        'C1': T - b - f*(a + c), 'C2': T - a + (1 - f)*c - u}
MF = (T + 3)**2/48   # Fan: max density at level t = 1+T

def enumerate_faces(ineqs, forced=(), fval=None, maxsize=4):
    """Return list of (A, xs) for active sets A (containing `forced`) whose KKT system has
    a unique x-solution (as rational functions of f,T). If fval is given, f is substituted."""
    G = {k: GALL[k] for k in ineqs}
    DD = D if fval is None else D.subs(f, fval)
    if fval is not None:
        G = {k: v.subs(f, fval) for k, v in G.items()}
    out = []; skipped = []
    others = [k for k in ineqs if k not in forced]
    for r in range(0, maxsize + 1 - len(forced)):
        for extra in itertools.combinations(others, r):
            A = tuple(forced) + extra
            mus = sp.symbols('m0:%d' % (len(A) + 1))
            L = DD - mus[0]*(a + b + c + s - 1) - sum(mus[i+1]*G[n] for i, n in enumerate(A))
            eqs = [sp.diff(L, v) for v in X] + [a + b + c + s - 1] + [G[n] for n in A]
            unk = list(X) + list(mus)
            M, rhs = sp.linear_eq_to_matrix(eqs, unk)
            sol = sp.linsolve((M, rhs), unk)
            if sol == sp.EmptySet or len(sol) == 0:
                skipped.append((A, 'inconsistent')); continue
            sol = list(sol)[0]
            xs = dict(zip(X, sol[:5]))
            free = set().union(*[sp.sympify(e).free_symbols for e in xs.values()]) - {f, T}
            if free:
                skipped.append((A, 'x not unique')); continue
            xs = {k: sp.factor(sp.together(v)) for k, v in xs.items()}
            # independent check of stationarity + constraints
            lam = sol[5:]
            chk = [sp.simplify(e.subs(dict(zip(unk, sol)))) for e in eqs]
            assert all(cc == 0 for cc in chk), (A, chk)
            out.append((A, xs))
    return out, skipped, G, DD
