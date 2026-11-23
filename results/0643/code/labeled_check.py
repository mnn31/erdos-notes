# For a dump of isomorphism classes (from classify), compute sum over classes of
# n!/|Aut(G)| per size = number of labeled families; compare with dfs_count.
# Also re-verify avoidance by definition and that classes are pairwise non-isomorphic.
# Usage: python3 -I labeled_check.py n dumpfile
import sys, itertools
from math import factorial
n=int(sys.argv[1]); fams=[]
for line in open(sys.argv[2]):
    w=line.split(); fams.append(frozenset(tuple(int(c) for c in s) for s in w[1:]))
def avoiding(F):
    F=[frozenset(t) for t in F]; seen=set()
    for i in range(len(F)):
        for j in range(i+1,len(F)):
            if not (F[i]&F[j]):
                U=F[i]|F[j]
                if U in seen: return False
                seen.add(U)
    return True
perms=list(itertools.permutations(range(n)))
tot={}; canon=set()
for F in fams:
    assert avoiding(F)
    aut=0; best=None
    for p in perms:
        img=frozenset(tuple(sorted(p[v] for v in t)) for t in F)
        if img==F: aut+=1
        key=tuple(sorted(img))
        if best is None or key<best: best=key
    assert best not in canon, "two isomorphic classes"
    canon.add(best)
    tot[len(F)]=tot.get(len(F),0)+factorial(n)//aut
print("classes",len(fams),"labeled counts by size",dict(sorted(tot.items())))
