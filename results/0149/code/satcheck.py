# Independent exact strong chromatic index via networkx + SAT (pysat/CaDiCaL).
# usage: python3 -I satcheck.py levelfile n idx [idx...]   (idx = record index in level file)
import sys; sys.path.append("~/.local/lib/python3.11/site-packages")  # user site for pysat (-I drops it)
import itertools, numpy as np, networkx as nx
from pysat.solvers import Cadical153
from pysat.card import CardEnc
def graph(rows):
    n=len(rows); G=nx.Graph(); G.add_nodes_from(range(n))
    G.add_edges_from((i,j) for i in range(n) for j in range(i+1,n) if rows[i]>>j&1); return G
def strong_conflict(G):
    E=list(G.edges()); L=nx.Graph(); L.add_nodes_from(range(len(E)))
    for a,b in itertools.combinations(range(len(E)),2):
        (u,v),(x,y)=E[a],E[b]
        if {u,v}&{x,y} or any(G.has_edge(p,q) for p in (u,v) for q in (x,y)): L.add_edge(a,b)
    return E,L
def colorable(L,k):
    V=list(L.nodes()); var=lambda v,c: v*k+c+1
    s=Cadical153()
    for v in V: s.add_clause([var(v,c) for c in range(k)])
    for a,b in L.edges():
        for c in range(k): s.add_clause([-var(a,c),-var(b,c)])
    # symmetry breaking: vertices of a max clique get fixed colours
    Q=max(nx.find_cliques(L),key=len)
    for i,v in enumerate(Q): s.add_clause([var(v,i)])
    if len(Q)>k: return False
    r=s.solve(); s.delete(); return r
def sq(rows):
    G=graph(rows); assert all(d==4 for _,d in G.degree()); E,L=strong_conflict(G)
    w=max(len(c) for c in nx.find_cliques(L)); k=w
    while not colorable(L,k): k+=1
    return k,w
if __name__=='__main__':
    fn,n=sys.argv[1],int(sys.argv[2]); D=np.fromfile(fn,dtype=np.uint32).reshape(-1,n)
    for i in sys.argv[3:]:
        rows=[int(x) for x in D[int(i)]]; k,w=sq(rows); print(f'idx {i}: sq={k} omega={w} connected={nx.is_connected(graph(rows))}',flush=True)
