# test whether sq(G) <= K via SAT (imports the independent checker). usage: sat_le.py level n K idx...
import sys; sys.path.insert(0, sys.argv[0].rsplit('/',1)[0])
import satcheck, numpy as np
fn,n,K=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); D=np.fromfile(fn,dtype=np.uint32).reshape(-1,n)
for i in sys.argv[4:]:
    G=satcheck.graph([int(x) for x in D[int(i)]]); E,L=satcheck.strong_conflict(G)
    print(f'idx {i}: sq<={K}: {satcheck.colorable(L,K)}',flush=True)
