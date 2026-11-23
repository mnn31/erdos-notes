# Lift a mod-p hit to an exact Q-certificate:  target = sum_c coeff * (minor of 2*Gram) * monomial ; verify exactly.
import sympy as sp, itertools, pickle, sys, json
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
def setup(f,nv):
    d=sp.symbols(f'd0:{nv}')
    cls={}
    for c,m in enumerate(f):
        for e in m: cls[tuple(e)]=c
    npts=1+max(max(e) for m in f for e in m)
    D=lambda i,j: 0 if i==j else d[cls[(min(i,j),max(i,j))]]
    G=sp.Matrix(npts-1,npts-1,lambda i,j: (D(0,i+1)+D(0,j+1)-D(i+1,j+1)))
    mins={}
    for r in itertools.combinations(range(npts-1),3):
        for c in itertools.combinations(range(npts-1),3):
            if r<=c:
                m=sp.expand(G.extract(list(r),list(c)).det())
                if m!=0 and m not in mins.values(): mins[(r,c)]=m
    return d,G,mins
def lift(f,nv,target_str,deg):
    d,G,mins=setup(f,nv)
    loc={str(s):s for s in d}
    target=sp.expand(sp.sympify(target_str,locals=loc))
    mons=[sp.Mul(*c) for c in itertools.combinations_with_replacement(d,deg-3)] if deg>3 else [sp.Integer(1)]
    gens=[(k,mo,sp.Poly(m*mo,*d)) for k,m in mins.items() for mo in mons]
    allm=sorted(set().union(*[g.monoms() for _,_,g in gens])|set(sp.Poly(target,*d).monoms()))
    idx={m:i for i,m in enumerate(allm)}
    rows=[[QQ(0)]*(len(gens)+1) for _ in allm]
    for j,(_,_,g) in enumerate(gens):
        for mo,c in g.terms(): rows[idx[mo]][j]=QQ(int(c))
    for mo,c in sp.Poly(target,*d).terms(): rows[idx[mo]][len(gens)]=QQ(int(c))
    A=DomainMatrix(rows,(len(allm),len(gens)+1),QQ)
    R,piv=A.rref()
    if len(gens) in piv: return None
    Rl=R.to_Matrix()
    sol=[0]*len(gens)
    for i,p in enumerate(piv): sol[p]=Rl[i,len(gens)]
    tot=sp.expand(sum(s*g.as_expr() for s,(_,_,g) in zip(sol,gens) if s!=0))
    assert sp.expand(tot-target)==0
    cert=[(str(s),list(k[0]),list(k[1]),str(mo)) for s,(k,mo,_) in zip(sol,gens) if s!=0]
    return cert
if __name__=='__main__':
    reps=pickle.load(open(sys.argv[1],'rb')); k=int(sys.argv[2]); tgt=sys.argv[3]; deg=int(sys.argv[4])
    c=lift(reps[k],len(reps[k]),tgt,deg)
    print('rep',k,'target',tgt,'certificate terms:',None if c is None else len(c))
    if c: json.dump({'rep':reps[k],'target':tgt,'matrix':'M_ij = D(0,i)+D(0,j)-D(i,j), i,j=1..n-1 (twice the Gram matrix)','terms':c},open(sys.argv[5],'w'),indent=0)
