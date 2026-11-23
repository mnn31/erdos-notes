# Definition-based avoidance check of every family in a dump file (vertices may be
# multi-digit only as "10"/"11", so triples are parsed by a greedy rule on known n).
# Usage: python3 -I check_avoid.py n dumpfile
import sys, itertools
n=int(sys.argv[1])
names={str(v):v for v in range(n)}
def parse(s):
    # split a concatenation of three vertex labels in increasing order
    for i in range(1,len(s)):
        for j in range(i+1,len(s)):
            a,b,c=s[:i],s[i:j],s[j:]
            if a in names and b in names and c in names and names[a]<names[b]<names[c]:
                return (names[a],names[b],names[c])
    raise ValueError(s)
def avoiding(F):
    F=[frozenset(t) for t in F]; seen=set()
    for i in range(len(F)):
        for j in range(i+1,len(F)):
            if not (F[i]&F[j]):
                U=F[i]|F[j]
                if U in seen: return False
                seen.add(U)
    return True
for line in open(sys.argv[2]):
    w=line.split(); F=[parse(s) for s in w[1:]]
    assert len(F)==int(w[0]) and len(set(F))==len(F)
    deg=[sum(v in t for t in F) for v in range(n)]
    print(len(F),'avoiding' if avoiding(F) else 'NOT AVOIDING','degrees',sorted(deg,reverse=True))
