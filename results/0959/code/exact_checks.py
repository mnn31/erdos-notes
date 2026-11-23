# Exact computations used in WRITEUP.md (Lemmas C1-C6).  Pure rational arithmetic.
# Part 1 (lattice part): points of Q(w), w = exp(i pi/3), written z = x + y w with x,y in Q.
#   |x + y w|^2 = x^2 + x y + y^2.
# Part 2 (constructions): Cartesian points with coordinates in Q(sqrt3), numbers p + q*sqrt3.
from fractions import Fraction as F
import itertools
# ---------------- Part 1 ----------------
def N(p,q): dx=p[0]-q[0]; dy=p[1]-q[1]; return dx*dx+dx*dy+dy*dy
def conj(p): return (p[0]+p[1], -p[1])           # conj(w) = 1 - w
def mul(p,q):
    a,b=p; c,d=q; return (a*c-b*d, a*d+b*c+b*d)   # w^2 = w - 1
def sub(p,q): return (p[0]-q[0],p[1]-q[1])
def add(p,q): return (p[0]+q[0],p[1]+q[1])
def scal(r,p): return (r*p[0],r*p[1])
def inv(p):
    n=N(p,(0,0)); c=conj(p); return (c[0]/n,c[1]/n)
W=(F(0),F(1)); ONE=(F(1),F(0)); I3=sub(scal(2,W),ONE)   # 2w-1 = i*sqrt3
def common_unit_neighbours(s,t):
    """All points v with |v-s|=|v-t|=1, for s,t in Q(w) with D=|s-t|^2 in {1,3,4} (else returns None if D<4 not handled)."""
    D=N(s,t)
    if D>4: return []
    h={F(1):F(1,2),F(3):F(1,6),F(4):F(0)}.get(D)
    if h is None: raise ValueError("unexpected D=%s"%D)
    m=scal(F(1,2),add(s,t)); d=mul(I3,sub(t,s))
    out={add(m,scal(h,d)),add(m,scal(-h,d))}
    for v in out: assert N(v,s)==1 and N(v,t)==1
    return sorted(out)
def circumcenter(a,b,c):
    B=sub(b,a); C=sub(c,a)
    den=sub(mul(conj(B),C),mul(B,conj(C)))
    if den==(0,0): return None
    num=sub(scal(N(B,(0,0)),C),scal(N(C,(0,0)),B))
    o=add(mul(num,inv(den)),a)
    assert N(o,a)==N(o,b)==N(o,c)
    return o
def units(P): return sum(1 for p,q in itertools.combinations(P,2) if N(p,q)==1)
def mults(P):
    d={}
    for p,q in itertools.combinations(P,2): d[N(p,q)]=d.get(N(p,q),0)+1
    return d
def canon(P):
    forms=[]; r=ONE
    for k in range(6):
        for refl in (False,True):
            Q=[mul(conj(p) if refl else p, r) for p in P]
            m=min(Q); forms.append(tuple(sorted(sub(q,m) for q in Q)))
        r=mul(r,W)
    return min(forms)
def show(P): return "{"+", ".join("%s+%s*w"%(a,b) for a,b in P)+"}"
def unit_degree(v,P): return sum(1 for p in P if N(v,p)==1)
def new_points_with_k_neighbours(P,k):
    """all v not in P at unit distance from >=k points of P, k in {2,3}: v is a common unit neighbour of some pair."""
    cand=set()
    for s,t in itertools.combinations(P,2):
        for v in common_unit_neighbours(s,t):
            if v not in P: cand.add(v)
    return [v for v in cand if unit_degree(v,P)>=k]
log=[]
def say(*a):
    s=" ".join(str(x) for x in a); print(s)
# C1: rhombus R = {0,1,w,1+w}? no: rhombus = two unit triangles sharing an edge: {0,1,w,1-w... } use {0,1,w,w-1}? take {0,1,w,1+w}? |1+w|^2=3, triangles (0,1,w),(1,w,1+w)
R=[(F(0),F(0)),(F(1),F(0)),(F(0),F(1)),(F(1),F(1))]
assert units(R)==5
say("C1: rhombus R =",show(R),"unit distances:",units(R))
ext=new_points_with_k_neighbours(R,2)
say("  points outside R with >=2 unit neighbours in R:",[(show([v]),unit_degree(v,R)) for v in ext])
assert all(unit_degree(v,R)==2 for v in ext), "a point with 3 unit nbrs would give u(5)>=8"
L57=set(canon(R+[v]) for v in ext)
say("  => 5-point sets with 7 unit distances, up to congruence:",[show(P) for P in L57])
assert len(L57)==1
T=list(next(iter(L57)))
say("  trapezoid T =",show(T),"multiplicities {squared distance: count}:",{str(k):v for k,v in mults(T).items()})
# C2: no point outside T has 3 unit neighbours in T  (=> u(6)<=9);  6-point lattice sets with 9 unit distances
ext=new_points_with_k_neighbours(T,2)
assert all(unit_degree(v,T)==2 for v in ext)
say("C2: points outside T with >=2 unit nbrs in T:",len(ext),"; all have exactly 2 (so no 6-point set with 10 unit distances)")
L69=sorted(set(canon(T+[v]) for v in ext))
say("  lattice-type 6-point sets with 9 unit distances (up to congruence):",len(L69))
for P in L69: say("   ",show(P),"units",units(P),"mults",{str(k):v for k,v in sorted(mults(P).items())})
# C3: 7-point sets with 12 unit distances whose 6-point subset is lattice-type: add v with 3 unit nbrs
res=set()
for H in L69:
    H=list(H)
    for v in new_points_with_k_neighbours(H,3):
        assert unit_degree(v,H)==3
        res.add(canon(H+[v]))
