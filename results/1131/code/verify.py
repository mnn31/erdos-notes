"""Exact verification for Erdos 1131, n = 4.  Run:  python3 -I code/verify.py
All load-bearing steps use exact rational / polynomial arithmetic (sympy).
Floating point appears only in the clearly-labelled SANITY section."""
import sympy as sp, random
from fractions import Fraction as Fr
x,u,v,s,d,z,w,t=sp.symbols('x u v s d z w t')
ok=lambda c,msg: print(('PASS ' if c else 'FAIL ')+msg) or (c or exit(1))

# ---- Step 1: I(-1,u,v,1) as an exact rational function -----------------
nodes=[-1,u,v,1]; I=0
for k,xk in enumerate(nodes):
    num=sp.Integer(1); den=sp.Integer(1)
    for j,xj in enumerate(nodes):
        if j!=k: num*=(x-xj); den*=(xk-xj)
    I+=sp.integrate(sp.expand(num**2),(x,-1,1))/den**2
I=sp.cancel(sp.together(I))
P,Q=sp.fraction(sp.factor(I))
print('I(-1,u,v,1) =',P,'/',Q)

# independent check with pure-Python Fractions at random rational points
def I_frac(nd):
    tot=Fr(0)
    for k,xk in enumerate(nd):
        c=[Fr(1)]; den=Fr(1)
        for j,xj in enumerate(nd):
            if j==k: continue
            c=[Fr(0)]+c; c=[c[i]-xj*(c[i+1] if i+1<len(c) else 0) for i in range(len(c))]  # multiply by (x-xj)
            den*=xk-xj
        sq=[Fr(0)]*(2*len(c)-1)
        for i,a in enumerate(c):
            for j2,b in enumerate(c): sq[i+j2]+=a*b
        tot+=sum(a*(Fr(1)-Fr((-1)**(i+1)))/(i+1) for i,a in enumerate(sq))/den**2
    return tot
random.seed(1)
for _ in range(20):
    a1,a2=sorted(Fr(random.randint(-999,999),1000) for _ in range(2))
    if a1==a2: continue
    ok(I_frac([Fr(-1),a1,a2,Fr(1)])==sp.Rational(I.subs({u:sp.Rational(a1.numerator,a1.denominator),v:sp.Rational(a2.numerator,a2.denominator)})), f'rational function matches direct Fraction integral at ({a1},{a2})')

# ---- Step 2: symmetric family and target value --------------------------
It=sp.cancel(I.subs({u:-sp.sqrt(t),v:sp.sqrt(t)}))
target=(140*t**2-112*t+92+8/t)/(105*(1-t)**2)
ok(sp.simplify(It-target)==0,'I(-1,-sqrt t,sqrt t,1) == (140t^2-112t+92+8/t)/(105(1-t)^2)')
dnum=sp.factor(sp.numer(sp.together(sp.diff(target,t)))); dden=sp.factor(sp.denom(sp.together(sp.diff(target,t))))
print('dI/dt =',dnum,'/',dden)
cub=21*t**3+9*t**2+3*t-1
ok(sp.simplify(sp.diff(target,t)-sp.Rational(8,105)*cub/(t**2*(1-t)**3))==0,'dI/dt == 8(21t^3+9t^2+3t-1)/(105 t^2 (1-t)^3)')
ok(sp.discriminant(sp.diff(cub,t),t)<0 and sp.Poly(sp.diff(cub,t),t).LC()>0,"cubic' >0 everywhere => cubic has exactly one real root")
ok(cub.subs(t,0)<0 and cub.subs(t,1)>0,'that root lies in (0,1)')
ok(sp.Poly(cub,t).count_roots(0,1)==1,'Sturm: exactly one root of cubic in [0,1]')
ok(target.subs(t,sp.Rational(3,16))==sp.Rational(91076,53235) and sp.Rational(91076,53235)<2,'I(t=3/16)=91076/53235<2')

