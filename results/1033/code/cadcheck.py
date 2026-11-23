"""Exact sign-invariant cell check (2D CAD-lite in (f,T), or 1D in T when f is fixed).

For every face A with candidate x_A(f,T): we verify on every open 2D cell (sector) of a
cylindrical decomposition adapted to all relevant polynomials that
   [x_A defined and feasible]  ==>  M_F(T) - D(x_A) >= 0,
by exact rational evaluation at one sample point of each cell.
"""
import sympy as sp
from fractions import Fraction as Fr
from qpfaces import f, T, X, MF
P8 = sp.Poly(1761*T**8 + 15288*T**7 + 40795*T**6 + 11790*T**5 - 59967*T**4 + 75924*T**3
             - 72279*T**2 + 32886*T - 5238, T)

def above_Tb(t):
    """exact test t > T_b, where T_b is the unique root of P8 in (93/200, 1)."""
    t = sp.Rational(t)
    import os
    if os.environ.get('NEGCONTROL_CUT'):          # negative control only: plain cutoff
        return t > sp.Rational(os.environ['NEGCONTROL_CUT'])
    if t <= sp.Rational(93, 200): return False
    return P8.count_roots(sp.Rational(93, 200), t) == 1

def irr_factors(exprs, gens):
    fs = set()
    for e in exprs:
        e = sp.sympify(e)
        if e == 0: continue
        n, d = sp.fraction(sp.together(e))
        for part in (n, d):
            part = sp.expand(part)
            if part.is_number: continue
            _, fl = sp.factor_list(part, *gens)
            for q, m in fl:
                p = sp.Poly(q, *gens)
                if p.total_degree() == 0: continue
                p = p.monic() if p.LC() != 0 else p
                fs.add(p.as_expr())
    return sorted(fs, key=sp.default_sort_key)

def isolate_sorted(polys, lo, hi, var):
    """Real roots in the open interval (lo,hi) of univariate rational polys (distinct
    irreducibles), sorted, as pairwise disjoint closed rational intervals inside (lo,hi)."""
    items = []
    for q in polys:
        P = sp.Poly(q, var, domain='QQ')
        if P.degree() <= 0: continue
        for (l, r), m in P.intervals():
            l, r = sp.Rational(l), sp.Rational(r)
            if l == r:                       # exact rational root
                if lo < l < hi: items.append([l, r, P])
                continue
            # irrational root: it differs from the rationals lo, hi; refine until decided
            while (l <= lo <= r) or (l <= hi <= r):
                l, r = P.refine_root(l, r, eps=(r - l)/4)
                l, r = sp.Rational(l), sp.Rational(r)
            if lo < l and r < hi: items.append([l, r, P])
    changed = True
    while changed:
        changed = False
        items.sort(key=lambda z: z[0])
        for i in range(len(items) - 1):
            A, B = items[i], items[i+1]
            if A[1] >= B[0]:
                assert not (A[0] == A[1] and B[0] == B[1]), "equal rational roots of distinct irreducibles?"
                for Z in (A, B):
                    if Z[0] != Z[1]:
                        l, r = Z[2].refine_root(Z[0], Z[1], eps=(Z[1]-Z[0])/4)
                        Z[0], Z[1] = sp.Rational(l), sp.Rational(r)
                changed = True
                break
    items.sort(key=lambda z: z[0])
    return items

def samples_between(items, lo, hi):
    pts = []
    edges = [lo] + [x for it in items for x in (it[0], it[1])] + [hi]
    # gaps: (lo, l1), (r1, l2), ..., (rk, hi)
    for i in range(0, len(edges), 2):
        L, R = edges[i], edges[i+1]
        assert L < R, (L, R)
        pts.append((L + R)/2)
    return pts

