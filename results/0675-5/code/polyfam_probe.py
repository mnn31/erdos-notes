# Probe: for P(v) = A v^2 + B v + C (small integers), which m in 0..40 make P^2 + m a norm from Z[i][v]
# (i.e. a sum of two squares of polynomials over Q, equivalently every Q(i)-irreducible factor of odd
# multiplicity ... we test: factor over Q(i) and check that P^2+m = c * g * conj(g)).
import sympy as sp, itertools, sys
v=sp.symbols('v'); I=sp.I
def is_norm(f):
    f=sp.Poly(sp.expand(f),v)
    lc, facs = sp.factor_list(f.as_expr(), v, extension=I)
    # f is a norm iff the multiset of irreducible factors is closed under conjugation (pairing g with conj(g)),
    # with g != conj(g) up to units, or even multiplicity for self-conjugate ones.
    rem=[]
    for g,e in facs:
        g=sp.Poly(g,v); rem.append([g,e])
    def monic(g): return sp.Poly(g.as_expr()/g.LC(),v)
    used=[False]*len(rem)
    for i,(g,e) in enumerate(rem):
        gm=monic(g); gc=monic(sp.Poly(sp.conjugate(g.as_expr()).subs(sp.conjugate(v),v),v))
        if gm==gc:
            if e%2: return False
        else:
            # need conj partner with same multiplicity
            ok=False
            for j,(h,e2) in enumerate(rem):
                if monic(h)==gc and e2==e: ok=True
            if not ok: return False
    return True
best=[]
for A in (1,2):
  for B in range(0,5):
    for C in range(-12,13):
      P=A*v**2+B*v+C
      good=[m for m in range(0,41) if is_norm(P**2+m)]
      best.append((len(good),A,B,C,good))
best.sort(reverse=True)
for b in best[:15]: print(b)
