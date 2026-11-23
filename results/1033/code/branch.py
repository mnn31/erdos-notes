"""Wouter branch (active set {C1,C2}): exact crossing with Fan, alpha_b, and the
existence certificate for T in [T1, T_b).  All sign claims use exact rational interval
arithmetic on rational enclosures of the algebraic numbers."""
import sys
sys.path.insert(0, '.')
import sympy as sp
from fractions import Fraction as Fr
from qpfaces import enumerate_faces, f, T, MF, X
A_ = sp.symbols('A')
faces, _, G, DD = enumerate_faces(['a','b','c','us','u','C1','C2'], (), maxsize=2)
xs = dict(faces)[('C1', 'C2')]
VW = sp.factor(sp.together(DD.subs(xs)))
Delta = sp.factor(sp.together(MF - VW))
print('x_W(f,T) =', xs)
print('V_W(f,T) =', VW)
print('M_F - V_W =', Delta)
num, den = sp.fraction(Delta)
# Delta = (f-1)*N/(48*den4)
N = sp.expand(sp.cancel(num/(f - 1)))
den4 = f**4 - 6*f**3 - 11*f**2 - 36*f + 4
assert sp.simplify(Delta - (f - 1)*N/(48*den4)) == 0
print('N(f,T) =', sp.collect(N, T))
Nf = sp.diff(N, f)
R = sp.factor(sp.resultant(N, Nf, f))
print('Res_f(N, dN/df) =', R)
P8 = sp.Poly(1761*T**8 + 15288*T**7 + 40795*T**6 + 11790*T**5 - 59967*T**4 + 75924*T**3
             - 72279*T**2 + 32886*T - 5238, T)
assert sp.rem(sp.Poly(R, T), P8).is_zero
# subresultant of degree 1 in f: gives f_b = -S0(T_b)/S1(T_b)
subs_ = sp.subresultants(sp.Poly(N, f), sp.Poly(Nf, f))
S1p = [q for q in subs_ if q.degree() == 1][0]
S1c, S0c = [sp.expand(cf) for cf in S1p.all_coeffs()]
fb_expr = -S0c/S1c
# exact verification that N(f_b,T_b)=0 and dN/df(f_b,T_b)=0 in Q[T]/(P8)
for name, poly in (('N', N), ('dN/df', Nf)):
    e = sp.together(poly.subs(f, fb_expr))
    nn, dd = sp.fraction(e)
    assert sp.rem(sp.Poly(nn, T), P8).is_zero, name
    print(f'{name}(f_b(T), T) vanishes modulo P8: True')
# rational enclosure of T_b
iv = [iv for iv, m in P8.intervals() if iv[0] > sp.Rational(46, 100)][0]
lo, hi = P8.refine_root(iv[0], iv[1], eps=sp.Rational(1, 10**60))
lo, hi = Fr(int(sp.Rational(lo).p), int(sp.Rational(lo).q)), Fr(int(sp.Rational(hi).p), int(sp.Rational(hi).q))
print('T_b in [%s, %s]' % (sp.N(sp.Rational(lo.numerator, lo.denominator), 40), sp.N(sp.Rational(hi.numerator, hi.denominator), 40)))
# --- tiny exact interval arithmetic over Fractions ---
class I:
    def __init__(s, l, h=None): s.l = Fr(l); s.h = Fr(l if h is None else h); assert s.l <= s.h
    def __add__(s, o): o = o if isinstance(o, I) else I(o); return I(s.l + o.l, s.h + o.h)
    __radd__ = __add__
    def __neg__(s): return I(-s.h, -s.l)
    def __sub__(s, o): return s + (-(o if isinstance(o, I) else I(o)))
    def __rsub__(s, o): return I(o) - s
    def __mul__(s, o):
        o = o if isinstance(o, I) else I(o); p = [s.l*o.l, s.l*o.h, s.h*o.l, s.h*o.h]; return I(min(p), max(p))
    __rmul__ = __mul__
    def inv(s): assert s.l > 0 or s.h < 0, 'division by interval containing 0'; return I(1/s.h, 1/s.l)
    def __truediv__(s, o): o = o if isinstance(o, I) else I(o); return s*o.inv()
    def __pow__(s, n):
        r = I(1)
        for _ in range(n): r = r*s
        return r
    def __repr__(s): return '[%.25f, %.25f]' % (float(s.l), float(s.h))
