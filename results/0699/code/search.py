# Near-miss search for Erdos 699 families: n=2^k (i=2) and n=3^m+1 (i=3).
# A near-miss = (n,i,j), i<j<=n/2, with no prime p>i dividing gcd(C(n,i),C(n,j)).
# Exact big-integer arithmetic throughout.
import sys, os, json, math, bisect, time
from math import log
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import divisors, isprime

def load_factors(path):
    F = {}
    for line in open(path):
        r = json.loads(line)
        F.setdefault((r['b'], r['d']), []).append(r)
    return F

def gather(fam, e, F, cyc):
    """Return n, i, list of (prime), list of (C, t) composites, missing-d list."""
    if fam == 2:
        n, i = 2**e, 2
        groups = [(1, [d for d in divisors(e)], 2)]            # n-1 = 2^k-1
    else:
        n, i = 3**e + 1, 3
        groups = [(0, [d for d in divisors(2*e) if e % d != 0], 3),  # n = 3^m+1
                  (2, [d for d in divisors(e)], 3)]                  # n-2 = 3^m-1
    primes, comps, missing = set(), [], []
    for t, ds, b in groups:
        prod = 1
        for d in ds:
            key = (b, d)
            if key not in F or math.prod(int(r['N']) for r in F[key]) != cyc_val(b, d):
                missing.append(d); prod = None; continue
            for r in F[key]:
                for p in r['primes']:
                    if p > i: primes.add(p)
                for c in r['comps']:
                    comps.append((int(c), t))
                if prod is not None: prod *= int(r['N'])
        if not missing:
            assert prod == (n - t) or (b == 3 and (n - t) % prod == 0), (fam, e, t)
    return n, i, sorted(primes), comps, missing

_CV = {}
def cyc_val(b, d):
    if (b, d) not in _CV:
        from sympy import cyclotomic_poly, Symbol
        _CV[(b, d)] = int(cyclotomic_poly(d, Symbol('x')).subs(Symbol('x'), b))
    return _CV[(b, d)]

def digits(n, p, cnt):
    out = []
    while n and len(out) < cnt: n, r = divmod(n, p); out.append(r)
    return out

def dominated(j, n, p):
    while j:
        if j % p > n % p: return False
        j //= p; n //= p
    return True

