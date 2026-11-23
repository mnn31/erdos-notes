# Independent check of sieve flags: for each line "S T d c sq", recompute by trial division which
# classes (3 / 5 / 7 / 11..Y) contain a prime p with |d|<p that divides T+d exactly once, and
# whether some such sieved prime has p^2 | T+d.
import sys
Y=int(sys.argv[2]); ps=[p for p in range(3,Y+1) if all(p%q for q in range(2,int(p**.5)+1))]
cls=lambda p: 0 if p==3 else 1 if p==5 else 2 if p==7 else 3
bad=0; n=0
for line in open(sys.argv[1]):
    _,T,d,c,sq=line.split(); T=int(T); d=int(d); c=int(c); sq=int(sq); N=T+d
    cc=0; ss=0
    for p in ps:
        if abs(d)>=p: continue
        if N%p==0:
            if N%(p*p): cc|=1<<cls(p)
            else: ss=1
    n+=1
    if cc!=c or ss!=sq: bad+=1; print("MISMATCH",line.strip(),cc,ss) if bad<5 else None
print("lines",n,"mismatches",bad)
