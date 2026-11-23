"""Computational checks of Lemmas 1, 2, 4 and Theorem B of WRITEUP.md (corroboration of the
hand proofs; the hand proofs do not depend on these runs except where stated)."""
import sys, itertools
sys.path.insert(0, sys.path[0])
import networkx as nx
from gstar import groetzsch, gstar, indep_sets, triangle_free
from pysat.solvers import Cadical153

def colourable(G, k):
    V = list(G.nodes()); idx = {v: i for i, v in enumerate(V)}
    var = lambda v, c: idx[v]*k + c + 1
    s = Cadical153()
    for v in V: s.add_clause([var(v, c) for c in range(k)])
    for u, w in G.edges():
        for c in range(k): s.add_clause([-var(u, c), -var(w, c)])
    r = s.solve(); m = set(x for x in (s.get_model() or []) if x > 0); s.delete()
    if not r: return None
    col = {v: min(c for c in range(k) if var(v, c) in m) for v in V}
    assert all(col[u] != col[w] for u, w in G.edges()); return col

def mycielski(G, tag):
    """M(G): vertices ('o',x) originals, ('c',x) copies, ('w',tag) hub."""
    M = nx.Graph()
    for x in G.nodes(): M.add_node(('o', x)); M.add_node(('c', x))
    M.add_node(('w', tag))
    for x, y in G.edges():
        M.add_edge(('o', x), ('o', y)); M.add_edge(('c', x), ('o', y)); M.add_edge(('c', y), ('o', x))
    for x in G.nodes(): M.add_edge(('c', x), ('w', tag))
    return M

def chi(G, lo=1):
    k = lo
    while colourable(G, k) is None: k += 1
    return k

Gr = groetzsch()
print('Groetzsch: n', Gr.number_of_nodes(), 'm', Gr.number_of_edges(), 'triangle-free', triangle_free(Gr),
      'iso to networkx mycielski_graph(4):', nx.is_isomorphic(Gr, nx.mycielski_graph(4)), 'chi', chi(Gr))

# Lemma 4: the colouring kappa (outer cycle 0,1,0,1,2; copy 5+i gets kappa(i); hub 10 gets 3)
kappa = {0: 0, 1: 1, 2: 0, 3: 1, 4: 2}
kappa.update({5+i: kappa[i] for i in range(5)}); kappa[10] = 3
assert all(kappa[u] != kappa[v] for u, v in Gr.edges())
I = indep_sets(Gr)
rainbow = [S for S in I if {kappa[s] for s in S} == {0, 1, 2, 3}]
print('Lemma 4: kappa proper; #independent sets of Groetzsch', len(I), '; #rainbow (meeting all 4 classes):', len(rainbow),
      '; max |I| containing hub:', max(len(S) for S in I if 10 in S), '; alpha', max(len(S) for S in I))

# corroboration of Lemmas 3+4 via the scout reduction: the rule-based 5-colouring of G*(Groetzsch) is proper
G = gstar(Gr); col = {}
for v in G.nodes():
    if v[0] == 'h': col[v] = kappa[int(v[1:])]
    elif v[0] == 'a': col[v] = 4
    else:
        S = [int(x) for x in v[2:-1].split(',') if x]
        col[v] = min({0, 1, 2, 3} - {kappa[s] for s in S})
print('G*(Groetzsch):', G.number_of_nodes(), 'vertices,', G.number_of_edges(), 'edges; rule-based 5-colouring proper:',
      all(col[u] != col[w] for u, w in G.edges()))

# Theorem B (upper bound): M(M(Groetzsch)) = Mycielski graph M_6
M1 = mycielski(Gr, 1); M2 = mycielski(M1, 2)
S = [('o', ('o', h)) for h in Gr.nodes()] + [('w', 2)]
R = M2.copy(); R.remove_nodes_from(S)
X = [('o', ('w', 1)), ('c', ('w', 1))] + [('c', ('o', h)) for h in Gr.nodes()]
Y = [('o', ('c', h)) for h in Gr.nodes()] + [('c', ('c', h)) for h in Gr.nodes()]
assert set(X) | set(Y) == set(R.nodes()) and not set(X) & set(Y)
bip_ok = all((u in X) != (v in X) for u, v in R.edges())
print('M(M(Groetzsch)): n', M2.number_of_nodes(), 'm', M2.number_of_edges(), 'triangle-free', triangle_free(M2),
      '| iso to networkx mycielski_graph(6):', nx.is_isomorphic(M2, nx.mycielski_graph(6)))
print('  |S| =', len(S), '; M2 - S has', R.number_of_nodes(), 'vertices; explicit bipartition X,Y proper:', bip_ok,
      '; nx.is_bipartite:', nx.is_bipartite(R))
c5 = colourable(M2, 5); c6 = colourable(M2, 6)
print('  5-colourable (CaDiCaL):', c5 is not None, '; 6-colourable (CaDiCaL, colouring re-checked):', c6 is not None)

# sanity: same construction for r = 4, 5 (H = K2, C5) gives OCT <= 3, 6 matching g(4)=3, g(5)=6
for nm, H, r in [('K2', nx.complete_graph(2), 4), ('C5', nx.cycle_graph(5), 5)]:
    MM = mycielski(mycielski(H, 1), 2)
    R2 = MM.copy(); R2.remove_nodes_from([('o', ('o', h)) for h in H.nodes()] + [('w', 2)])
    print(f'  r={r}: H={nm}, M(M(H)) n={MM.number_of_nodes()} tf={triangle_free(MM)} chi={chi(MM)} '
          f'deleting |H|+1={H.number_of_nodes()+1} vertices leaves bipartite: {nx.is_bipartite(R2)}')
