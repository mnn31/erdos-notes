# membership of candidate products in V_k = span(minors * monomials of degree k-3), mod p, via one RREF.
import sympy as sp, itertools, pickle, sys, numpy as np
P=32003
def rref_mod(M):
    M=M.copy()%P; r=0; rows,cols=M.shape; piv=[]
    for c in range(cols):
        nz=np.nonzero(M[r:,c])[0]
        if len(nz)==0: continue
        i=r+nz[0]; M[[r,i]]=M[[i,r]]
        M[r]=(M[r]*pow(int(M[r,c]),P-2,P))%P
        col=M[:,c].copy(); col[r]=0
        M=(M-np.outer(col,M[r]))%P
        piv.append(c); r+=1
        if r==rows: break
    return M[:r],piv
def reduce(v,B,piv):
    v=v.copy()%P
    for i,c in enumerate(piv):
        if v[c]: v=(v-v[c]*B[i])%P
    return not v.any()
def build(f,nv,k):
    d=sp.symbols(f'd0:{nv}')
    cls={}
    for c,m in enumerate(f):
        for e in m: cls[tuple(sorted(e))]=c
    npts=1+max(max(e) for m in f for e in m)
    D=lambda i,j: 0 if i==j else d[cls[(min(i,j),max(i,j))]]
    G=sp.Matrix(npts-1,npts-1,lambda i,j:(D(0,i+1)+D(0,j+1)-D(i+1,j+1)))
    mins=set()
    for r in itertools.combinations(range(npts-1),3):
        for c in itertools.combinations(range(npts-1),3):
            if r<=c:
                m=sp.expand(G.extract(list(r),list(c)).det())
                if m!=0: mins.add(m)
    mons=[sp.Mul(*c) for c in itertools.combinations_with_replacement(d,k-3)]
    allm=[m for m in sp.itermonomials(d,k,k)]
    allm=sorted(sp.Poly(m,*d).monoms()[0] for m in allm)
    idx={m:i for i,m in enumerate(allm)}
    rows=[]
    for m in mins:
        for mo in mons:
            v=np.zeros(len(allm),dtype=np.int64)
            for t,c in sp.Poly(m*mo,*d).terms(): v[idx[t]]=int(c)%P
            rows.append(v)
    B,piv=rref_mod(np.array(rows))
    return d,idx,B,piv,len(allm)
if __name__=='__main__':
    reps=pickle.load(open(sys.argv[1],'rb')); ri=int(sys.argv[2]); k=int(sys.argv[3]); f=reps[ri]; nv=len(f)
    d,idx,B,piv,N=build(f,nv,k)
    print('rep',ri,'deg',k,'dim V',len(piv),'of',N,flush=True)
    facs=list(d)+[d[i]-d[j] for i,j in itertools.combinations(range(nv),2)]+[d[i]+d[j] for i,j in itertools.combinations(range(nv),2)]
    hits=0
    for combo in itertools.combinations_with_replacement(range(len(facs)),k):
        if all(facs[i] in d or len(facs[i].args)==2 and facs[i].args[1].could_extract_minus_sign()==False and '+' in str(facs[i]) for i in combo):
            pass
        t=sp.Poly(sp.Mul(*[facs[i] for i in combo]),*d)
        v=np.zeros(N,dtype=np.int64)
        for mo,c in t.terms(): v[idx[mo]]=int(c)%P
        if reduce(v,B,piv):
            print('HIT',sp.factor(t.as_expr()),flush=True); hits+=1
            if hits>=3: break
    print('done hits',hits)
