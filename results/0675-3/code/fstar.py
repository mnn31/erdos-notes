# F*(p): least N such that every nonzero class r mod p contains two elements of E cap [1,N]
# that are distinct mod p^2 (E = sums of two squares). By Lemma 2 of WRITEUP.md, p | t for every
# n-shift t as soon as n >= F*(p), and (Prop. 14) no argument using only the p-local condition can do
# better. Also Bbox(p): least B such that every nonzero class contains two distinct values x^2+y^2
# with |x|,|y| < B. Run: python3 -I fstar.py [PMAX]   (numpy; PMAX=20000 takes a few minutes)
import math, sys, numpy as np

PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20000

def primes(n):
    s = bytearray([1])*(n+1); s[0] = s[1] = 0
    for i in range(2, int(n**.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]

L = 60*PMAX*int(math.log(PMAX)+1)
E = np.zeros(L+1, dtype=bool)
for x in range(0, math.isqrt(L)+1):
    ys = np.arange(0, math.isqrt(L - x*x)+1)
    E[x*x + ys*ys] = True
E[0] = False
Elist = np.flatnonzero(E)

def fstar(p):
    # scan elements of E in increasing order; need, per class r != 0, two elements distinct mod p^2
    first = np.full(p, -1, dtype=np.int64); done = np.zeros(p, dtype=bool); done[0] = True
    left = p - 1; P2 = p*p
    for a in Elist:
        r = a % p
        if done[r]: continue
        if first[r] < 0: first[r] = a % P2
        elif a % P2 != first[r]:
            done[r] = True; left -= 1
            if left == 0: return int(a)
    return None

def bbox(p):
    # least B: every class r != 0 gets two distinct integer values x^2+y^2 with 0<=x,y<B
    vals = [set() for _ in range(p)]
    good = 0; B = 0
    while True:
        B += 1; b = B - 1
        for x in range(B):
            for v in {x*x + b*b}:
                r = v % p
                if r and len(vals[r]) < 2:
                    vals[r].add(v)
                    if len(vals[r]) == 2: good += 1
        if good == p - 1: return B

rows = []
for p in primes(PMAX):
    if p % 4 != 3: continue
    F = fstar(p)
    assert F is not None, p
    rows.append((p, F))
print("p, F*(p), F*/p, log F*/log p, F*/(p log p sqrt(log p))  [selected]")
sel = set([3, 7, 11, 19, 23, 31, 43, 103, 211, 499, 1019, 2003, 4003, 8011, 16007]) 
for (p, F) in rows:
    if p in sel or p == rows[-1][0]:
        print(p, F, round(F/p, 2), round(math.log(F)/math.log(p), 4), round(F/(p*math.log(p)**1.5), 3))
mx = max(math.log(F)/math.log(p) for (p, F) in rows if p >= 100)
print("max over 100<=p<=%d of log F*(p)/log p = %.4f" % (PMAX, mx))
print("max over p>=1000 of F*(p)/(p*log(p)^1.5) = %.3f" % max(F/(p*math.log(p)**1.5) for (p, F) in rows if p >= 1000))
for (p, F) in rows:
    assert F <= 5*(p-1)**2/4 or p == 3, p   # consistent with Lemma 1 (5(p-1)^2/4) of PROOF.md
print("F*(p) <= 5(p-1)^2/4 for all p = 3 mod 4 <= %d: OK" % PMAX)
print("box threshold Bbox(p) (two distinct values x^2+y^2, 0<=x,y<B, in every nonzero class):")
for p in [103, 211, 499, 1019, 2003, 4003]:
    Bb = bbox(p)
    print("p=%5d Bbox=%5d  Bbox/sqrt(p)=%.2f  log Bbox/log p=%.4f" % (p, Bb, Bb/math.sqrt(p), math.log(Bb)/math.log(p)))
