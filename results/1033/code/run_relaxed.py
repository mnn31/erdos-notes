import sys, time, pickle
sys.path.insert(0, '.')
import sympy as sp
from qpfaces import enumerate_faces, f, T
from cadcheck import check_face_2d
spec = sys.argv[1] if len(sys.argv) > 1 else 'relaxed'
SPECS = {
 'relaxed': dict(ineqs=['a','b','c','us','u','C1','C2'], forced=()),
 'abc_only': dict(ineqs=['a','b','c','us','u','C1'], forced=('u',)),     # ade absent: u=0
 'ade_only_b0': dict(ineqs=['a','b','c','us','u','C2'], forced=('b',)),  # abc absent via b=0
 'ade_only_c0': dict(ineqs=['a','b','c','us','u','C2'], forced=('c',)),  # abc absent via c=0
}
sp_ = SPECS[spec]
t0 = time.time()
faces, skipped, G, DD = enumerate_faces(sp_['ineqs'], sp_['forced'])
print(f"[{spec}] faces with unique KKT point: {len(faces)}; skipped: {len(skipped)}", flush=True)
for A, why in skipped: print('  skipped', A, why)
allfails = []; tot = 0
for A, xs in faces:
    n, fails, nT = check_face_2d(A, xs, G, DD, None, sp.Integer(1))
    tot += n
    print(f"  face {A}: T-cells above T_b = {nT}, 2D cells checked = {n}, failures = {len(fails)}", flush=True)
    allfails += fails
print(f"[{spec}] TOTAL cells {tot}, failures {len(allfails)}, time {time.time()-t0:.1f}s")
for x in allfails[:20]: print('  FAIL', x)
