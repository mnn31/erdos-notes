# Independent brute force (no shared code with g475.c): for small n, all subsets of Z_n\{0},
# all permutations. Prints per t: #orbits under unit multiplication, #sets with no valid
# ordering in mode 0 (s1..st distinct), mode 1 (s0..st distinct, nonzero-sum sets only),
# and #zero-sum sets (which mode 3 must report as exhausted).
import sys, itertools, math
n = int(sys.argv[1])
units = [u for u in range(1, n) if math.gcd(u, n) == 1]
def ok(order, incl0):
    seen = {0} if incl0 else set(); s = 0
    for a in order:
        s = (s + a) % n
        if s in seen: return False
        seen.add(s)
    return True
def exists(A, incl0):
    return any(ok(p, incl0) for p in itertools.permutations(A))
for t in range(1, n):
    orbits = set(); f0 = f1 = zs = 0; nz = 0
    for A in itertools.combinations(range(1, n), t):
        orbits.add(min(tuple(sorted(u * a % n for a in A)) for u in units))
        if not exists(A, False): f0 += 1
        if sum(A) % n == 0: zs += 1
        else:
            nz += 1
            if not exists(A, True): f1 += 1
    print(n, t, len(orbits), f0, nz, f1, zs)
