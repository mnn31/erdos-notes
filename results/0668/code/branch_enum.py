# Exhaustive exact enumeration of triangle-orientation branches for the AMP25 graphs.
# See WRITEUP.md, Lemmas 1-4.  Usage: python3 -I branch_enum.py
import sys, os, itertools, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graphs import *
from qw import *

class RREF:
    """Incremental reduced row echelon form over Q(w) on n columns."""
    def __init__(s,n): s.n=n; s.rows={}   # pivot col -> row (list), row[pivot]=1
    def copy(s):
        t=RREF(s.n); t.rows={k:list(v) for k,v in s.rows.items()}; return t
    def reduce(s,r):
        r=list(r)
        for p,row in s.rows.items():
            if not iszero(r[p]):
                c=r[p]; r=[sub(x,mul(c,y)) for x,y in zip(r,row)]
        return r
    def add(s,r):
        r=s.reduce(r)
        piv=next((j for j in range(s.n) if not iszero(r[j])),None)
        if piv is None: return False
        c=inv(r[piv]); r=[mul(c,x) for x in r]
        for p in list(s.rows):
            row=s.rows[p]
            if not iszero(row[piv]):
                c2=row[piv]; s.rows[p]=[sub(x,mul(c2,y)) for x,y in zip(row,r)]
        s.rows[piv]=r; return True
    def kernel(s):
        free=[j for j in range(s.n) if j not in s.rows]
        B=[]
        for f in free:
            v=[Z]*s.n; v[f]=ONE
            for p,row in s.rows.items(): v[p]=neg(row[f])
            B.append(v)
        return B   # list of kernel basis vectors
    def in_rowspace(s,r): return all(iszero(x) for x in s.reduce(r))

def rhombus_row(n,a,b,c,d):
    r=[Z]*n; r[a]=add(r[a],ONE); r[c]=add(r[c],ONE); r[b]=sub(r[b],ONE); r[d]=sub(r[d],ONE); return r
def tri_row(n,a,b,c,s):
    # orientation s=+1: p_c - p_a = w (p_b - p_a);  s=-1: p_c - p_a = conj(w)(p_b - p_a)
    om = W if s==1 else WB
    r=[Z]*n; r[c]=add(r[c],ONE); r[a]=sub(r[a],ONE); r[b]=sub(r[b],om); r[a]=add(r[a],om); return r
def diff(n,u,v):
    r=[Z]*n; r[u]=ONE; r[v]=neg(ONE); return r

def collision(M,n):
    for u in range(n):
        for v in range(u+1,n):
            if M.in_rowspace(diff(n,u,v)): return (u,v)
    return None

def run(n,E):
    T=triangles(n,E); C4=four_cycles(n,E)
    M0=RREF(n)
    for q in C4: M0.add(rhombus_row(n,*q))
    stats={'nodes':0,'pruned':0,'leaves':[]}
    prunelog=[]
    def dfs(k,M,sig):
        stats['nodes']+=1
        col=collision(M,n)
        if col is not None:
            stats['pruned']+=1; prunelog.append((sig,col)); return
        if k==len(T):
            stats['leaves'].append((sig,M)); return
        for s in ((1,) if k==0 else (1,-1)):
            M2=M.copy(); M2.add(tri_row(n,*T[k],s)); dfs(k+1,M2,sig+(s,))
    dfs(0,M0,())
    return T,C4,M0,stats,prunelog

if __name__=='__main__':
    res={}
    for n,c in CODES.items():
        _,E=dec(c)
        T,C4,M0,st,pl=run(n,E)
        print('n=%d: rhombus-only kernel dim=%d; DFS nodes=%d, pruned by forced coincidence=%d, surviving leaves=%d'
              %(n,n-len(M0.rows),st['nodes'],st['pruned'],len(st['leaves'])))
        for sig,M in st['leaves']:
            print('   leaf sigma=%s kernel dim=%d'%(''.join('+' if s>0 else '-' for s in sig), n-len(M.rows)))
        res[n]=[sig for sig,M in st['leaves']]
        print('   triangles (in branching order):',T)
        for sig,col in pl: print('   pruned prefix %-18s forces p_%d = p_%d'%(''.join('+' if s>0 else '-' for s in sig),col[0],col[1]))
        sys.stdout.flush()
    json.dump({str(k):v for k,v in res.items()},open(sys.argv[1] if len(sys.argv)>1 else 'leaves.json','w'))
