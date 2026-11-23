# vectorised membership test: which products of k factors from {d_i, d_i-d_j, d_i+d_j} lie in V_k (mod p)
import sympy as sp, itertools, pickle, sys, numpy as np
from memtest import build, P
def kernel_mod(B,piv,N):
    free=[c for c in range(N) if c not in piv]
    K=np.zeros((len(free),N),dtype=np.int64)
    for a,fc in enumerate(free):
        K[a,fc]=1
        for i,pc in enumerate(piv): K[a,pc]=(-B[i,fc])%P
    return K
reps=pickle.load(open(sys.argv[1],'rb')); ri=int(sys.argv[2]); k=int(sys.argv[3]); f=reps[ri]; nv=len(f)
withsum=len(sys.argv)>4
d,idx,B,piv,N=build(f,nv,k)
K=kernel_mod(B,piv,N); print('rep',ri,'deg',k,'dim V',len(piv),'codim',K.shape[0],flush=True)
assert not ((B@K.T)%P).any()
lin=[]
for i in range(nv):
    e=[0]*nv; e[i]=1; lin.append(({tuple(e):1},f'd{i}'))
for i,j in itertools.combinations(range(nv),2):
    ei=[0]*nv; ei[i]=1; ej=[0]*nv; ej[j]=1
    lin.append(({tuple(ei):1,tuple(ej):P-1},f'(d{i}-d{j})'))
    if withsum: lin.append(({tuple(ei):1,tuple(ej):1},f'(d{i}+d{j})'))
def mul(p,q):
    r={}
    for a,ca in p.items():
        for b,cb in q.items():
            m=tuple(x+y for x,y in zip(a,b)); r[m]=(r.get(m,0)+ca*cb)%P
    return r
hits=[]; batch=[]; names=[]
def flush():
    global batch,names
    if not batch: return
    M=np.zeros((len(batch),N),dtype=np.int64)
    for r,pd in enumerate(batch):
        for m,c in pd.items(): M[r,idx[m]]=c
    Z=(M@K.T)%P
    for r in np.nonzero(~Z.any(axis=1))[0]: hits.append(names[r])
    batch=[];names=[]
def dfs(start,depth,poly,name):
    if depth==k:
        batch.append(poly); names.append(name)
        if len(batch)>=20000: flush()
        return
    for i in range(start,len(lin)):
        dfs(i,depth+1,mul(poly,lin[i][0]),name+'*'+lin[i][1])
dfs(0,0,{tuple([0]*nv):1},'')
flush()
print('hits',len(hits)); 
# prefer hits with fewest factors of type d_i (pure) -- print a few
for h in hits[:20]: print('HIT',h[1:])
