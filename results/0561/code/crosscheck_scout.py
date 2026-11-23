# Cross-check arrow.c against the scout's independent Python checker (attack/561/code/arrow.py)
# on every graph with e edges for several pairs: the sets of arrowing graphs must coincide.
# Usage: python3 -I crosscheck_scout.py scout_code_dir graphsdir
import sys, subprocess, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('scout_arrow', os.path.join(sys.argv[1], 'arrow.py'))
sa = importlib.util.module_from_spec(spec); spec.loader.exec_module(sa)
gd = sys.argv[2]
cases = [((2,), (2,), 3), ((2,), (2, 2), 6), ((2, 1), (2, 1), 6), ((2, 2), (2, 1), 8), ((3, 1), (2, 1), 8), ((2, 1, 1), (2, 1), 7), ((2, 2, 1), (2, 1, 1), 8), ((3,), (2, 2), 7), ((2, 2), (2, 2), 8)]
for n, m, e in cases:
    lines = [l for l in open(f'{gd}/g{e}.txt') if l.strip()]
    py = set()
    for l in lines:
        E = [tuple(map(int, t.split('-'))) for t in l.split()]
        if sa.arrows(E, list(n), list(m))[0]: py.add(l.strip())
    r = subprocess.run([f'{here}/arrow', ','.join(map(str, n)), ','.join(map(str, m)), f'{gd}/g{e}.txt'], capture_output=True, text=True)
    c = {x[len('ARROWS: '):].strip() for x in r.stdout.splitlines() if x.startswith('ARROWS')}
    print(n, m, f'e={e}', 'graphs', len(lines), 'arrowing(C)', len(c), 'arrowing(scout py)', len(py), 'AGREE' if c == py else 'DISAGREE', flush=True)
