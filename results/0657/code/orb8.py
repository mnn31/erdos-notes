# orbit representatives (under S7) of partitions of E(K7) into exactly 8 matchings
import itertools, pickle, time
n=7
E=list(itertools.combinations(range(n),2)); eid={e:i for i,e in enumerate(E)}
vm=[(1<<a)|(1<<b) for a,b in E]
M=[]
for k in (1,2,3):
    for c in itertools.combinations(range(21),k):
        vs=0; ok=True
        for i in c:
            if vs & vm[i]: ok=False;break
            vs|=vm[i]
        if ok: M.append(sum(1<<i for i in c))
bylow={}
for m in M: bylow.setdefault((m&-m).bit_length()-1,[]).append(m)
pats=[]
def rec(rem,ch):
    if rem==0:
        if len(ch)==8: pats.append(tuple(sorted(ch)))
        return
    if len(ch)==8 or bin(rem).count('1')>3*(8-len(ch)): return
    low=(rem&-rem).bit_length()-1
    for m in bylow[low]:
        if m&rem==m: rec(rem^m,ch+[m])
t=time.time(); rec((1<<21)-1,[]); print('labelled',len(pats),time.time()-t,flush=True)
perms=list(itertools.permutations(range(n)))
ptab=[[eid[tuple(sorted((p[a],p[b])))] for a,b in E] for p in perms]
def mapmask(tab,m):
    r=0
    while m:
        lb=m&-m; i=lb.bit_length()-1; r|=1<<tab[i]; m^=lb
    return r
seen=set(); reps=[]
for P in pats:
    if P in seen: continue
    orb=set()
    for tab in ptab:
        orb.add(tuple(sorted(mapmask(tab,m) for m in P)))
    seen|=orb; reps.append((P,len(orb)))
print('orbits',len(reps),'sum',sum(s for _,s in reps),time.time()-t)
out=[[[E[i] for i in range(21) if m>>i&1] for m in P] for P,_ in reps]
pickle.dump(out,open('../out/k7_8class_reps.pkl','wb'))
