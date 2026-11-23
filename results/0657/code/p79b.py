import sympy as sp
exec(open('p79.py').read().split('# numeric solution')[0])
E=list(dict.fromkeys(eqs))
t=sp.symbols('t')
sub={u:(1-t**2)/(1+t**2), v:2*t/(1+t**2)}
Es=[sp.factor(sp.together(e.subs(sub))) for e in E]
Es=[sp.numer(e) for e in Es]
GB=sp.groebner(Es,b1,b2,c1,c2,t,order='lex')
for g in GB.exprs: print(sp.factor(g))
