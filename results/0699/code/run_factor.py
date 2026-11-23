# Factor the primitive parts Phi_d(b), b in {2,3}, d<=300 (with Aurifeuillian splits), in parallel.
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
from math import gcd
from sympy import cyclotomic_poly, Symbol
import fac
X = Symbol('x')
OUT = sys.argv[1]; BUDGET = float(sys.argv[2]); DMAX = int(sys.argv[3])

def pieces(b, d):
    v = int(cyclotomic_poly(d, X).subs(X, b))
    parts = [v]
    # Aurifeuillian: b=2, d=4*odd: 2^(d/2)+1 = L*M, L,M = 2^(2h+1) -+ 2^(h+1) + 1 with d/2 = 4h+2
    if b == 2 and d % 8 == 4 and d > 4:
        h = (d//2 - 2)//4
        L = 2**(2*h+1) - 2**(h+1) + 1
        g = gcd(v, L); parts = [x for x in (g, v//g) if x > 1]
    # b=3, d=6*odd: 3^(d/2)+1 = (3^(2h+1)+1)(3^(2h+1)+1 -+ 3^(h+1)) with d/2 = 3(2h+1)
    if b == 3 and d % 12 == 6 and d > 6:
        h = (d//6 - 1)//2
        L = 3**(2*h+1) + 1 - 3**(h+1)
        g = gcd(v, L); parts = [x for x in (g, v//g) if x > 1]
    return v, parts

def work(task):
    b, d, idx, N = task
    t = time.time()
    pr, co = fac.factor_full(N, BUDGET, extra=d)
    return dict(b=b, d=d, idx=idx, N=str(N), primes=pr, comps=[str(c) for c in co], sec=round(time.time()-t, 1))

if __name__ == '__main__':
    tasks = []
    for b in (2, 3):
        for d in range(1, DMAX+1):
            v, parts = pieces(b, d)
            for i, p in enumerate(parts): tasks.append((b, d, i, p))
    done = set()
    for sk in sys.argv[4:]:
        for line in open(sk):
            r = json.loads(line); done.add((r['b'], r['d'], r['idx']))
    tasks = [t for t in tasks if (t[0], t[1], t[2]) not in done]
    tasks.sort(key=lambda t: t[3].bit_length())
    with Pool(11) as pool, open(OUT, 'w') as f:
        for r in pool.imap_unordered(work, tasks):
            f.write(json.dumps(r) + '\n'); f.flush()
    print('done', len(tasks))
