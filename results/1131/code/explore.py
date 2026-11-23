import sympy as sp
x,u,v,s,d,w=sp.symbols('x u v s d w')
nodes=[-1,u,v,1]
I=0
for k,xk in enumerate(nodes):
    num=sp.Integer(1); den=sp.Integer(1)
    for j,xj in enumerate(nodes):
        if j!=k: num*=(x-xj); den*=(xk-xj)
    I+=sp.integrate(sp.expand(num**2),(x,-1,1))/den**2
I=sp.factor(sp.together(I))
print(I)
P,Q=sp.fraction(I)
print('degP',sp.Poly(P,u,v).total_degree(),'Q',sp.factor(Q))
# symmetric check
print(sp.simplify(I.subs({u:-sp.sqrt(s),v:sp.sqrt(s)})))
# s,d coords: u=(s-d)/2, v=(s+d)/2
J=sp.factor(sp.together(I.subs({u:(s-d)/2,v:(s+d)/2})))
print(J)