def search(n, i, primes, comps, maxlogN=38.0, maxout=3e6):
    lo, hi = i + 1, n // 2
    L = hi - lo + 1
    if L <= 0: return [], dict(status='OK', note='empty j range')
    # moduli: per prime p a prefix of base-p digits; composites with t=0 give j = 0 mod C
    dig = {p: digits(n, p, 64) for p in primes}
    tlen = {p: 1 for p in primes}
    logN = sum(log(dig[p][0] + 1) for p in primes)
    logQ = sum(log(p) for p in primes)
    zero_mods = [C for (C, t) in comps if t == 0]
    logQ += sum(log(C) for C in zero_mods)
    logL = log(L)
    # greedy digit extensions
    while logN + logL - logQ > log(2):
        best = None
        for p in primes:
            c = g = 0.0
            for s in range(1, 9):
                pos = tlen[p] + s - 1
                if pos >= len(dig[p]): break
                c += log(dig[p][pos] + 1); g += log(p)
                if dig[p][pos] + 1 > 4096: break
                r = c / g
                if best is None or r < best[0]: best = (r, p, s, c, g)
        if best is None or best[0] >= 1.0 or logN + best[3] > maxlogN * log(2): break
        _, p, s, c, g = best
        tlen[p] += s; logN += c; logQ += g
    mods = [(p**tlen[p], [ (p, k) for k in range(tlen[p]) ]) for p in primes]
    Q = 1
    for m, _ in mods: Q *= m
    for C in zero_mods:
        assert math.gcd(Q, C) == 1; Q *= C
    # items: (weight, number of choices)
    items = []
    for m, pos in mods:
        Mi = Q // m; E = Mi * pow(Mi, -1, m) % Q
        for (p, k) in pos:
            d = dig[p][k]
            if d > 0: items.append((p**k * E % Q, d + 1))
    Nlog2 = sum(math.log2(c) for _, c in items)
    expected_out = 2**Nlog2 * (L / Q if Q > L else 1) * (max(1, L // Q + 1))
    info = dict(n_primes=len(primes), n_zero_comps=len(zero_mods), log2N=round(Nlog2, 2),
                log2Q=round(Q.bit_length(), 1), log2L=L.bit_length(), est_out=float(expected_out))
    if Nlog2 > maxlogN + 0.5 or expected_out > maxout:
        info['status'] = 'TOO_MANY'; return None, info
    # MITM split balancing log choices
    items.sort(key=lambda x: -x[1])
    A, B, la, lb = [], [], 0.0, 0.0
    for it in items:
        if la <= lb: A.append(it); la += log(it[1])
        else: B.append(it); lb += log(it[1])
    def sums(its):
        S = [0]
        for w, c in its:
            S = [(x + k * w) % Q for x in S for k in range(c)]
        return S
    SA = sorted(sums(A)); SB = sums(B)
    cands = []
    if Q > hi:
        for y in SB:
            a, b = (lo - y) % Q, (hi - y) % Q
            rngs = [(a, b)] if a <= b else [(a, Q - 1), (0, b)]
            for (u, v) in rngs:
                for idx in range(bisect.bisect_left(SA, u), bisect.bisect_right(SA, v)):
                    cands.append((SA[idx] + y) % Q)
    else:
        for y in SB:
            for x in SA:
                r = (x + y) % Q
                t0 = r if r >= lo else r + ((lo - r + Q - 1) // Q) * Q
                for j in range(t0, hi + 1, Q): cands.append(j)
    info['n_cands'] = len(cands)
    out = []
    for j in cands:
        if not (lo <= j <= hi): continue
        if not all(dominated(j, n, p) for p in primes): continue
        ok, unres = True, False
        for (C, t) in comps:
            P = 1
            for s in range(t + 1): P *= (j - s)
            if pow(P, C.bit_length(), C) != 0: ok = False; break
            unres = True
        if ok: out.append((j, unres))
    info['status'] = 'OK'
    return out, info

def vp_fact(x, p):
    s = 0
    while x: x //= p; s += x
    return s

def second_check(n, i, j, primes):
    """Independent: Legendre's formula for v_p(C(n,j)) for every prime p>i of C(n,i);
    also v_i(C(n,j)) if i prime."""
    bad = [p for p in primes if vp_fact(n, p) - vp_fact(j, p) - vp_fact(n - j, p) > 0]
    vi = vp_fact(n, i) - vp_fact(j, i) - vp_fact(n - j, i)
    return bad, vi

def npieces(b, d):
    if b == 2 and d % 8 == 4 and d > 4: return 2
    if b == 3 and d % 12 == 6 and d > 6: return 2
    return 1
G = {}
def init(fam, fpath):
    G['fam'] = fam; G['F'] = load_factors(fpath)
    G['cyc'] = {(b, d): npieces(b, d) for b in (2, 3) for d in range(1, 301)}
def job(e):
    fam, F, cyc = G['fam'], G['F'], G['cyc']
    t = time.time()
    n, i, primes, comps, missing = gather(fam, e, F, cyc)
    if missing:
        return dict(fam=fam, e=e, status='MISSING_FACTOR_DATA', missing=missing)
    res, info = search(n, i, primes, comps)
    rec = dict(fam=fam, e=e, i=i, comps=[(str(C), t) for C, t in comps], **info, sec=round(time.time() - t, 2))
    if res is not None:
        rec['found'] = []
        for j, unres in res:
            bad, vi = second_check(n, i, j, primes)
            rec['found'].append(dict(j=str(j), unresolved_by_composite=unres,
                                     legendre_bad_primes=[str(p) for p in bad], v_i=vi))
        rec['primes_bpsw_ok'] = all(isprime(p) for p in primes)
    return rec

if __name__ == '__main__':
    fam = int(sys.argv[1]); e0, e1 = int(sys.argv[2]), int(sys.argv[3])
    fpath = sys.argv[4]; outp = sys.argv[5]
    from multiprocessing import Pool
    with Pool(int(os.environ.get('THREADS', '10')), initializer=init, initargs=(fam, fpath)) as pool, open(outp, 'w') as f:
        for rec in pool.imap(job, range(e0, e1 + 1)):
            f.write(json.dumps(rec) + '\n'); f.flush()
