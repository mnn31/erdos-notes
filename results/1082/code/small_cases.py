# Rigorous small-case check (n = 6 and n = 8) for Erdos #1082 target.
# For each convex Q in Fishburn's lists (4 quadrilaterals with 2 distances, 3 hexagons with 3 distances):
#   (1) verify EXACTLY (sympy minimal polynomials) that Q has exactly |D| distances and is strictly convex;
#   (2) enumerate ALL points p not in Q with |p-v| in D(Q) for every vertex v of Q
#       (p lies on a circle about v0 and a circle about v1 with radii in D(Q)); rejections are certified
#       with mpmath interval arithmetic (mpmath.iv), acceptances are verified exactly with sympy;
#   (3) for every pair {p,q} of such points decide whether |p-q| in D(Q) and Q+{p,q} has no 3 collinear.
import sympy as sp, mpmath, itertools, sys
from mpmath import iv
iv.dps = 60
mpmath.mp.dps = 90
X = sp.Symbol('X')
def is_zero(e):
    v = sp.N(e, 80)
    if abs(v) > sp.Float(10)**-30: return False
    return sp.minimal_polynomial(sp.expand(e), X) == X
def to_iv(e):
    # rigorous enclosure: evaluate exact sympy expression to 80 digits, widen by 1e-60
    # sympy evalf to 80 significant digits; the decimal strings below are parsed by mpmath.iv with
    # outward rounding; widening by 1e-50 dominates the evalf error (|values| < 10 here).
    v = sp.N(e, 80); assert abs(sp.im(v)) < sp.Float(10)**-70
    w = sp.Float(10, 90)**-50
    return iv.mpf([str(sp.N(sp.re(v) - w, 85)), str(sp.N(sp.re(v) + w, 85))])
def d2(p, q): return sp.expand((p[0]-q[0])**2 + (p[1]-q[1])**2)
def cross(a, b, c): return sp.expand((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]))

def exact_distset(Q):
    D = []
    for i, j in itertools.combinations(range(len(Q)), 2):
        e = d2(Q[i], Q[j])
        if not any(is_zero(e - f) for f in D): D.append(e)
    return D
def strictly_convex_cyclic(Q):
    # Q given in cyclic order; all consecutive cross products same strict sign, and polygon simple
    # (for a closed polygon whose turns are all the same sign and total turning 2*pi, i.e. winding 1).
    h = len(Q); s = [sp.N(cross(Q[i], Q[(i+1) % h], Q[(i+2) % h]), 50) for i in range(h)]
    import math
    ang = 0.0
    for i in range(h):
        a = [float(sp.N(Q[(i+1) % h][k]-Q[i][k])) for k in (0, 1)]; b = [float(sp.N(Q[(i+2) % h][k]-Q[(i+1) % h][k])) for k in (0, 1)]
        ang += math.atan2(a[0]*b[1]-a[1]*b[0], a[0]*b[0]+a[1]*b[1])
    return (all(x > 1e-40 for x in s) or all(x < -1e-40 for x in s)) and abs(abs(ang) - 2*math.pi) < 1e-9

