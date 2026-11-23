# family: abc absent because f = 0 (C1 dropped); f fixed => 1D check in T
import sys, time
sys.path.insert(0, '.')
import sympy as sp
from qpfaces import enumerate_faces, T
from cadcheck import check_face_1d
t0 = time.time()
faces, skipped, G, DD = enumerate_faces(['a','b','c','us','u','C2'], (), fval=0)
print(f"[f=0, no C1] faces with unique KKT point: {len(faces)}; skipped {len(skipped)}")
for A, why in skipped: print('  skipped', A, why)
allf = []; tot = 0
for A, xs in faces:
    n, fails = check_face_1d(A, xs, G, DD, None, sp.Integer(1))
    tot += n; allf += fails
    print(f"  face {A}: T-cells above T_b = {n}, failures = {len(fails)}")
print(f"[f=0] TOTAL cells {tot}, failures {len(allf)}, time {time.time()-t0:.1f}s")
for x in allf: print('  FAIL', x)
