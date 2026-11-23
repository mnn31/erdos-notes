# Driver: for star forests F1 (sizes n) and F2 (sizes m):
#  1. compute l_k and the conjectured value v = sum l_k;
#  2. check with arrow.c that the star union  U_k K_{1,l_k}  arrows (F1,F2)  (upper bound);
#  3. run arrow.c on every graph with v-1 edges and no isolated vertices (file graphs/g{v-1}.txt);
#     record a witness colouring for each graph;
#  4. re-verify every witness with the independent checker verify_witness.py.
# Usage: python3 -I run_instance.py n1,n2,.. m1,m2,.. graphsdir outdir
import sys, subprocess, os
here = os.path.dirname(os.path.abspath(__file__))
n = sorted(map(int, sys.argv[1].split(',')), reverse=True)
m = sorted(map(int, sys.argv[2].split(',')), reverse=True)
gd, od = sys.argv[3], sys.argv[4]
s, t = len(n), len(m)
L = [max(n[i-1] + m[k-i-1] - 1 for i in range(1, s+1) if 1 <= k-i <= t) for k in range(2, s+t+1)]
v = sum(L)
tag = f"{'.'.join(map(str,n))}_vs_{'.'.join(map(str,m))}"
print(f'F1={n} F2={m} l_k={L} value={v}', flush=True)
edges = []; base = 0
for l in L:
    edges += [(base, base+1+j) for j in range(l)]; base += l + 1
su = f'{od}/{tag}_starunion.txt'
with open(su, 'w') as f: f.write(' '.join(f'{a}-{b}' for a, b in edges) + '\n')
r = subprocess.run([f'{here}/arrow', sys.argv[1], sys.argv[2], su], capture_output=True, text=True)
print('star union arrows:', r.stdout.strip().splitlines()[-1], flush=True)
for e in [v-1]:
    wf = f'{od}/{tag}_e{e}_witnesses.tsv'
    r = subprocess.run([f'{here}/arrow', sys.argv[1], sys.argv[2], f'{gd}/g{e}.txt', wf], capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    print(f'e={e}:', out[-1], flush=True)
    for x in out[:-1][:20]: print('  ', x)
    r2 = subprocess.run([sys.executable, '-I', f'{here}/verify_witness.py', sys.argv[1], sys.argv[2], wf], capture_output=True, text=True)
    last = r2.stdout.strip().splitlines()[-1] if r2.stdout.strip() else 'VERIFIER FAILED: ' + r2.stderr.strip().replace(chr(10), ' | ')[-300:]
    print('independent witness check:', last, flush=True)
