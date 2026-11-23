# Independent resolution of the one BUDGET case (n=30, A=Z_30\{0}, Alspach s_0-included form):
# Gordon's sequencing 1, -2, 3, -4, ... gives partial sums 0,1,-1,2,-2,...,15 (all distinct).
n = 30
order = [(k if k % 2 else -k) % n for k in range(1, n)]
assert sorted(order) == list(range(1, n))
s, seen = 0, {0}
for a in order:
    s = (s + a) % n
    assert s not in seen; seen.add(s)
print("n=30 Alspach t=29 resolved by Gordon ordering:", order, "sums distinct incl s0:", len(seen) == n)
