import sympy as sp, itertools, pickle, sys, time
reps=pickle.load(open('../out/nf7_reps.pkl','rb'))
k=int(sys.argv[1]); f=reps[k]
d=sp.symbols('d0:7')
cls={}
for c,m in enumerate(f):
    for e in m: cls[tuple(e)]=c
D=lambda i,j: 0 if i==j else d[cls[(min(i,j),max(i,j))]]
G=sp.Matrix(6,6,lambda i,j: (D(0,i+1)+D(0,j+1)-D(i+1,j+1)))
mins=set()
for r in itertools.combinations(range(6),3):
    for c in itertools.combinations(range(6),3):
        if r<=c:
            m=sp.expand(G.extract(list(r),list(c)).det())
            if m!=0: mins.add(m)
t=time.time()
GB=sp.groebner(list(mins),*d,order='grevlex',modulus=32003)
print('rep',k,'GB size',len(GB.exprs),'time',round(time.time()-t,1),flush=True)
for g in GB.exprs:
    print(' ',sp.factor(g.as_expr(),modulus=32003))