def ev(expr, env):
    """evaluate a sympy rational expression with interval arithmetic"""
    expr = sp.sympify(expr)
    if expr.is_Number: return I(Fr(int(sp.Rational(expr).p), int(sp.Rational(expr).q)))
    if expr.is_Symbol: return env[expr]
    if expr.is_Add:
        r = I(0)
        for t in expr.args: r = r + ev(t, env)
        return r
    if expr.is_Mul:
        r = I(1)
        for t in expr.args: r = r*ev(t, env)
        return r
    if expr.is_Pow:
        bse, e = expr.args
        if e.is_Integer and e > 0: return ev(bse, env)**int(e)
        if e.is_Integer and e < 0: return (ev(bse, env)**int(-e)).inv()
    raise ValueError(expr)
Tb = I(lo, hi)
fb = ev(sp.together(fb_expr), {T: Tb})
print('f_b  in', fb)
assert fb.l > 0 and fb.h < 1
alpha_b = ev(MF, {T: Tb}); print('alpha_b in', alpha_b)
# minimal polynomial of alpha_b
mp = sp.factor(sp.resultant(P8.as_expr(), 48*A_ - (T + 3)**2, T))
octic = [q for q, m in sp.factor_list(mp)[1] if sp.Poly(q, A_).degree() == 8][0]
print('alpha_b is a root of', sp.Poly(octic, A_).as_expr(), ' irreducible:', sp.Poly(octic, A_).is_irreducible)
oc = sp.Poly(octic, A_)
assert oc.eval(sp.Rational(alpha_b.l.numerator, alpha_b.l.denominator))*oc.eval(sp.Rational(alpha_b.h.numerator, alpha_b.h.denominator)) < 0
# --- existence certificate on [T1, T_b) with f = f_b fixed ---
T1 = Fr(4635, 10000)
NfbT = sp.Poly(N, T)   # coefficients in f
A2, A1, A0 = [ev(cf, {f: fb}) for cf in NfbT.all_coeffs()]
print('N(f_b,T) = A2 T^2 + A1 T + A0 with A2 in', A2, 'A1 in', A1, 'A0 in', A0)
other_root = A0/(A2*Tb)   # product of roots = A0/A2
print('second root of N(f_b,.) in', other_root)
assert other_root.h < T1 or other_root.l > hi
# sign of Delta_W(f_b, T) at T1  (Delta = (f-1)N/(48 den4))
d_T1 = ev(Delta, {f: fb, T: I(T1)})
print('Delta_W(f_b, T1) in', d_T1, '(must be < 0)')
assert d_T1.h < 0
# feasibility of x_W(f_b,T): coordinates affine in T; check strict positivity at both ends
for Tend in (I(T1), Tb):
    vals = {k: ev(v, {f: fb, T: Tend}) for k, v in xs.items()}
    print('  T =', Tend, {str(k): v for k, v in vals.items()})
    for k in X: assert vals[k].l > 0, k
    assert (vals[X[3]] - vals[X[4]]).l > 0   # u < s  (g < 1)
    for gname in ('C1', 'C2'):   # active on this face: identically zero
        assert sp.simplify(G[gname].subs(xs)) == 0, gname
VT1 = ev(VW, {f: fb, T: I(T1)})
print('V_W(f_b, T1) in', VT1, '(must be <= 1/4)')
assert VT1.h <= Fr(1, 4)
print('EXISTENCE CERTIFICATE OK')
# cross-check against Wouter's degree-7 polynomial at alpha = 1/4: crossing of the branch with density 1/4
Gq = sp.numer(sp.together(VW - sp.Rational(1, 4)))
Pst = sp.numer(sp.together(sp.diff(VW, f)))
R4 = sp.factor(sp.resultant(sp.expand(Gq), sp.expand(Pst), f))
y = sp.symbols('y')
W7 = 384*y**7 + 1744*y**6 - 832*y**5 - 86712*y**4 + 379016*y**3 - 697963*y**2 + 617212*y - 215708
print('Wouter P(y) divides Res at T=y-1:', sp.rem(sp.Poly(sp.expand(R4.subs(T, y - 1)), y), sp.Poly(W7, y)).is_zero)
