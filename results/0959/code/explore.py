# Numerical exploration (NOT a proof): for each candidate unit-distance graph G on n vertices
# with m edges, sample realisations by least squares and record distance multiplicities.
import itertools, sys, numpy as np, networkx as nx
from scipy.optimize import least_squares
rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv)>3 else 1)
n = int(sys.argv[1]); mmin = int(sys.argv[2])

def ok(G):
    # K4-free and K_{2,3}-free (two vertices with >=3 common neighbours)
    for a,b in itertools.combinations(G.nodes,2):
        if len(set(G[a])&set(G[b]))>=3: return False
    for q in itertools.combinations(G.nodes,4):
        if G.subgraph(q).number_of_edges()==6: return False
    return True

def graphs(n, mmax):
    layers=[[nx.empty_graph(n)]]
    for m in range(1,mmax+1):
        seen={}
        out=[]
        for G in layers[-1]:
            for e in itertools.combinations(range(n),2):
                if G.has_edge(*e): continue
                H=G.copy(); H.add_edge(*e)
                if not ok(H): continue
                h=nx.weisfeiler_lehman_graph_hash(H,iterations=4)
                lst=seen.setdefault(h,[])
                if any(nx.is_isomorphic(H,K) for K in lst): continue
                lst.append(H); out.append(H)
        layers.append(out)
        if not out: break
    return layers

layers=graphs(n, 30)
print("counts by m:", [len(l) for l in layers])
iu=list(itertools.combinations(range(n),2))
best=[]
for m in range(mmin, len(layers)):
    for G in layers[m]:
        E=list(G.edges)
        def res(x):
            P=x.reshape(n,2)
            return [np.sum((P[a]-P[b])**2)-1 for a,b in E]
        found={}
        for t in range(int(sys.argv[4]) if len(sys.argv)>4 else 300):
            x0=rng.normal(size=2*n)*1.0
            r=least_squares(res,x0,xtol=1e-15,ftol=1e-15,gtol=1e-15,max_nfev=2000)
            if np.max(np.abs(r.fun))>1e-10: continue
            P=r.x.reshape(n,2)
            D=np.array([np.linalg.norm(P[a]-P[b]) for a,b in iu])
            if D.min()<1e-4: continue
            unit=sum(abs(D-1)<1e-7)
            if unit!=m: continue  # unit graph strictly larger
            nu=sorted(D[abs(D-1)>=1e-7])
            cl=[];
            for d in nu:
                if cl and abs(d-cl[-1][0])<1e-7: cl[-1][1]+=1
                else: cl.append([d,1])
            f2=max(c for _,c in cl) if cl else 0
            key=tuple(sorted(c for _,c in cl))
            if key not in found: found[key]=(f2,P.copy())
        for key,(f2,P) in found.items():
            best.append((m-f2,m,f2,key,sorted(E)))
best.sort(key=lambda t:-t[0])
for b in best[:25]: print(b)
