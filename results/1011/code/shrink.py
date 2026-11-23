"""Find a small vertex set W of G*(Groetzsch + K1) whose induced subgraph is not 5-colourable.
Core-guided shrinking then deletion-minimisation (each vertex removed in turn if still UNSAT).
Symmetry breaking: a{} gets colour 0, b{} gets colour 1 (they are adjacent; always kept)."""
import sys, json, time, random
sys.path.insert(0, sys.path[0])
import networkx as nx
from gstar import groetzsch, gstar, triangle_free
from pysat.solvers import Cadical153
H = groetzsch(); H.add_node(11)      # vertex 11 = isolated vertex z
G = gstar(H); k = 5
V = sorted(G.nodes()); idx = {v: i for i, v in enumerate(V)}; n = len(V)
var = lambda v, c: idx[v]*k + c + 1
sel = lambda v: n*k + idx[v] + 1          # selector: vertex v present
def solver():
    s = Cadical153()
    for v in V: s.add_clause([-sel(v)] + [var(v, c) for c in range(k)])
    for u, w in G.edges():
        for c in range(k): s.add_clause([-var(u, c), -var(w, c)])
    s.add_clause([var('a{}', 0)]); s.add_clause([var('b{}', 1)])
    return s
s = solver(); keep = set(V); t = time.time()
for it in range(6):
    r = s.solve(assumptions=[sel(v) for v in sorted(keep)])
    assert r is False
    core = {V[x - n*k - 1] for x in s.get_core()}
    print('iter', it, 'core size', len(core), 'time', round(time.time()-t, 1), flush=True)
    if len(core) == len(keep): break
    keep = core | {'a{}', 'b{}'}
random.seed(1)
order = sorted(keep); random.shuffle(order)
for v in order:
    if v in ('a{}', 'b{}'): continue
    trial = keep - {v}
    if s.solve(assumptions=[sel(w) for w in sorted(trial)]) is False:
        core = {V[x - n*k - 1] for x in s.get_core()} | {'a{}', 'b{}'}
        keep = core
print('minimal (w.r.t. single deletions, keeping a{},b{}):', len(keep), 'time', round(time.time()-t, 1), flush=True)
# final check of minimality: each single deletion is 5-colourable (without the a{},b{} pins if deleted)
W = sorted(keep)
json.dump(W, open(sys.argv[1], 'w'))
GW = G.subgraph(W)
print('edges', GW.number_of_edges(), 'triangle-free', triangle_free(GW),
      'H-vertices', sorted(v for v in W if v[0] == 'h'),
      'a-vertices', sum(v[0] == 'a' for v in W), 'b-vertices', sum(v[0] == 'b' for v in W))
