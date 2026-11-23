# Exhaustive enumeration (up to isomorphism) of graphs on n<=7 labelled vertices that are
# K4-free and K_{2,3}-free (no two vertices with >=3 common neighbours).
# Canonical form = minimum edge-bitmask over all n! vertex permutations (exact, no hashing).
import itertools, sys, numpy as np
def run(n):
    E=list(itertools.combinations(range(n),2)); idx={e:i for i,e in enumerate(E)}
    perms=list(itertools.permutations(range(n)))
    PE=np.array([[idx[tuple(sorted((p[a],p[b])))] for a,b in E] for p in perms],dtype=np.int64)
    W=(np.int64(1)<<PE)  # weight of edge e under perm p
    def canon(mask):
        bits=np.array([(mask>>i)&1 for i in range(len(E))],dtype=np.int64)
        return int((W*bits).sum(1).min())
    def ok(mask):
        adj=[0]*n
        for i,(a,b) in enumerate(E):
            if mask>>i&1: adj[a]|=1<<b; adj[b]|=1<<a
        for a,b in E:
            if bin(adj[a]&adj[b]).count('1')>=3: return False
        for q in itertools.combinations(range(n),4):
            if all(mask>>idx[(x,y)]&1 for x,y in itertools.combinations(q,2)): return False
        return True
    layers=[{0}]
    while True:
        nxt=set()
        for g in layers[-1]:
            for i in range(len(E)):
                if not g>>i&1:
                    h=g|1<<i
                    if ok(h): nxt.add(canon(h))
        if not nxt: break
        layers.append(nxt)
    return E,layers
if __name__=="__main__":
    for n in range(3,8):
        E,L=run(n)
        print("n=%d counts by m:"%n,[len(l) for l in L], "max m:",len(L)-1)
        for m in range(max(0,len(L)-3),len(L)):
            for g in sorted(L[m]):
                print("  m=%d"%m,[E[i] for i in range(len(E)) if g>>i&1])
