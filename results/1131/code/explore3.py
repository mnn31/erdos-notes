import sympy as sp
z,w=sp.symbols('z w')
a=(-77*w**4*z - 28*w**4 + 112*w**3*z**2 - 1072*w**3*z + 192*w**3 + 126*w**2*z**3 - 2328*w**2*z**2 + 4128*w**2*z + 384*w**2 - 280*w*z**4 + 3952*w*z**3 - 9280*w*z**2 + 9472*w*z - 5120*w + 119*z**5 - 524*z**4 - 2208*z**3 + 12928*z**2 - 15616*z + 9216)
b=(28*w**5 - 175*w**4*z**2 - 168*w**4*z - 432*w**4 + 504*w**3*z**3 - 3144*w**3*z**2 + 576*w**3*z + 2432*w**3 - 462*w**2*z**4 + 2432*w**2*z**3 + 320*w**2*z**2 + 3072*w**2*z - 5632*w**2 + 112*w*z**5 + 1068*w*z**4 - 8256*w*z**3 + 10880*w*z**2 - 9216*w*z + 3072*w + 21*z**6 - 216*z**5 + 624*z**4 - 256*z**3 + 768*z**2 - 6144*z + 4096)
for var,other in [(w,z),(z,w)]:
    R=sp.resultant(a,b,var)
    fl=sp.factor_list(R)
    print('eliminate',var,'content',fl[0])
    for f,m in fl[1]:
        P=sp.Poly(f,other)
        print('  deg',P.degree(),'mult',m, f if P.degree()<=2 else '')
        print('    real roots isolating:',[ (float(lo),float(hi)) for (lo,hi),k in P.intervals()])
