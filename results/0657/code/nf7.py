# enumerate near-1-factorizations of K7 (7 matchings of size 3 partitioning E(K7)), orbits under S7
import itertools, pickle
n=7
E=[frozenset(e) for e in itertools.combinations(range(n),2)]
NM=[frozenset(m) for m in itertools.combinations(E,3) if len(set().union(*m))==6]
facts=[]
def rec(rem,chosen):
    if not rem: facts.append(frozenset(chosen)); return
    e=min(rem,key=lambda x:sorted(x))
    for m in NM:
        if e in m and m<=rem:
            rec(rem-m,chosen+[m])
rec(frozenset(E),[])
facts=set(facts)
print('labelled near-1-factorizations of K7:',len(facts))
def act(p,f): return frozenset(frozenset(frozenset(p[v] for v in e) for e in m) for m in f)
seen=set(); reps=[]
perms=list(itertools.permutations(range(n)))
for f in sorted(facts,key=lambda f:sorted(sorted(sorted(e) for e in m) for m in f)):
    if f in seen: continue
    orb=set(act(p,f) for p in perms)
    assert orb<=facts
    seen|=orb; reps.append((f,len(orb)))
print('orbits:',len(reps),'sizes',[s for _,s in reps],'sum',sum(s for _,s in reps))
pickle.dump([[sorted(sorted(e) for e in m) for m in f] for f,_ in reps],open('../out/nf7_reps.pkl','wb'))
for f,s in reps: print(s,[sorted(tuple(sorted(e)) for e in m) for m in f])
