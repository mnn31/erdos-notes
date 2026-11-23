# Lemma 7 test: among all 10-edge graphs (no isolated vertices), count those in which some two
# vertices u,v cover >= 6 edges (then colouring the covered edges blue and the rest red is good),
# and check the explicit colouring of Lemma 7 with the independent verifier.
import sys, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('vw', os.path.join(here, 'verify_witness.py'))
vw = importlib.util.module_from_spec(spec); spec.loader.exec_module(vw)
F1, F2 = [2, 2, 1], [2, 1, 1]
cov = rest = bad = 0
for line in open(sys.argv[1]):
    E = [tuple(map(int, t.split('-'))) for t in line.split()]
    V = sorted({x for e in E for x in e})
    best = None
    for i, u in enumerate(V):
        for v in V[i:]:
            c = sum(1 for e in E if u in e or v in e)
            if best is None or c > best[0]: best = (c, u, v)
    if best[0] >= 6:
        cov += 1
        u, v = best[1], best[2]
        R = {x: set() for x in V}; B = {x: set() for x in V}
        for a, b in E:
            D = B if (u in (a, b) or v in (a, b)) else R
            D[a].add(b); D[b].add(a)
        if vw.contains(R, F1) or vw.contains(B, F2): bad += 1
    else:
        rest += 1
print(f'10-edge graphs: two vertices cover >=6 edges: {cov} (colouring of Lemma 7 fails on {bad}); remaining: {rest}')
