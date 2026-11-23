# Exact elimination for graph B (see WRITEUP).
# p1=0, p2=1, p6=w (WLOG by rotation/reflection), p3=y, p5=s2*y, p4=1+z, p0=1+z+t ; |y|=|z|=|t|=1
import sympy as sp, itertools
y,z,t=sp.symbols('y z t')
s3=sp.sqrt(3); EXT=sp.I*s3
w=sp.Rational(1,2)+sp.I*s3/2; wb=sp.Rational(1,2)-sp.I*s3/2
cj={y:1/y,z:1/z,t:1/t}
def conjexpr(e):
    return sp.conjugate(e).subs({sp.conjugate(y):1/y,sp.conjugate(z):1/z,sp.conjugate(t):1/t})
def eq(a,b,gens):
    d=a-b
    e=sp.expand(d*conjexpr(d)-1)
    return sp.Poly(sp.expand(sp.numer(sp.together(e))),*gens,extension=EXT)
for s2name,s2 in (("omega",w),("conj(omega)",wb)):
    p1=sp.Integer(0); p2=sp.Integer(1); p6=w; p3=y; p5=s2*y; p4=1+z; p0=1+z+t
    E1=eq(p4,p3,(y,z,t)); E2=eq(p0,p5,(y,z,t)); E3=eq(p0,p6,(y,z,t))
    R1=sp.Poly(E2.as_expr(),t,y,z,extension=EXT).resultant(sp.Poly(E3.as_expr(),t,y,z,extension=EXT))
    R1=sp.Poly(R1.as_expr(),z,y,extension=EXT)
    R2=R1.resultant(sp.Poly(E1.as_expr(),z,y,extension=EXT))
    R2=sp.Poly(R2.as_expr(),y,extension=EXT)
    print("s2=",s2name,"deg R1",R1.total_degree(),"R2 zero?",R2.is_zero,"deg R2",R2.degree())
    fac=sp.factor_list(R2.as_expr(),y,extension=EXT)
    print("  factors of R2(y):",[(f,m) for f,m in fac[1]])
    # candidate y: roots of factors; keep |y|=1 (checked exactly), then back-substitute
    for f,m in fac[1]:
        fr=sp.roots(sp.Poly(f,y,extension=EXT)); assert sum(fr.values())==sp.Poly(f,y,extension=EXT).degree()
        for y0 in fr:
            if sp.simplify(y0*sp.conjugate(y0)-1)!=0: 
                print("   root",y0,"not on unit circle"); continue
            e1=sp.Poly(sp.expand(sp.numer(sp.together(E1.as_expr().subs(y,y0)))),z,extension=EXT)
            zr=sp.roots(e1) if e1.degree()>0 else {}
            assert e1.degree()<=0 or sum(zr.values())==e1.degree()
            for z0 in zr:
                if sp.simplify(z0*sp.conjugate(z0)-1)!=0: continue
                e2=sp.Poly(sp.expand(E2.as_expr().subs({y:y0,z:z0})),t,extension=EXT)
                e3=sp.Poly(sp.expand(E3.as_expr().subs({y:y0,z:z0})),t,extension=EXT)
                g=sp.gcd(e2,e3)
                tr=sp.roots(g) if g.degree()>0 else {}
                assert g.degree()<=0 or sum(tr.values())==g.degree()
                if e2.is_zero and e3.is_zero:
                    # t is unconstrained; then |p4+t-p5|=1 for all unit t forces p4=p5 -- check collision directly
                    q4=sp.expand(p4.subs({y:y0,z:z0})); q5=sp.expand(p5.subs({y:y0,z:z0})); q6=sp.expand(p6)
                    print("   E2,E3 vanish identically in t at y=",y0,"z=",z0,"; p4==p5:",sp.simplify(q4-q5)==0,"p4==p6:",sp.simplify(q4-q6)==0)
                    assert sp.simplify(q4-q5)==0 or sp.simplify(q4-q6)==0
                    continue
                for t0 in tr:
                    P=[sp.expand(p.subs({y:y0,z:z0,t:t0})) for p in (p0,p1,p2,p3,p4,p5,p6)]
                    coll=any(sp.simplify(P[i]-P[j])==0 for i,j in itertools.combinations(range(7),2))
                    nu=sum(1 for i,j in itertools.combinations(range(7),2) if sp.simplify(sp.expand((P[i]-P[j])*sp.conjugate(P[i]-P[j]))-1)==0)
                    print("   solution y=",y0,"z=",z0,"t=",t0,"|t|^2=",sp.simplify(t0*sp.conjugate(t0)),"collision:",coll,"#unit:",nu)
            if e1.degree()<=0: print("   E1 vanishes identically in z at y0=",y0,"; but then p3=y0=1=p2 (collision) iff y0==1:",sp.simplify(y0-1)==0)