# ---- Step 3: invariant coordinates z=(v-u)^2, w=(u+v)^2 ------------------
Psd=sp.Poly(sp.expand(P.subs({u:(s-d)/2,v:(s+d)/2})),s,d)
ok(all(i%2==0 and j%2==0 for (i,j) in Psd.monoms()),'numerator is even in s and in d separately')
Nzw=sp.expand(sum(c*w**(i//2)*z**(j//2) for (i,j),c in Psd.terms()))
E=(w-z)**2-8*(w+z)+16
zw={z:(v-u)**2,w:(u+v)**2}
ok(sp.expand(E.subs(zw)-16*(1-u**2)*(1-v**2))==0,'E(z,w) = 16(1-u^2)(1-v^2)')
G=Nzw/(z*E**2)
c0=sp.cancel(I/G.subs(zw)); print('I / G =',c0)
ok(c0.is_number,'I(u,v) = const * N(z,w)/(z E(z,w)^2) identically')
print('N(z,w) =',Nzw)
# gradient numerators
Gw_num=sp.expand(sp.diff(Nzw,w)*E-2*Nzw*sp.diff(E,w))          # G_w = Gw_num/(z E^3)
Gz_num=sp.expand(z*E*sp.diff(Nzw,z)-Nzw*E-2*z*Nzw*sp.diff(E,z)) # G_z = Gz_num/(z^2 E^3)
ok(sp.simplify(sp.diff(G,w)-Gw_num/(z*E**3))==0,'G_w = Gw_num/(z E^3)')
ok(sp.simplify(sp.diff(G,z)-Gz_num/(z**2*E**3))==0,'G_z = Gz_num/(z^2 E^3)')
A=sp.Poly(Gw_num,z,w); B=sp.Poly(Gz_num,z,w)
cA,pA=A.primitive(); cB,pB=B.primitive()
print('content Gw_num',cA,' content Gz_num',cB)
print('a(z,w) =',pA.as_expr()); print('b(z,w) =',pB.as_expr())
bz=sp.Poly(pB.as_expr(),z); az=sp.Poly(pA.as_expr(),z)
print('deg_z a =',az.degree(),' LC_z a =',az.LC(),'; deg_z b =',bz.degree(),' LC_z b =',bz.LC())
ok(bz.LC().is_number and bz.LC()!=0,'LC_z(b) is a nonzero constant, so Res_z(a,b)(w0)=0 iff a(.,w0),b(.,w0) share a complex root')
Rw=sp.Poly(sp.resultant(pA.as_expr(),pB.as_expr(),z),w)
print('Res_z(a,b) has degree',Rw.degree())
fl=sp.factor_list(Rw.as_expr())
ok(sp.expand(fl[0]*sp.Mul(*[f**m for f,m in fl[1]])-Rw.as_expr())==0,'factorization of Res_z re-multiplies correctly')
for f,m in fl[1]:
    fp=sp.Poly(f,w); print('  factor deg',fp.degree(),'mult',m,':',f if fp.degree()<=2 else '(deg 10, see out/)')
n04=Rw.count_roots(0,4)   # closed interval, exact Sturm
ok(Rw.eval(0)==0 and Rw.eval(4)==0,'w=0 and w=4 are roots')
sq=sp.Poly(sp.quo(Rw.as_expr(),(w**3*(w-4)**6)),w)
ok(sp.rem(Rw.as_expr(),w**3*(w-4)**6,w)==0 and sq.eval(0)!=0 and sq.eval(4)!=0,'Res_z = w^3 (w-4)^6 * R1 with R1(0),R1(4) != 0')
ok(sq.count_roots(0,4)==0,'Sturm: R1 has no real root in [0,4]  ==> Res_z(a,b) has no root in (0,4)')
ok(all(hi<0 for (lo,hi),k in sq.intervals()),'all real roots of R1 are negative (independent root isolation)')
# cross-check resultant via the other elimination order (not load-bearing)
Rz=sp.Poly(sp.resultant(pA.as_expr(),pB.as_expr(),w),z)
print('[cross-check] Res_w(a,b) real roots isolated:',[(lo,hi) for (lo,hi),k in Rz.intervals()])

# ---- Step 4: coercivity constant ----------------------------------------
vv=sp.symbols('vv')
ok(sp.expand(sp.integrate(((x**2-1)*(x-vv))**2,(x,-1,1))-(sp.Rational(16,105)+sp.Rational(16,15)*vv**2))==0,'int (x^2-1)^2 (x-v)^2 = 16/105 + 16/15 v^2')

# ---- SANITY (floating point, not load-bearing) -------------------------
import mpmath as mp
mp.mp.dps=40
ts=mp.findroot(lambda q:21*q**3+9*q**2+3*q-1,0.18)
Is=(140*ts**2-112*ts+92+8/ts)/(105*(1-ts)**2)
print('[sanity] t* =',ts,' sqrt t* =',mp.sqrt(ts),' I* =',Is)
If=sp.lambdify((u,v),I,'math')
best=(9,None)
for i in range(1,400):
    for j in range(i+1,400):
        uu=-1+2*i/400; vv2=-1+2*j/400; val=If(uu,vv2)
        if val<best[0]: best=(val,(uu,vv2))
print('[sanity] grid min over endpoint-fixed configs (step 0.005):',best)
open('out/resultant_factors.txt','w').write('Res_z(a,b) = '+str(fl[0])+' * '+' * '.join('('+str(f)+')^'+str(m) for f,m in fl[1])+'\n')
print('wrote out/resultant_factors.txt')
