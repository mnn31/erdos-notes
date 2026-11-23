# Combine out/lshift_upto_1e14.txt (all t <= 1e14) with the 10 contiguous segment runs covering
# [1e14+1, 1e16] (out/seg/*.out) into the least n-shift t_n for each n, or a lower bound.
# Logic: within one segment, the reported t for n is the least t in that segment with L(t) >= n
# (lshift reports, for every n, the first t of the segment that is an n-shift; an n not reported
# but below a reported n' inherits the earlier report). t_n = min over all pieces.
# run: python3 -I code/combine_segments.py
import re, glob, os
D = os.path.dirname(os.path.abspath(__file__)) + "/../out"
pieces = []  # (lo, hi, {n: t}, nfail) ; nfail: first n with "none" (lower bound up to hi)
def parse(path, lo, hi):
    best = {}; nfail = None
    for line in open(path):
        m = re.match(r"t_(\d+) = (\d+)", line)
        if m: best[int(m.group(1))] = int(m.group(2))
        m = re.match(r"t_(\d+) : none", line)
        if m: nfail = int(m.group(1))
    return (lo, hi, best, nfail)
pieces.append(parse(D + "/lshift_upto_1e14.txt", 1, 10**14))
for f in glob.glob(D + "/seg/seg_49_*.out"):
    lo = int(re.search(r"seg_49_(\d+)\.out", f).group(1))
    pieces.append(parse(f, lo, None))
pieces.sort(key=lambda p: p[0])
for i, p in enumerate(pieces):
    if p[1] is None:
        hi = pieces[i+1][0] - 1 if i + 1 < len(pieces) else 10**16
        pieces[i] = (p[0], hi, p[2], p[3])
for i in range(len(pieces) - 1): assert pieces[i][1] + 1 == pieces[i+1][0], "gap"
print("coverage: t in [%d, %d], contiguous" % (pieces[0][0], pieces[-1][1]))
def first_in_piece(p, n):
    # least t in piece with L(t) >= n, or None. Reports with key >= n are candidates; smallest key >= n wins
    ks = [k for k in p[2] if k >= n]
    if ks: return p[2][min(ks)]
    return None
for n in range(1, 54):
    ts = [first_in_piece(p, n) for p in pieces]
    ts = [t for t in ts if t is not None]
    if ts: print("t_%d = %d" % (n, min(ts)))
    else:
        # every piece must have certified 'none' for some n0 <= n after its last report
        ok = all(p[3] is not None and p[3] <= n for p in pieces)
        print("t_%d > %d (%s)" % (n, pieces[-1][1], "certified" if ok else "NOT certified")); break
