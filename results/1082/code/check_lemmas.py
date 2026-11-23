# Numerical sanity checks (double precision; NOT part of the proof) of Lemmas 2-5 in WRITEUP.md.
import numpy as np, itertools
rng = np.random.default_rng(0)
def poly(N, drop=None): return np.array([np.exp(2j*np.pi*k/N) for k in range(N) if k != drop])
def dset(P, tol=1e-9):
    ds = np.sort([abs(a-b) for a, b in itertools.combinations(P, 2)]); out = [ds[0]]
    for d in ds[1:]:
        if d-out[-1] > tol: out.append(d)
    return np.array(out)
def ndist(p, P, tol=1e-9): return len(dset(np.concatenate([[p], P]), tol)) if False else len(np.unique(np.round(abs(P-p)/tol).astype(np.int64)))
# Lemma 2 (count of distinct distances from p != 0 to regular N-gon): orbit count formula
bad = 0
for N in range(3, 41):
    P = poly(N)
    for trial in range(200):
        r = rng.uniform(0.05, 3); s = rng.integers(0, 2*N)
        th = np.pi*s/N if trial % 2 == 0 else rng.uniform(0, 2*np.pi)
        p = r*np.exp(1j*th)
        cnt = len(np.unique(np.round(abs(P-p), 8)))
        if trial % 2 == 0:
            fix = (1 if N % 2 else (2 if s % 2 == 0 else 0))
            pred = (N+fix)//2
        else: pred = N
        if cnt != pred: bad += 1
print("Lemma 2 orbit-count mismatches:", bad)
def extensions(P, D, tol=1e-8):
    v0, v1 = P[0], P[1]; hits = []
    for r1, r2 in itertools.product(D, D):
        d = abs(v1-v0); a = (r1*r1-r2*r2+d*d)/(2*d); h2 = r1*r1-a*a
        if h2 < -1e-12: continue
        h = np.sqrt(max(h2, 0)); u = (v1-v0)/d
        for p in (v0+a*u+1j*h*u, v0+a*u-1j*h*u):
            if np.min(abs(P-p)) < 1e-7: continue
            if all(np.min(abs(abs(p-q)-D)) < tol for q in P):
                if all(abs(p-x) > 1e-7 for x in hits): hits.append(p)
    return hits
for N in range(3, 61):
    P = poly(N); D = dset(P); e = extensions(P, D)
    print("regular %2d-gon: |D|=%2d one-point extensions: %s" % (N, len(D), [np.round(x, 6) for x in e]))
for M in range(5, 62, 2):
    P = poly(M, drop=0); D = dset(P); e = extensions(P, D)
    print("regular %2d-gon minus vertex: |D|=%2d one-point extensions: %s" % (M, len(D), [np.round(x, 6) for x in e]))
