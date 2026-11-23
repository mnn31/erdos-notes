# Independent double-precision cross-check of small_cases.py (not part of the proof).
import numpy as np, itertools
def dset(P, tol=1e-9):
    ds = np.sort([abs(a-b) for a, b in itertools.combinations(P, 2)]); out = [ds[0]]
    for d in ds[1:]:
        if d-out[-1] > tol: out.append(d)
    return np.array(out)
def ext(P, D, tol=1e-8):
    hits = []
    for i0, i1 in [(0, 1), (0, 2)]:   # use two different base pairs: results must agree
        v0, v1 = P[i0], P[i1]; h_ = []
        for r1, r2 in itertools.product(D, D):
            d = abs(v1-v0); a = (r1*r1-r2*r2+d*d)/(2*d); h2 = r1*r1-a*a
            if h2 < -1e-12: continue
            h = np.sqrt(max(h2, 0)); u = (v1-v0)/d
            for p in (v0+a*u+1j*h*u, v0+a*u-1j*h*u):
                if np.min(abs(P-p)) < 1e-7: continue
                if all(np.min(abs(abs(p-q)-D)) < tol for q in P) and all(abs(p-x) > 1e-7 for x in h_): h_.append(p)
        hits.append(sorted(h_, key=lambda z: (round(z.real, 6), round(z.imag, 6))))
    return hits
def turtle(ext_deg):
    P = [0j]; ang = 0
    for e in ext_deg: P.append(P[-1]+np.exp(1j*np.radians(ang))); ang += e
    return np.array(P[:-1])
s3 = np.sqrt(3)
cases = {"square": np.exp(2j*np.pi*np.arange(4)/4), "pentagon-1": np.exp(2j*np.pi*np.arange(1, 5)/5),
         "rhombus60": np.array([0, 1, 1.5+1j*s3/2, 0.5+1j*s3/2]), "kite": np.array([0, s3/2-0.5j, 1, s3/2+0.5j]),
         "hexagon": np.exp(2j*np.pi*np.arange(6)/6), "heptagon-1": np.exp(2j*np.pi*np.arange(1, 7)/7), "H3": turtle([90, 30]*3)}
for k, P in cases.items():
    D = dset(P); e = ext(P, D)
    print(k, "|D|=", len(D), "extensions (base v0v1):", np.round(e[0], 6), " (base v0v2):", np.round(e[1], 6))
