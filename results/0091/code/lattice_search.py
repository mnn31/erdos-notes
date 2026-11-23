"""Sanity search (NOT load-bearing): largest subsets of the triangular lattice with <= k distinct
distances, using only distances whose squared norm is in a small window.  Lattice point (a,b)
means a*1 + b*w, w = e^{i pi/3}; squared distance of (a,b) is a^2+ab+b^2 (exact integers).
For every k-subset S of the Loeschian numbers <= NMAX we take the graph on lattice points within
squared radius max(S) of the origin, edges = pairs whose squared distance lies in S, and find all
maximum cliques through the origin.  Output: size of the largest set found and the list of sets
found at that size (up to translation), with a float similarity canonical form."""
import itertools, sys, cmath, math
import networkx as nx

def N(a,b): return a*a+a*b+b*b
def loesch(nmax): return sorted({N(a,b) for a in range(-10,11) for b in range(-10,11)} - {0} & set(range(nmax+1)))

def cz(p): return complex(p[0]+p[1]/2, p[1]*math.sqrt(3)/2)

def canon(P):
    """float canonical form up to similarity (incl. reflections): min over ordered pairs (p,q) at
    the min distance of the sorted rounded image under z -> (z-p)/(q-p), with and without conj."""
    Z=[cz(p) for p in P]; best=None
    dmin=min(abs(a-b) for a,b in itertools.combinations(Z,2))
    for refl in (False,True):
        ZZ=[z.conjugate() for z in Z] if refl else Z
        for i,j in itertools.permutations(range(len(ZZ)),2):
            if abs(abs(ZZ[i]-ZZ[j])-dmin)>1e-9: continue
            img=tuple(sorted((round(((z-ZZ[i])/(ZZ[j]-ZZ[i])).real,6)+0.0, round(((z-ZZ[i])/(ZZ[j]-ZZ[i])).imag,6)+0.0) for z in ZZ))
            if best is None or img<best: best=img
    return best

def run(k, nmax):
    L=loesch(nmax); best=0; found={}
    for S in itertools.combinations(L,k):
        S=set(S); R=max(S)
        r=int(math.isqrt(4*R))+2
        V=[(a,b) for a in range(-r,r+1) for b in range(-r,r+1) if (a,b)!=(0,0) and N(a,b) in S]
        G=nx.Graph(); G.add_nodes_from(V)
        for u,v in itertools.combinations(V,2):
            if N(u[0]-v[0],u[1]-v[1]) in S: G.add_edge(u,v)
        for C in nx.find_cliques(G):
            sz=len(C)+1
            if sz<best: continue
            P=[(0,0)]+C
            c=canon(P)
            if sz>best: best=sz; found={}
            found.setdefault(c,(sorted(P), sorted({N(p[0]-q[0],p[1]-q[1]) for p,q in itertools.combinations(P,2)})))
    return best, found

if __name__=="__main__":
    for k,nmax in [(4,21),(5,21),(6,28)]:
        best,found=run(k,nmax)
        print(f"k={k} (squared distances from Loeschian numbers <= {nmax}): max lattice set size {best}; "
              f"{len(found)} similarity class(es) found at that size")
        for c,(P,D) in found.items():
            print("   points", P, " squared distances", D)
        sys.stdout.flush()