def analyse(name, Q):
    print("=" * 70); print(name, " |Q| =", len(Q))
    D = exact_distset(Q)
    print("  exact number of distances:", len(D), " values^2 ~", [sp.N(f, 12) for f in D])
    print("  strictly convex (cyclic order):", strictly_convex_cyclic(Q))
    Div = [to_iv(f) for f in D]
    Qiv = [(to_iv(a), to_iv(b)) for a, b in Q]
    v0, v1 = Q[0], Q[1]
    cand = []  # exact candidate points
    for f1, f2 in itertools.product(D, D):
        # circle |p-v0|^2=f1, |p-v1|^2=f2
        dd = d2(v0, v1); a = (f1 - f2 + dd) / (2 * dd)  # p = v0 + a*(v1-v0) + t*perp, |perp|^2 = dd
        t2 = sp.simplify((f1 - a**2 * dd) / dd)
        t2iv = to_iv(t2)
        if t2iv.b < 0: continue            # circles certified disjoint
        if t2iv.a <= 0 <= t2iv.b:
            if is_zero(t2): ts = [sp.Integer(0)]
            else: raise SystemExit("ambiguous tangency")
        else: ts = [sp.sqrt(t2), -sp.sqrt(t2)]
        for t in ts:
            p = (v0[0] + a*(v1[0]-v0[0]) - t*(v1[1]-v0[1]), v0[1] + a*(v1[1]-v0[1]) + t*(v1[0]-v0[0]))
            cand.append(p)
    print("  circle-intersection candidates:", len(cand))
    ext = []
    for p in cand:
        piv = (to_iv(p[0]), to_iv(p[1]))
        ok = True; isvertex = False
        for (vx, vy), v in zip(Qiv, Q):
            e = (piv[0]-vx)**2 + (piv[1]-vy)**2
            if e.a <= 0 <= e.b and is_zero(d2(p, v)): isvertex = True; break
            if not any(e.a <= f.b and f.a <= e.b for f in Div): ok = False; break   # certified miss
        if isvertex or not ok: continue
        # survivor: verify exactly that every distance lies in D
        for v in Q:
            assert any(is_zero(d2(p, v) - f) for f in D), "interval survivor not exact"
        if not any(is_zero(p[0]-q[0]) and is_zero(p[1]-q[1]) for q in ext): ext.append(p)
    print("  EXACT one-point extensions (p not in Q, all |p-v| in D(Q)):", len(ext))
    for p in ext:
        col = [(i, j) for i, j in itertools.combinations(range(len(Q)), 2) if is_zero(cross(Q[i], Q[j], p))]
        print("    p ~ (%s, %s)  collinear with vertex pairs: %s" % (sp.N(p[0], 10), sp.N(p[1], 10), col))
    good = [p for p in ext if not any(is_zero(cross(Q[i], Q[j], p)) for i, j in itertools.combinations(range(len(Q)), 2))]
    print("  extensions with no collinear triple in Q+{p}:", len(good))
    pairs_ok = 0
    for p, q in itertools.combinations(good, 2):
        e = d2(p, q)
        if not any(is_zero(e - f) for f in D): continue
        if any(is_zero(cross(Q[i], p, q)) for i in range(len(Q))): continue
        pairs_ok += 1; print("    VALID PAIR:", p, q)
    print("  valid pairs {p,q} (|p-q| in D, no 3 collinear in Q+{p,q}):", pairs_ok)
    return pairs_ok

s3 = sp.sqrt(3); s2 = sp.sqrt(2)
def reg(N, drop=None):
    return [(sp.cos(2*sp.pi*j/N), sp.sin(2*sp.pi*j/N)) for j in range(N) if j != drop]
def turtle(sides, ext_deg):
    P = [(sp.Integer(0), sp.Integer(0))]; ang = sp.Integer(0)
    for L, e in zip(sides, ext_deg):
        P.append((P[-1][0] + L*sp.cos(ang*sp.pi/180), P[-1][1] + L*sp.sin(ang*sp.pi/180))); ang += e
    assert is_zero(P[-1][0]) and is_zero(P[-1][1]); return [(sp.simplify(x), sp.simplify(y)) for x, y in P[:-1]]
quads = {
  "square (regular 4-gon)": reg(4),
  "regular pentagon minus a vertex": reg(5, drop=0),
  "rhombus with 60-degree angle": [(0, 0), (1, 0), (sp.Rational(3, 2), s3/2), (sp.Rational(1, 2), s3/2)],
  # kite: equilateral triangle A,B,C (side 1) plus D on the axis through A beyond BC with |AD| = 1
  "kite (equilateral triangle + point at distance 1 on axis)": [(0, 0), (s3/2, -sp.Rational(1, 2)), (1, 0), (s3/2, sp.Rational(1, 2))],
}
hexes = {
  "regular hexagon": reg(6),
  "regular heptagon minus a vertex": reg(7, drop=0),
  "equilateral hexagon, angles 90,150,90,150,90,150": turtle([1]*6, [90, 30]*3),
}
total = 0
which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all", "quads"):
    for k, Q in quads.items(): total += analyse(k, [(sp.sympify(a), sp.sympify(b)) for a, b in Q])
if which in ("all", "hexes", "h3"):
    for k, Q in hexes.items():
        if which == "h3" and not k.startswith("equilateral"): continue
        total += analyse(k, [(sp.sympify(a), sp.sympify(b)) for a, b in Q])
print("TOTAL valid pairs over all cases:", total)
