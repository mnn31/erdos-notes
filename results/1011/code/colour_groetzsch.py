"""Find a proper 5-colouring of G*(Groetzsch) and save it (out/gstar_groetzsch_5col.json)."""
import sys, json
sys.path.insert(0, sys.path[0])
from gstar import groetzsch, gstar, triangle_free
from pysat.solvers import Cadical153
H = groetzsch(); G = gstar(H); k = 5
print('|V(G*)|', G.number_of_nodes(), '|E|', G.number_of_edges(), 'triangle-free', triangle_free(G))
V = sorted(G.nodes()); idx = {v: i for i, v in enumerate(V)}
var = lambda v, c: idx[v]*k + c + 1
s = Cadical153()
for v in V: s.add_clause([var(v, c) for c in range(k)])
for u, v in G.edges():
    for c in range(k): s.add_clause([-var(u, c), -var(v, c)])
assert s.solve()
m = set(x for x in s.get_model() if x > 0)
col = {v: min(c for c in range(k) if var(v, c) in m) for v in V}
json.dump(col, open(sys.argv[1], 'w'), indent=0, sort_keys=True)
print('saved colouring, colours used', sorted(set(col.values())))
