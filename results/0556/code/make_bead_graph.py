# Builds the 31-vertex "four beads on an 11-cycle" graph (Example E1 in WRITEUP.md).
# C = v0..v10 (vertices 0..10). Windows {0,1,2},{3,4,5},{6,7,8},{9,10,0}.
# Each window gets 5 private vertices forming K5, each joined to all 3 window vertices.
edges = set()
for i in range(11): edges.add(tuple(sorted((i, (i+1) % 11))))
nxt = 11
for W in [(0,1,2),(3,4,5),(6,7,8),(9,10,0)]:
    P = list(range(nxt, nxt+5)); nxt += 5
    for a in range(5):
        for b in range(a+1,5): edges.add((P[a],P[b]))
        for w in W: edges.add(tuple(sorted((P[a], w))))
import sys
out = sys.argv[1]
with open(out,'w') as f:
    f.write(f"{nxt} {len(edges)}\n")
    for (a,b) in sorted(edges): f.write(f"{a} {b}\n")
print(nxt, len(edges))
