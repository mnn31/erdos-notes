# Second factoring pass with larger budget on pieces still blocking a decision.
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
import fac
BUDGET = float(sys.argv[2])
def work(t):
    b, d, idx, N = t
    pr, co = fac.factor_full(N, BUDGET, extra=d)
    return dict(b=b, d=d, idx=idx, N=str(N), primes=pr, comps=[str(c) for c in co], pass3=True)
if __name__ == '__main__':
    tasks = [tuple(x[:3]) + (int(x[3]),) for x in json.load(open(sys.argv[1]))]
    with Pool(11) as pool, open(sys.argv[3], 'w') as f:
        for r in pool.imap_unordered(work, tasks):
            f.write(json.dumps(r) + '\n'); f.flush()
