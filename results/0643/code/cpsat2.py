# Independent CP-SAT check: avoiding family of >= k triples on [n]?
# Clause model + symmetry breaking deg(0)>=deg(1)>=...>=deg(n-1) (valid: relabel vertices).
# Usage: python3 -I cpsat2.py n k timelimit workers
import sys, itertools, time
from ortools.sat.python import cp_model
n,k,tl,w=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4])
T=list(itertools.combinations(range(n),3)); idx={t:i for i,t in enumerate(T)}
m=cp_model.CpModel(); x=[m.NewBoolVar(str(t)) for t in T]
for S in itertools.combinations(range(n),6):
    parts=[(idx[A],idx[tuple(v for v in S if v not in A)]) for A in itertools.combinations(S,3) if A[0]==S[0]]
    for (a,b),(c,d) in itertools.combinations(parts,2):
        m.AddBoolOr([x[a].Not(),x[b].Not(),x[c].Not(),x[d].Not()])
    m.Add(sum(x[idx[A]] for A in itertools.combinations(S,3))<=11)
deg=[sum(x[i] for i,t in enumerate(T) if v in t) for v in range(n)]
for v in range(n-1): m.Add(deg[v]>=deg[v+1])
m.Add(sum(x)>=k)
s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=w
t0=time.time(); r=s.Solve(m)
print(n,k,s.StatusName(r),round(time.time()-t0,1),'s',flush=True)
if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    print([T[i] for i in range(len(T)) if s.Value(x[i])])
