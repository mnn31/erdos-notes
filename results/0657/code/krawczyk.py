# Generic Krawczyk certification (mpmath interval arithmetic, outward rounding) + distance-class checks.
import sympy as sp, mpmath, itertools, numpy as np
from mpmath import iv, mp
iv.prec=200; mp.prec=200
def certify(zs, eqs, z0, pts, rad=1e-30, refine=60):
    """zs: sympy symbols; eqs: sympy polys (square system); z0 approx root; pts: list of (X,Y) sympy exprs in zs.
    Returns (ok, box, info)."""
    n=len(zs); J=sp.Matrix(eqs).jacobian(zs)
    # rigor guard: lambdify would turn non-integer rationals into inexact floats; insist on integer coefficients
    for e in eqs: assert all(c.is_Integer for c in sp.Poly(e,*zs).coeffs()), 'non-integer coefficient'
    for p in pts:
        for t in p: assert all(c.is_Integer for c in sp.Poly(sp.sympify(t),*zs).coeffs()), 'non-integer coordinate coeff' 
    Ff=sp.lambdify(zs,eqs,'mpmath'); Jf=sp.lambdify(zs,J.tolist(),'mpmath')
    z=mpmath.matrix([mpmath.mpf(x) for x in z0])
    for _ in range(refine):  # Newton in high precision
        Fz=mpmath.matrix(Ff(*z)); Jz=mpmath.matrix(Jf(*z))
        z=z-mpmath.lu_solve(Jz,Fz)
    Jm=mpmath.matrix(Jf(*z)); Y=mpmath.inverse(Jm)
    X=[iv.mpf([z[i]-rad,z[i]+rad]) for i in range(n)]
    m=[iv.mpf(z[i]) for i in range(n)]
    Fm=Ff(*m); JX=Jf(*X)
    Yi=[[iv.mpf(Y[i,j]) for j in range(n)] for i in range(n)]
    ok=True; K=[]
    for i in range(n):
        s=m[i]-sum(Yi[i][j]*Fm[j] for j in range(n))
        for k in range(n):
            c=(1 if i==k else 0)-sum(Yi[i][j]*JX[j][k] for j in range(n))
            s+=c*(X[k]-m[k])
        K.append(s)
        if not (s.a>X[i].a and s.b<X[i].b): ok=False
    return ok, X, z
def dist_check(pts, zs, X):
    f=sp.lambdify(zs,[sp.expand((p[0]-q[0])**2+(p[1]-q[1])**2) for p,q in itertools.combinations(pts,2)],'mpmath')
    D=[x if isinstance(x,type(iv.mpf(1))) else iv.mpf(x) for x in f(*X)]; E=list(itertools.combinations(range(len(pts)),2)); Dd=dict(zip(E,D))
    return Dd
def overlap(a,b): return not (a.b<b.a or b.b<a.a)
