# Sanity check of the graph lists: line counts versus OEIS A000664 (refs/b000664.txt), every line a
# simple graph with exactly e edges (no loops, no repeated edges) and no isolated vertex
# (vertex labels 0..n-1 all used).
import sys
gd, bfile = sys.argv[1], sys.argv[2]
oeis = {int(a): int(b) for a, b in (l.split() for l in open(bfile) if l.strip() and not l.startswith('#'))}
for e in range(1, int(sys.argv[3]) + 1):
    n = 0; ok = True
    for line in open(f'{gd}/g{e}.txt'):
        if not line.strip(): continue
        n += 1
        E = [tuple(map(int, t.split('-'))) for t in line.split()]
        S = {frozenset(x) for x in E}
        V = {v for x in E for v in x}
        if len(E) != e or len(S) != e or any(a == b for a, b in E) or V != set(range(len(V))): ok = False
    print(f'e={e} graphs={n} OEIS={oeis[e]} {"MATCH" if n == oeis[e] else "MISMATCH"} wellformed={ok}')
