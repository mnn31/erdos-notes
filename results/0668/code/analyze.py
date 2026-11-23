import sys; sys.path.insert(0,'.')
from graphs import *
import networkx as nx
for n,c in CODES.items():
    nn,E=dec(c); assert nn==n
    adj=adjacency(n,E)
    T=triangles(n,E); C4=four_cycles(n,E)
    G=nx.Graph(E)
    print('n=%d |E|=%d (u=%d) degs=%s'%(n,len(E),U[n],sorted(len(a) for a in adj)))
    print('  triangles(%d):'%len(T),T)
    print('  4-cycles(%d):'%len(C4),C4)
    # K4 minus edge? diagonals of 4-cycles that are edges
    print('  4-cycles with an edge diagonal:',[q for q in C4 if q[2] in adj[q[0]] or q[3] in adj[q[1]]])
    from networkx.algorithms.isomorphism import GraphMatcher
    print('  |Aut|=',sum(1 for _ in GraphMatcher(G,G).isomorphisms_iter()))
    print('  E=',E)
