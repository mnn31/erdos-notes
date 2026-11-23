import sympy as sp, itertools, pickle, sys, time
reps=pickle.load(open('../out/nf7_reps.pkl','rb'))
k=int(sys.argv[1]); sub=sys.argv[2] if len(sys.argv)>2 else 'all'
f=reps[k]
d=sp.symbols('d0:7')
cls={}
for c,m in enumerate(f):
    for e in m: cls[tuple(e)]=c
D=lambda i,j: 0 if i==j else d[cls[(min(i,j),max(i,j))]]
pts=list(range(7)) if sub=='all' else [int(x) for x in sub.split(',')]
b=pts[0]; rest=pts[1:]
G=sp.Matrix(len(rest),len(rest),lambda i,j: sp.Rational(1,2)*(D(b,rest[i])+D(b,rest[j])-D(rest[i],rest[j])))
mins=set()
for r in itertools.combinations(range(len(rest)),3):
    for c in itertools.combinations(range(len(rest)),3):
        if r<=c:
            m=sp.expand(G.extract(list(r),list(c)).det())
            if m!=0: mins.add(m)
t=time.time()
GB=sp.groebner(list(mins),*d,order='grevlex')
print('rep',k,'pts',pts,'minors',len(mins),'GB size',len(GB.exprs),'time',round(time.time()-t,1))
for g in GB.exprs:
    fg=sp.factor(g)
    if sp.Poly(g,*d).total_degree()<=3: print(' ',fg)
