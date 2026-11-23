# For each near-1-factorization rep of K7: span V_k of (3x3 minors of Gram) * (monomials of degree k-3).
# Test whether products of k factors from {d_i} U {d_i - d_j} lie in V_k (mod p first, fast).
import sympy as sp, itertools, pickle, sys, numpy as np
reps=pickle.load(open('../out/nf7_reps.pkl','rb'))
d=sp.symbols('d0:7')
P=1000003
def rank_mod(M):
    M=M.copy()%P; r=0; rows,cols=M.shape
    for c in range(cols):
        piv=None
        for i in range(r,rows):
            if M[i,c]: piv=i;break
        if piv is None: continue
        M[[r,piv]]=M[[piv,r]]
        inv=pow(int(M[r,c]),P-2,P); M[r]=(M[r]*inv)%P
        for i in range(rows):
            if i!=r and M[i,c]: M[i]=(M[i]-M[i,c]*M[r])%P
        r+=1
        if r==rows: break
    return r
def minors_of(f):
    cls={}
    for c,m in enumerate(f):
        for e in m: cls[tuple(e)]=c
    D=lambda i,j: 0 if i==j else d[cls[(min(i,j),max(i,j))]]
    G=sp.Matrix(6,6,lambda i,j: sp.Rational(1,2)*(D(0,i+1)+D(0,j+1)-D(i+1,j+1)))
    out=set()
    for r in itertools.combinations(range(6),3):
        for c in itertools.combinations(range(6),3):
            if r<=c:
                m=sp.expand(2*G.extract(list(r),list(c)).det()*4)
                if m!=0: out.add(m)
    return [sp.Poly(m,*d) for m in out]
k=int(sys.argv[1]) if len(sys.argv)>1 else 3
facs=list(d)+[d[i]-d[j] for i,j in itertools.combinations(range(7),2)]
for ri,f in enumerate(reps):
    mins=minors_of(f)
    mons=[sp.Poly(sp.Mul(*c),*d) for c in itertools.combinations_with_replacement(d,k-3)] if k>3 else [sp.Poly(1,*d)]
    gens=[m*mo for m in mins for mo in mons]
    allmon=sorted(set().union(*[g.monoms() for g in gens]))
    # monomials of degree k
    allmon=sorted(set(itertools.chain.from_iterable([g.monoms() for g in gens])))
    idx={m:i for i,m in enumerate(allmon)}
    M=np.zeros((len(gens),len(allmon)),dtype=np.int64)
    for a,g in enumerate(gens):
        for mo,c in g.terms():
            M[a,idx[mo]]=int(c)%P
    r0=rank_mod(M)
    hits=[]
    for combo in itertools.combinations_with_replacement(range(len(facs)),k):
        # require at least one difference factor (pure monomials d^a are positive; also interesting)
        t=sp.Poly(sp.Mul(*[facs[i] for i in combo]),*d)
        if any(mo not in idx for mo in t.monoms()): continue
        row=np.zeros((1,len(allmon)),dtype=np.int64)
        for mo,c in t.terms(): row[0,idx[mo]]=int(c)%P
        if rank_mod(np.vstack([M,row]))==r0:
            hits.append(sp.factor(t.as_expr()))
            break
    print('rep',ri,'deg',k,'#gens',len(gens),'rank',r0,'of',len(allmon),'hit:',hits[:1],flush=True)
