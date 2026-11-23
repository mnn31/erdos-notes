import sys; sys.path.insert(0,'.')
import sympy as sp, mpmath as mp
from qpfaces import enumerate_faces, f, T, MF
mp.mp.dps = 40
y, A = sp.symbols('y A')
p8 = 1761*T**8 + 15288*T**7 + 40795*T**6 + 11790*T**5 - 59967*T**4 + 75924*T**3 - 72279*T**2 + 32886*T - 5238
print('t_b = 1+T_b is a root of', sp.expand(p8.subs(T, y - 1)))
Tb = mp.findroot(lambda t: sp.lambdify(T, p8, 'mpmath')(t), mp.mpf('0.46502'))
print('T_b =', Tb, ' t_b =', 1 + Tb, ' alpha_b =', (Tb + 3)**2/48)
octic = 457278898176*A**8 - 466300901376*A**7 + 181754989888*A**6 - 30906363888*A**5 + 1134475329*A**4 + 285053348*A**3 - 22147578*A**2 - 988332*A + 37249
print('real roots of octic:', [sp.N(r, 25) for r in sp.real_roots(sp.Poly(octic, A))])
faces, _, G, DD = enumerate_faces(['a','b','c','us','u','C1','C2'], (), maxsize=2)
xs = dict(faces)[('C1','C2')]
N = T**2*(f**3 - 5*f**2 + 32*f - 196) + T*(6*f**3 - 30*f**2 + 96*f + 168) + 9*f**3 + 3*f**2 - 48*f - 36
fb = mp.findroot(lambda z: sp.lambdify((f, T), sp.diff(N, f), 'mpmath')(z, Tb), mp.mpf('0.4467'))
vals = {str(k): sp.lambdify((f, T), v, 'mpmath')(fb, Tb) for k, v in xs.items()}
print('crossing (Wouter-type) blow-up at alpha_b: f_ac =', fb)
print('  x_a =', vals['a'], ' x_b =', vals['b'], ' x_c =', vals['c'], ' x_d = x_e =', vals['s']/2, ' f_de =', vals['u']/vals['s'])
a_, b_, c_, s_, u_ = [vals[k] for k in 'abcsu']
print('  density =', a_*b_ + b_*c_ + fb*a_*c_ + a_*s_ + u_*s_/4, ' both triangle sums =', 1 + b_ + fb*(a_ + c_), 1 + a_ - (1 - fb)*c_ + u_)
k = 2*mp.sqrt(((Tb+3)**2/48)/3)
print('Fan blow-up at alpha_b: x_b = %s, x_a = x_c = %s, f_ac = %s' % (1 - k, k/2, 4*((Tb+3)**2/48 - k*(1-k))/k**2))
