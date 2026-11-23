import sympy as sp, itertools
from fractions import Fraction as Fr
exec(open('p79.py').read().split('# numeric solution')[0])
E=list(dict.fromkeys(eqs))
def check(Pt):
    D={e:(Pt[e[0]][0]-Pt[e[1]][0])**2+(Pt[e[0]][1]-Pt[e[1]][1])**2 for e in itertools.combinations(range(7),2)}
    vals=sorted(set(D.values()))
    iso=[(a,b,c) for a,b,c in itertools.combinations(range(7),3) if len({D[(a,b)],D[(a,c)],D[(b,c)]})<3]
    return len(vals),iso,D
found=[]
for tv in [sp.Rational(s,1)*sp.Rational(m*m+1,2*m) if False else None for s in [] for m in []]: pass
cands=set()
for m in range(1,12):
    for k in range(1,12):
        if sp.gcd(m,k)==1:
            tt=sp.Rational(m*m+k*k,2*m*k)   # t^2-1 = ((m^2-k^2)/(2mk))^2
            if tt!=1: cands|={tt,-tt}
for tv in sorted(cands,key=lambda x:abs(x)):
    uv={u:(1-tv**2)/(1+tv**2), v:2*tv/(1+tv**2)}
    sols=sp.solve([e.subs(uv) for e in E],[b1,b2,c1,c2],dict=True)
    for s in sols:
        if not all(val.is_rational for val in s.values()): continue
        Pt={0:(1,0),1:(-1,0),2:(s[b1],s[b2]),3:(-s[b1],-s[b2]),5:(s[c1],s[c2]),6:(-s[c1],-s[c2]),4:(uv[u],uv[v])}
        Pt={k:(Fr(int(sp.numer(a)),int(sp.denom(a))),Fr(int(sp.numer(b)),int(sp.denom(b)))) for k,(a,b) in Pt.items()}
        if len(set(Pt.values()))<7: continue
        n,iso,D=check(Pt)
        if not iso: found.append((tv,n,Pt))
        if not iso: print('t=',tv,'distinct distances',n, {k:(str(a),str(b)) for k,(a,b) in sorted(Pt.items())},flush=True)
    if len(found)>=3: break
