# Independent exact verification of a certificate JSON (no sympy): evaluate both sides with Fractions on the
# grid {0..deg}^nv. Both sides are polynomials of total degree <= deg, so agreement on the grid proves identity.
import json, sys, itertools, re
from fractions import Fraction as Fr
C=json.load(open(sys.argv[1])); rep=C['rep']; nv=len(rep)
cls={}
for c,m in enumerate(rep):
    for e in m: cls[tuple(sorted(e))]=c
npts=1+max(max(e) for m in rep for e in m)
assert len(cls)==npts*(npts-1)//2
def ev(expr,d):  # evaluate simple sympy-printed polynomial expression safely
    return eval(re.sub(r'd(\d+)',r'd[\1]',expr).replace('^','**'),{'__builtins__':{}},{'d':d})
def det3(M): return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
terms=[(Fr(s),r,c,mo) for s,r,c,mo in C['terms']]
deg=max(3+sum(int(x) if x else 1 for x in re.findall(r'\*\*(\d+)|d\d+',mo) ) if mo!='1' else 3 for *_,mo in terms)
deg=max(deg, 3)
# crude total degree of monomial strings: count variables with powers
def mdeg(mo):
    if mo=='1': return 0
    t=0
    for part in mo.split('*'):
        pass
    return sum(int(p) if p.isdigit() else 0 for p in re.findall(r'\*\*(\d+)',mo))+len(re.findall(r'd\d+(?!\*\*)',mo))
deg=3+max(mdeg(mo) for *_,mo in terms)
D=lambda d,i,j: 0 if i==j else d[cls[(min(i,j),max(i,j))]]
bad=0; cnt=0
for d in itertools.product(range(deg+1),repeat=nv):
    d=list(map(Fr,d))
    G=[[D(d,0,i+1)+D(d,0,j+1)-D(d,i+1,j+1) for j in range(npts-1)] for i in range(npts-1)]
    s=sum(c*det3([[G[a][b] for b in cc] for a in r])*ev(mo,d) for c,r,cc,mo in terms)
    if s!=ev(C['target'],d): bad+=1
    cnt+=1
print(sys.argv[1],': degree',deg,'grid points',cnt,'failures',bad)
