import sympy as sp, time
z,w=sp.symbols('z w')
N=(35*z**5 - 140*z**4*w - 392*z**4 + 210*z**3*w**2 + 840*z**3*w + 1824*z**3 - 140*z**2*w**3 - 504*z**2*w**2 + 3744*z**2*w - 4608*z**2 + 35*z*w**4 + 56*z*w**3 + 4960*z*w**2 - 11904*z*w + 4864*z + 224*w**3 - 1664*w**2 + 2560*w + 2048)
E=(w-z)**2-8*(w+z)+16
G=4*N/(105*z*E**2)
A=sp.factor(sp.numer(sp.together(sp.diff(G,w))))
B=sp.factor(sp.numer(sp.together(sp.diff(G,z))))
print('A=',A); print('B=',B)
a=sp.Poly(sp.expand(A/32),w,z); b=sp.Poly(sp.expand(-B/32),w,z)
t0=time.time()
R=sp.resultant(a.as_expr(),b.as_expr(),w)
R=sp.Poly(R,z)
print('res deg',R.degree(),time.time()-t0)
fl=sp.factor_list(R.as_expr())
for f,m in fl[1]:
    fp=sp.Poly(f,z); print('factor deg',fp.degree(),'mult',m)
    for r in sp.Poly(f,z).nroots(n=30):
        if abs(sp.im(r))<1e-20 and 0<sp.re(r)<4:
            zr=sp.re(r)
            # common w roots
            wa=sp.Poly(a.as_expr().subs(z,zr),w).nroots(n=30)
            wb=sp.Poly(b.as_expr().subs(z,zr),w).nroots(n=30)
            print('  z=',zr, 'wmax',(2-sp.sqrt(zr))**2)
            for x1 in wa:
                for x2 in wb:
                    if abs(x1-x2)<1e-10: print('     common w',x1)
