# Graph-theoretic facts used in WRITEUP.md (Lemma G).  Uses the networkx graph atlas
# (all graphs on <=7 vertices up to isomorphism, 1253 graphs) and cross-checks enum_graphs.py.
import itertools, networkx as nx, sys
from networkx.generators.atlas import graph_atlas_g
sys.path.insert(0, __import__('os').path.dirname(__file__))
import enum_graphs
def ok(G):
    for a,b in itertools.combinations(G.nodes,2):
        if len(set(G[a])&set(G[b]))>=3: return False      # K_{2,3}
    for q in itertools.combinations(G.nodes,4):
        if G.subgraph(q).number_of_edges()==6: return False # K_4
    return True
atlas=[G for G in graph_atlas_g() if G.number_of_nodes()==7]
print("atlas: number of graphs on 7 vertices:",len(atlas))
cnt={}
for G in atlas:
    if ok(G): cnt[G.number_of_edges()]=cnt.get(G.number_of_edges(),0)+1
E,L=enum_graphs.run(7)
print("K4/K23-free graphs on 7 vertices by #edges, atlas:",[cnt.get(m,0) for m in range(0,14)])
print("                                      enum_graphs:",[len(L[m]) if m<len(L) else 0 for m in range(0,14)])
assert [cnt.get(m,0) for m in range(0,14)]==[len(L[m]) if m<len(L) else 0 for m in range(0,14)]
A=nx.Graph([(0,3),(0,4),(0,5),(0,6),(1,2),(1,5),(1,6),(2,4),(2,6),(3,4),(3,5)])
B=nx.Graph([(0,4),(0,5),(0,6),(1,2),(1,3),(1,5),(1,6),(2,4),(2,6),(3,4),(3,5)])
C=nx.Graph([(0,2),(0,4),(0,5),(0,6),(1,2),(1,3),(1,6),(2,6),(3,4),(3,5),(4,5)])
for nm,X in zip("ABC",(A,B,C)): assert ok(X) and X.number_of_edges()==11 and min(d for _,d in X.degree())==3
S=[G for G in atlas if ok(G) and G.number_of_edges()==11 and min(d for _,d in G.degree())>=3]
names=[[nm for nm,X in zip("ABC",(A,B,C)) if nx.is_isomorphic(G,X)] for G in S]
print("K4/K23-free 7-vertex 11-edge graphs with min degree >=3:",len(S),"isomorphic to",names)
assert sorted(sum(names,[]))==["A","B","C"]
# 3-regular graphs on 6 vertices
R6=[G for G in graph_atlas_g() if G.number_of_nodes()==6 and all(d==3 for _,d in G.degree())]
print("3-regular graphs on 6 vertices:",len(R6),"; K4/K23-free among them:",sum(ok(G) for G in R6),
      "; that one is the prism:",[nx.is_isomorphic(G,nx.circular_ladder_graph(3)) for G in R6 if ok(G)])
print("GRAPH FACTS OK")
