"""Cross-check (not part of the proof): write class representatives with 40 digits, recheck the
edge lengths and unit-pair counts in mpmath at 40 digits, and compare sorted distance lists with
coordinate files produced by other runs (scout, t2/prove).  Usage:
  python3 -I crosscheck.py ../out/n20.json ../out <other coordinate files...>
"""
import sys
import json
import itertools
import mpmath as mp

mp.mp.dps = 40


def load_other(path):
    pts = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        pts.append((mp.mpf(parts[1]), mp.mpf(parts[2])))
    return pts


def dists(pts):
    return sorted(mp.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for a, b in itertools.combinations(pts, 2))


def main():
    J = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    edges = [tuple(e) for e in J["edges"]]
    reps = {}
    for k, cl in enumerate(J["classes"]):
        c = J["candidates"][cl[0]]
        pts = [(mp.mpf(x), mp.mpf(y)) for x, y in c["points_40digits"]]
        reps[k] = pts
        with open(f"{outdir}/n20_class{k}.txt", "w") as f:
            f.write(f"# n=20 congruence class {k}: candidate {cl[0]} (leaf {c['leaf']}); vertex x y (40 digits)\n")
            for i, (x, y) in enumerate(pts):
                f.write(f"{i} {mp.nstr(x, 40)} {mp.nstr(y, 40)}\n")
        err = max(abs(mp.sqrt((pts[a][0] - pts[b][0]) ** 2 + (pts[a][1] - pts[b][1]) ** 2) - 1) for a, b in edges)
        units = sum(1 for a, b in itertools.combinations(range(20), 2)
                    if abs(mp.sqrt((pts[a][0] - pts[b][0]) ** 2 + (pts[a][1] - pts[b][1]) ** 2) - 1) < mp.mpf(10) ** -30)
        near = min(abs(mp.sqrt((pts[a][0] - pts[b][0]) ** 2 + (pts[a][1] - pts[b][1]) ** 2) - 1)
                   for a, b in itertools.combinations(range(20), 2) if (a, b) not in set(edges))
        print(f"class {k}: max edge error {mp.nstr(err, 5)}, unit pairs (1e-30) {units}, "
              f"closest non-edge |d-1| {mp.nstr(near, 8)}")
    for path in sys.argv[3:]:
        other = dists(load_other(path))
        for k, pts in reps.items():
            mine = dists(pts)
            dev = max(abs(a - b) for a, b in zip(mine, other))
            print(f"{path} vs class {k}: max |sorted distance difference| = {mp.nstr(dev, 5)}")


if __name__ == "__main__":
    main()
