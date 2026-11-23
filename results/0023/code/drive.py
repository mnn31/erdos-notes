import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
from bsat2 import feasible_case
from bsat import D_brute

def job(a):
    kind, N, t, L, dmin, tl, b2 = a
    short = [3] if kind == 'tri' else [3, 5]
    st, G, wt = feasible_case(N, t, L, short, dmin, tl, b2=b2)
    return dict(kind=kind, N=N, t=t, L=L, dmin=dmin, status=st, wall=round(wt, 2), graph=G,
                D_check=(D_brute(N, G) if G else None))

if __name__ == "__main__":
    kind, N0, N1, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    b2 = int(sys.argv[6]) if len(sys.argv) > 6 else None  # b(N0-2)
    tl = float(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] else None
    Lmin = 5 if kind == 'tri' else 7
    with Pool(10) as pool:
        for N in range(N0, N1 + 1):
            t = b + 1
            while True:
                dmin = 2 * (t - b)
                Ls = list(range(Lmin, N + 1, 2))
                T0 = time.time()
                res = pool.map(job, [(kind, N, t, L, dmin, tl, b2) for L in Ls]) if Ls else []
                for r in res:
                    print(json.dumps(r), flush=True)
                feas = [r for r in res if r['status'] in ('OPTIMAL', 'FEASIBLE')]
                unk = [r for r in res if r['status'] not in ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE')]
                print(json.dumps(dict(N=N, t=t, feasible=bool(feas), unknown=len(unk), secs=round(time.time()-T0, 1))), flush=True)
                if feas:
                    assert all(r['D_check'] >= t for r in feas)
                    t += 1
                    continue
                break
            if unk:
                print(json.dumps(dict(kind=kind, N=N, STOP="unknown case", lower=t-1)), flush=True)
                break
            b2, b = b, t - 1
            print(json.dumps(dict(kind=kind, N=N, b=b)), flush=True)
