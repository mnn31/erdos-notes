"""G*(H) construction (Definition 1 of WRITEUP). Vertices are strings:
  'h<v>'          vertex v of H
  'a<sorted I>'   a_I   e.g. 'a{0,3,7}'  ('a{}' for the empty set)
  'b<sorted I>'   b_I
Edges: edges of H; a_I - s, b_I - s for s in I; a_I - b_J iff I and J are disjoint."""
import itertools, networkx as nx

def groetzsch():
    """Groetzsch graph = Mycielskian of C5, written out explicitly:
    0..4 outer 5-cycle, 5..9 copies (5+i adjacent to the two cycle-neighbours of i), 10 hub."""
    E = [(i, (i+1) % 5) for i in range(5)]
    E += [(5+i, (i+1) % 5) for i in range(5)] + [(5+i, (i-1) % 5) for i in range(5)]
    E += [(10, 5+i) for i in range(5)]
    G = nx.Graph(); G.add_nodes_from(range(11)); G.add_edges_from(E); return G

def indep_sets(H):
    V = sorted(H.nodes()); out = [frozenset()]
    for v in V:
        out += [S | {v} for S in out if not any(H.has_edge(v, u) for u in S)]
    return out

def name(c, S): return c + '{' + ','.join(map(str, sorted(S))) + '}'

def gstar(H):
    I = indep_sets(H); G = nx.Graph()
    for v in H.nodes(): G.add_node('h%d' % v)
    for u, v in H.edges(): G.add_edge('h%d' % u, 'h%d' % v)
    for S in I:
        G.add_node(name('a', S)); G.add_node(name('b', S))
        for s in S:
            G.add_edge(name('a', S), 'h%d' % s); G.add_edge(name('b', S), 'h%d' % s)
    for S in I:
        for T in I:
            if not (S & T): G.add_edge(name('a', S), name('b', T))
    return G

def triangle_free(G):
    return all(not (set(G[u]) & set(G[v])) for u, v in G.edges())
