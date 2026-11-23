# Exact elimination for graph A (see WRITEUP Lemma on graph A).
import sympy as sp
x,y=sp.symbols('x y')
s3=sp.sqrt(3)
w=sp.Rational(1,2)+sp.I*s3/2      # omega = exp(i pi/3)
wb=sp.Rational(1,2)-sp.I*s3/2     # conj(omega)
def cl(e):
    return sp.Poly(sp.expand(sp.numer(sp.together(sp.expand(e)))),x,y,extension=sp.I*s3)
for name,sig,sigb in (("sigma=omega",w,wb),("sigma=conj(omega)",wb,w)):
    # p0=0,p3=1,p4=w,p5=wb,p6=x,p1=x+y,p2=x+sig*y ; conj(x)=1/x, conj(y)=1/y
    E1=(x+y-wb)*(1/x+1/y-w)-1          # |p1-p5|^2=1
    E2=(x+sig*y-w)*(1/x+sigb/y-wb)-1     # |p2-p4|^2=1
    P1=cl(E1); P2=cl(E2)
    R=sp.resultant(P1.as_expr(),P2.as_expr(),y)
    R=sp.Poly(sp.expand(R),x,extension=sp.I*s3)
    print(name,"resultant degree",R.degree(), "zero?",R.is_zero)
    fac=sp.factor_list(R.as_expr(),x,extension=sp.I*s3)
    print("  factors:",[(sp.simplify(f),m) for f,m in fac[1]])

print("--- back-substitution: for each root x0 with |x0|=1, all y with E1=E2=0")
import itertools
for name,sig,sigb in (("sigma=omega",w,wb),("sigma=conj(omega)",wb,w)):
    for x0 in (w,wb,sp.Integer(-1)):
        E1=(x0+y-wb)*(1/x0+1/y-w)-1
        E2=(x0+sig*y-w)*(1/x0+sigb/y-wb)-1
        n1=sp.Poly(sp.expand(sp.numer(sp.together(sp.expand(E1)))),y,extension=sp.I*s3)
        n2=sp.Poly(sp.expand(sp.numer(sp.together(sp.expand(E2)))),y,extension=sp.I*s3)
        g=sp.gcd(n1,n2)
        roots=sp.roots(g) if g.degree()>0 else {}
        assert g.degree()<=0 or sum(roots.values())==g.degree(), 'incomplete root list'
        assert not (n1.is_zero and n2.is_zero)
        for y0 in roots:
            y0=sp.nsimplify(sp.simplify(y0))
            P=[0,x0+y0,x0+sig*y0,1,w,wb,x0]
            P=[sp.nsimplify(sp.expand(p)) for p in P]
            d2={}
            coll=False
            for i,j in itertools.combinations(range(7),2):
                v=sp.nsimplify(sp.simplify(sp.expand((P[i]-P[j])*sp.conjugate(P[i]-P[j]))))
                if v==0: coll=True
                d2[(i,j)]=v
            units=[k for k,v in d2.items() if v==1]
            print(name,"x0=",x0,"y0=",y0,"|y0|^2=",sp.simplify(y0*sp.conjugate(y0)),"collision:",coll,"#unit:",len(units))
