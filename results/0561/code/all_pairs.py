# List every pair (F1,F2) of star forests (up to swapping the two colours) whose
# conjectured value sum l_k is <= V.  Output lines: value n m
import sys, itertools
V = int(sys.argv[1])
def value(n, m):
    s, t = len(n), len(m)
    return sum(max(n[i-1] + m[k-i-1] - 1 for i in range(1, s+1) if 1 <= k-i <= t) for k in range(2, s+t+1))
def parts(total, maxpart):
    # all partitions (weakly decreasing lists) with sum <= total and parts <= maxpart, nonempty
    if total <= 0: return
    for a in range(min(total, maxpart), 0, -1):
        yield [a]
        for rest in parts(total - a, a):
            yield [a] + rest
# value(n,m) >= sum_i n_i: the diagonals k = i+1 (j=1) give l_{i+1} >= n_i + m_1 - 1 >= n_i.
# Likewise value >= sum_j m_j. So both are partitions of integers <= V.
out = set()
for n in parts(V, V):
    for m in parts(V, V):
        if tuple(m) > tuple(n): continue
        v = value(n, m)
        if v <= V: out.add((v, tuple(n), tuple(m)))
for v, n, m in sorted(out):
    print(v, ','.join(map(str, n)), ','.join(map(str, m)))
