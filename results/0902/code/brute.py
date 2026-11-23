"""Independent brute-force check (no reductions): enumerate ALL connection sets S of a
small group, build the full tournament x->y iff x^{-1}y in S, and test every k-subset of
vertices for a common dominator outside it. Prints the sorted list of S with property S_k.
Group (m,k,r,d): elements (x,y,w); product computed by composing affine maps z -> x + r^y z
on Z_m, adding y mod k and w mod d. Index = ((x*k)+y)*d + w (same labelling as groups.h)."""
import sys, itertools
def group(m,k,r,d):
    els=[(x,y,w) for x in range(m) for y in range(k) for w in range(d)]
    idx={e:i for i,e in enumerate(els)}
    def mul(a,b):
        (x1,y1,w1),(x2,y2,w2)=a,b
        # affine composition: (z->x1+c1 z) o (z->x2+c2 z) = z -> x1 + c1 x2 + c1 c2 z
        c1=pow(r,y1,m)
        return ((x1+c1*x2)%m,(y1+y2)%k,(w1+w2)%d)
    n=len(els); M=[[idx[mul(a,b)] for b in els] for a in els]
    inv=[next(j for j in range(n) if M[i][j]==0) for i in range(n)]
    assert all(M[inv[i]][i]==0 for i in range(n))
    return n,M,inv
def has_Sk(n,M,inv,S,k):
    Sset=set(S)
    inn=[0]*n   # inn[v] = bitmask of z with z->v
    for z in range(n):
        for v in range(n):
            if M[inv[z]][v] in Sset: inn[v]|=1<<z
    for A in itertools.combinations(range(n),k):
        b=(1<<n)-1
        for v in A: b&=inn[v]
        if b==0: return False
    return True
def main():
    m,kk,r,d,K=map(int,sys.argv[1:6])
    n,M,inv=group(m,kk,r,d)
    pairs=[];seen={0}
    for g in range(1,n):
        if g not in seen: pairs.append((g,inv[g])); seen|={g,inv[g]}
    out=[]
    for bits in itertools.product((0,1),repeat=len(pairs)):
        S=sorted(p[b] for p,b in zip(pairs,bits))
        if has_Sk(n,M,inv,S,K): out.append(S)
    for S in sorted(out): print("S: "+" ".join(map(str,S)))
    print("count",len(out),file=sys.stderr)
main()
