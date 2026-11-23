# Value-14 pairs kept for the (time-capped) value-14 sweep: both forests have >= 3 stars and
# neither is a matching. This is the scout's frontier filter applied before any claim is used.
# It drops pairs with a side of <= 2 stars (DJKR 2.3 and You 2026) and matching sides.
import sys
for line in open(sys.argv[1]):
    v, n, m = line.split()
    n = list(map(int, n.split(','))); m = list(map(int, m.split(',')))
    if int(v) == 14 and len(n) >= 3 and len(m) >= 3 and max(n) >= 2 and max(m) >= 2:
        print(line, end='')