say("C3: 7-point sets with 12 unit distances (lattice case):",len(res))
for P in res:
    m=mults(P); say("   ",show(P),"units",units(P),"mults",{str(k):v for k,v in sorted(m.items())})
# C4: 7-point sets with 11 unit distances obtained as lattice-type L(6,9) + v with exactly 2 unit nbrs
res=set()
for H in L69:
    H=list(H)
    for v in new_points_with_k_neighbours(H,2):
        if unit_degree(v,H)==2: res.add(canon(H+[v]))
say("C4: 7-point sets with 11 unit distances, lattice case:",len(res))
minf2=99
for P in sorted(res):
    m=mults(P); assert units(P)==11
    f2=max(c for k,c in m.items() if k!=1); minf2=min(minf2,f2)
    say("   ",show(P),"f2 =",f2,"mults",{str(k):v for k,v in sorted(m.items())})
say("  minimum f2 over C4 configurations:",minf2)
assert minf2>=2
# ---------------- Part 2: constructions, Q(sqrt3) arithmetic ----------------
class Q3:
    __slots__=("p","q")
    def __init__(s,p,q=0): s.p=F(p); s.q=F(q)
    def __add__(s,o): o=o if isinstance(o,Q3) else Q3(o); return Q3(s.p+o.p,s.q+o.q)
    def __sub__(s,o): o=o if isinstance(o,Q3) else Q3(o); return Q3(s.p-o.p,s.q-o.q)
    def __mul__(s,o): o=o if isinstance(o,Q3) else Q3(o); return Q3(s.p*o.p+3*s.q*o.q, s.p*o.q+s.q*o.p)
    def __eq__(s,o): o=o if isinstance(o,Q3) else Q3(o); return s.p==o.p and s.q==o.q
    def __hash__(s): return hash((s.p,s.q))
    def __repr__(s): return ("%s%s%s*sqrt3"%(s.p,"+" if s.q>0 else "-",abs(s.q))) if s.q else str(s.p)
def pt(x,y): return (x if isinstance(x,Q3) else Q3(x), y if isinstance(y,Q3) else Q3(y))
def padd(a,b): return (a[0]+b[0],a[1]+b[1])
def d2(a,b): dx=a[0]-b[0]; dy=a[1]-b[1]; return dx*dx+dy*dy
def report(name,P):
    n=len(P)
    assert all(not(P[i][0]==P[j][0] and P[i][1]==P[j][1]) for i,j in itertools.combinations(range(n),2)), "not injective"
    m={}
    for i,j in itertools.combinations(range(n),2):
        k=d2(P[i],P[j]); m[k]=m.get(k,0)+1
    cnt=sorted(m.values(),reverse=True)
    gap=cnt[0]-cnt[1] if len(cnt)>1 else None
    say(name,": n =",n,"; sorted multiplicities",cnt,"; #distinct distances",len(m),"; gap f(d1)-f(d2) =",gap)
    say("   squared distances with multiplicity:",{repr(k):v for k,v in m.items()})
    return gap
A=pt(0,0); B=pt(1,0); C=pt(F(1,2),Q3(0,F(1,2)))        # unit equilateral triangle, C=(1/2, sqrt3/2)
u=pt(F(3,5),F(4,5))                                     # unit translation vector (3/5,4/5)
g5=report("n=5 trapezoid",[A,B,pt(2,0),C,padd(C,B)])
g6=report("n=6 prism T_u",[A,B,C,padd(A,u),padd(B,u),padd(C,u)])
r=pt(F(5,13),F(-12,13))                                 # second unit vector
g7=report("n=7 prism T_u + (A+r)",[A,B,C,padd(A,u),padd(B,u),padd(C,u),padd(A,r)])
assert (g5,g6,g7)==(5,8,9)
say("ALL EXACT CHECKS PASSED")