def projection(polys):
    """Collins-type projection w.r.t. f: leading coeffs, discriminants, pairwise resultants,
    and pure-T polys; polys is a list of irreducible sympy exprs in (f,T); f and f-1 are added."""
    ps = irr_factors(list(polys) + [f, f - 1], [f, T])   # deduplicated irreducibles
    out = []
    P = [sp.Poly(p, f, T) for p in ps]
    withf = []
    for p in P:
        if p.degree(f) == 0:
            out.append(p.as_expr())
        else:
            pf = sp.Poly(p.as_expr(), f)
            withf.append(pf)
            out.append(pf.LC())
            if pf.degree() >= 2:
                out.append(sp.discriminant(pf.as_expr(), f))
    for i in range(len(withf)):
        for j in range(i + 1, len(withf)):
            rr = sp.resultant(withf[i].as_expr(), withf[j].as_expr(), f)
            assert sp.expand(rr) != 0, "zero resultant: factors not coprime"
            out.append(rr)
    for e in out:
        assert sp.expand(e) != 0, "zero projection polynomial"
    return irr_factors(out, [T])

def check_face_2d(A, xs, G, DD, Tlo_cut, Thi, extra_T_polys=()):
    """Return (n_cells_checked, failures)."""
    vals = list(xs.values())
    gi = {k: sp.together(g.subs(xs)) for k, g in G.items()}
    Delta = sp.together(MF - DD.subs(xs))
    polys = irr_factors(vals + list(gi.values()) + [Delta], [f, T])
    Tpolys = projection(polys) + [P8.as_expr()]
    Tpolys = irr_factors(Tpolys, [T])
    Titems = isolate_sorted(Tpolys, sp.Rational(0), Thi, T)
    # keep only cells above Tlo_cut (an isolating interval [l,r] of T_b given separately)
    Tsamp = [t for t in samples_between(Titems, sp.Rational(0), Thi) if above_Tb(t)]
    fails = []; ncell = 0
    num_den = [sp.fraction(v) for v in vals]
    gnd = {k: sp.fraction(v) for k, v in gi.items()}
    Dn, Dd = sp.fraction(Delta)
    for t in Tsamp:
        fpolys = []
        for p in polys:
            q = sp.expand(p.subs(T, t))
            if q.is_number: continue
            _, fl = sp.factor_list(q, f)
            fpolys += [qq for qq, m in fl if sp.Poly(qq, f).degree() > 0]
        fpolys = list(set(fpolys))
        fitems = isolate_sorted(fpolys, sp.Rational(0), sp.Rational(1), f)
        for fs_ in samples_between(fitems, sp.Rational(0), sp.Rational(1)):
            ncell += 1
            sub = {f: fs_, T: t}
            if any(d.subs(sub) == 0 for n, d in num_den): continue
            feas = True
            for k, (n, d) in gnd.items():
                nv, dv = n.subs(sub), d.subs(sub)
                if dv == 0: feas = None; break
                if nv*dv < 0: feas = False; break
            if not feas: continue
            dn, dd = Dn.subs(sub), Dd.subs(sub)
            if dd == 0 or dn*dd < 0:
                fails.append((A, fs_, t, sp.N(dn/dd if dd != 0 else sp.oo)))
    return ncell, fails, len(Tsamp)

def check_face_1d(A, xs, G, DD, Tlo_cut, Thi):
    vals = list(xs.values())
    gi = {k: sp.together(g.subs(xs)) for k, g in G.items()}
    Delta = sp.together(MF - DD.subs(xs))
    polys = irr_factors(vals + list(gi.values()) + [Delta], [T])
    Titems = isolate_sorted(polys + [P8.as_expr()], sp.Rational(0), Thi, T)
    Tsamp = [t for t in samples_between(Titems, sp.Rational(0), Thi) if above_Tb(t)]
    fails = []
    for t in Tsamp:
        sub = {T: t}
        if any(sp.fraction(v)[1].subs(sub) == 0 for v in vals): continue
        if any(sp.sympify(v).subs(sub) < 0 for v in gi.values()): continue
        dv = Delta.subs(sub)
        if dv < 0: fails.append((A, t, sp.N(dv)))
    return len(Tsamp), fails
