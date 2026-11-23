# Exact (big-integer) evaluation of the recursion of Theorem A and exact checks of the
# inequalities of Lemmas 6-8; then a float (log-space) table of the ratio for large k.
import math, sys
from math import comb
LN2 = math.log(2)
I = 2 - 1/(2*LN2)
def phi(x): return (1+x)*math.log2(1+x) - (x*math.log2(x) if x > 0 else 0.0)

def table(N):
    s = {}; u = {}; v = {}; c = {}
    for i in range(N+1):
        for j in range(N+1):
            if i == 0 or j == 0:
                s[i,j] = u[i,j] = v[i,j] = c[i,j] = 1; continue
            s[i,j] = s[i-1,j] + s[i,j-1]
            u[i,j] = u[i-1,j]*(1+s[i,j-1]) + u[i,j-1]
            v[i,j] = v[i,j-1]*(1+s[i-1,j]) + v[i-1,j]
            c[i,j] = c[i-1,j] + c[i,j-1] + u[i-1,j]*v[i,j-1]
    return s, u, v, c

# ---- Part 1: exact checks on the full square 0<=i,j<=N
N = 45
s, u, v, c = table(N)
bad = 0
for i in range(N+1):
    for j in range(N+1):
        assert s[i,j] == comb(i+j, i)
        Phi_ = math.prod(1+comb(t+j, t) for t in range(1, i+1))
        Psi_ = math.prod(1+comb(i+t, t) for t in range(1, j+1))
        if not (u[i,j] <= 2**(i+j)*Phi_): bad += 1
        if not (v[i,j] <= 2**(i+j)*Psi_): bad += 1
        if not (c[i,j] <= 4**(i+j)*Phi_*Psi_): bad += 1
        if i >= 1 and j >= 1:
            lo = math.prod(comb(t+j-1, t) for t in range(1, i)) * math.prod(comb(i-1+t, t) for t in range(1, j))
            if not (c[i,j] >= u[i-1,j]*v[i,j-1] >= lo): bad += 1
            if not (u[i,j] >= math.prod(comb(t+j-1, t) for t in range(1, i+1))): bad += 1
# float check of the Q-form bounds of Theorem D: Q(i-1,j-1)-(i+j-2)log2(i+j) <= log2 c <= Q(i,j)+5(i+j)+2
def Phi(y):
    a = (1+y)**2/2*math.log2(1+y) - (1+y)**2/(4*LN2) + 1/(4*LN2)
    b = (y**2/2*math.log2(y) - y**2/(4*LN2)) if y > 0 else 0.0
    return a - b
def Q(a, b): return b*b*Phi(a/b) + a*a*Phi(b/a)
def lg(x):
    bl = x.bit_length(); return bl - 60 + math.log2(x >> (bl-60)) if bl > 900 else math.log2(x)
for i in range(1, N+1):
    for j in range(1, N+1):
        lc = lg(c[i,j])
        if not (lc <= Q(i, j) + 5*(i+j) + 2 + 1e-9): bad += 1
        if i >= 2 and j >= 2 and not (Q(i-1, j-1) - (i+j-2)*math.log2(i+j) <= lc + 1e-9): bad += 1
print(f"Part 1: exact inequality checks on 0<=i,j<={N}: violations = {bad}")
assert bad == 0
print("small values c(i,j) (i=a-2, j=b-2):", {(i+2, j+2): c[i,j] for i in range(1,4) for j in range(1,4)})

# ---- Part 2: exact diagonal with explicit Theorem B bounds (row-by-row, O(k) memory)
def diag_exact(K):
    # returns dict k -> (log2 c(k,k), log2 s(k,k)) for k<=K, computing rows i=0..K, j=0..K
    out = {}
    prev = None
    for i in range(K+1):
        row_s = [1]*(K+1); row_u = [1]*(K+1); row_v = [1]*(K+1); row_c = [1]*(K+1)
        if i > 0:
            ps, pu, pv, pc = prev
            for j in range(1, K+1):
                row_s[j] = ps[j] + row_s[j-1]
                row_u[j] = pu[j]*(1+row_s[j-1]) + row_u[j-1]
                row_v[j] = row_v[j-1]*(1+ps[j]) + pv[j]
                row_c[j] = pc[j] + row_c[j-1] + pu[j]*row_v[j-1]
        prev = (row_s, row_u, row_v, row_c)
        if i >= 1:
            def lg(x): 
                b = x.bit_length(); return b - 1 + math.log2(x / 2**(b-1)) if b < 1000 else b - 60 + math.log2(x >> (b-60))
            out[i] = (lg(row_c[i]), lg(row_s[i]))
    return out
K = int(sys.argv[1]) if len(sys.argv) > 1 else 160
d = diag_exact(K)
print(f"Part 2: exact diagonal up to k={K}; columns: k, m=k+2, log2 s, log2 c, ratio, lower bd, upper bd (Theorem B(iii))")
for k in sorted(d):
    lc, ls = d[k]
    lo = 2*I*(k-1)**2 - (2*k-2)*math.log2(2*k)   # Theorem B lower bound
    hi = 2*I*k*k + 10*k + 2                      # Theorem B upper bound
    assert lo <= lc + 1e-6 and lc <= hi + 1e-6, k
    if k in (1,2,3,5,10,20,40,80,120,160,200,300) or k == K:
        print(f"  k={k:4d} m={k+2:4d} log2s={ls:9.3f} log2c={lc:12.3f} ratio={lc/ls**2:.6f}  lo={lo:12.3f} hi={hi:12.3f}")
print("  all diagonal values satisfy lo <= log2 c(k,k) <= hi")

# ---- Part 3: float log-space diagonal for larger k (rounding only; not used in proofs)
def ladd(x, y):
    m = max(x, y); return m + math.log2(2**(x-m) + 2**(y-m))
def diag_float(K):
    ps = pu = pv = pc = [0.0]*(K+1); res = {}
    for i in range(1, K+1):
        rs = [0.0]*(K+1); ru = [0.0]*(K+1); rv = [0.0]*(K+1); rc = [0.0]*(K+1)
        for j in range(1, K+1):
            rs[j] = ladd(ps[j], rs[j-1])
            ru[j] = ladd(pu[j] + ladd(0.0, rs[j-1]), ru[j-1])
            rv[j] = ladd(rv[j-1] + ladd(0.0, ps[j]), pv[j])
            rc[j] = ladd(ladd(pc[j], rc[j-1]), pu[j] + rv[j-1])
        res[i] = (rc[i], rs[i]); ps, pu, pv, pc = rs, ru, rv, rc
    return res
KF = 2000
df = diag_float(KF)
print(f"Part 3: float diagonal; limit 1-1/(4ln2) = {1-1/(4*LN2):.6f}")
for k in (10, 40, 160, 320, 640, 1000, 1500, 2000):
    lc, ls = df[k]
    if k in d: assert abs(lc - d[k][0]) < 1e-6*max(1, lc), (k, lc, d[k][0])
    print(f"  k={k:5d} ratio={lc/ls**2:.6f}  log2c/(2k)^2={lc/(4*k*k):.6f}")
