#!/usr/bin/env python3
"""Write corrupted copies of the r=40, n=85 witness into out/negative/ (each must be rejected)."""
lines = open('out/witnesses/wit_r40.txt').read().split('\n')
i = [k for k, l in enumerate(lines) if l.startswith('W 85 ')][0]
hdr = lines[i]; cnt = int(hdr.split()[4]); masks = [int(x, 16) for x in lines[i + 1:i + 1 + cnt]]
sz = lambda m: bin(m).count('1')
def wr(name, h, ms):
    open('out/negative/' + name, 'w').write(h + '\n' + '\n'.join('%x' % m for m in ms) + '\n')
wr('ok_copy.txt', hdr, masks)                                  # unchanged: must pass
ms = masks[:]; a = [k for k in range(cnt) if sz(ms[k]) == 30]; ms[a[1]] = ms[a[0]]
wr('neg_dup.txt', hdr, ms)                                     # duplicated set
ms = masks[:]; low = [m for m in ms if sz(m) == 20][5]; k = [k for k in range(cnt) if sz(ms[k]) == 50][7]
x = low; bit = 0
while sz(x) < 50:
    if not (x >> bit) & 1: x |= 1 << bit
    bit += 1
assert x not in ms; ms[k] = x
wr('neg_comparable.txt', hdr, ms)                              # a 50-set containing a 20-set
ms = masks[:]; k = [k for k in range(cnt) if sz(ms[k]) == 10][0]; del ms[k]
wr('neg_mult.txt', hdr.replace(' 3240 ', ' 3239 '), ms)        # level 10 has only 39 sets
ms = masks[:]; ms[0] |= 1 << 90
wr('neg_range.txt', hdr, ms)                                   # element outside [85]
# core block (r=11): free set replaced by a 12-set containing a core 2-set -> must be rejected
L = open('out/witnesses/wit_r11.txt').read().split('\n')
k = [j for j, l in enumerate(L) if l.startswith('K ')][0]
q, r, s, cnt, nf = map(int, L[k].split()[1:6])
core = L[k + 1:k + 1 + cnt]; free = L[k + 1 + cnt:k + 1 + cnt + nf]
open('out/negative/core_ok.txt', 'w').write('\n'.join([L[k]] + core + free) + '\n')
two = [int(c, 16) for c in core if sz(int(c, 16)) == 2][0]
x = two; bit = 0
while sz(x) < s - 1:
    if not (x >> bit) & 1: x |= 1 << bit
    bit += 1
free2 = ['%x' % x] + free[1:]
open('out/negative/neg_core_free.txt', 'w').write('\n'.join([L[k]] + core + free2) + '\n')
