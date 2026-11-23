# CP-SAT: is there an avoiding family of 3-subsets of [n] with >= k members?
# Usage: python3 -I cpsat.py n k timelimit workers
import sys, itertools, time
from ortools.sat.python import cp_model
n,k,tl,w=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4])
T=list(itertools.combinations(range(n),3)); idx={t:i for i,t in enumerate(T)}
m=cp_model.CpModel(); x=[m.NewBoolVar(str(t)) for t in T]
for S in itertools.combinations(range(n),6):
    parts=[]
    for A in itertools.combinations(S,3):
        if A[0]!=S[0]: continue
        B=tuple(v for v in S if v not in A); parts.append((idx[A],idx[B]))
    for (a,b),(c,d) in itertools.combinations(parts,2):
        m.AddBoolOr([x[a].Not(),x[b].Not(),x[c].Not(),x[d].Not()])
    # redundant cut: at most 11 triples inside a 6-set
    m.Add(sum(x[idx[A]] for A in itertools.combinations(S,3))<=11)
F7={6:11,7:17}
if n>=8:
    for S in itertools.combinations(range(n),7):
        m.Add(sum(x[idx[A]] for A in itertools.combinations(S,3))<=17)
m.Add(sum(x)>=k)
s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=w
t0=time.time(); r=s.Solve(m)
print(n,k,s.StatusName(r),round(time.time()-t0,1),'s')
if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    print([T[i] for i in range(len(T)) if s.Value(x[i])])
