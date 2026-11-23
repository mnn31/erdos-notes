"""Sanity tests for the pieces the computer proof relies on.
  (a) cardinality encodings (seqcounter, totalizer): "at least T of lits" is satisfiable
      under an assignment of lits iff at least T of them are true;
  (b) walk encoding in cegar.build_base: for random graphs that contain the fixed cycle
      and satisfy the lex order, base CNF + edge assumptions is SAT iff the graph has no
      odd cycle of length < g (checked by an independent BFS-based test);
  (c) the witness graph found for T=4 and the blow-up C7[2]: odd girth >= 7, exact D2 = 4.
Usage: python3 -I verify.py
"""
import sys, os, json, random, itertools
sys.path.append('~/.local/lib/python3.11/site-packages')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
import cegar

random.seed(12345)


def shortest_odd_cycle(N, edges):
    """Independent: shortest odd closed walk length via BFS on the bipartite double cover.
    The shortest odd closed walk is a shortest odd cycle (any odd closed walk contains an odd
    cycle no longer than it). Returns None if bipartite."""
    adj = [[] for _ in range(N)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    best = None
    for s in range(N):
        dist = {(s, 0): 0}
        q = [(s, 0)]; i = 0
        while i < len(q):
            x, p = q[i]; i += 1
            for y in adj[x]:
                st = (y, 1 - p)
                if st not in dist:
                    dist[st] = dist[(x, p)] + 1; q.append(st)
        if (s, 1) in dist:
            L = dist[(s, 1)]
            best = L if best is None else min(best, L)
    return best


def test_card():
    bad = 0
    for enc in (EncType.seqcounter, EncType.totalizer):
        for trial in range(300):
            n = random.randint(5, 45); T = 5
            pool = IDPool()
            lits = [pool.id(('x', i)) for i in range(n)]
            cnf = CardEnc.atleast(lits=lits, bound=T, vpool=pool, encoding=enc)
            k = random.randint(0, min(n, 9))
            ones = set(random.sample(range(n), k))
            assum = [lits[i] if i in ones else -lits[i] for i in range(n)]
            with Solver(name='minisat22', bootstrap_with=cnf.clauses) as s:
                r = s.solve(assumptions=assum)
            if r != (k >= T):
                bad += 1
    return bad


def test_walk_encoding(N=14, g=7, trials=400):
    pool = IDPool()
    E, cls = cegar.build_base(N, g, pool)
    s = Solver(name='minisat22', bootstrap_with=cls)
    bad = 0; counts = {True: 0, False: 0}
    for t in range(trials):
        p = random.choice([0.08, 0.12, 0.18, 0.25])
        edges = set((i, (i + 1) % g) if i < (i + 1) % g else ((i + 1) % g, i) for i in range(g))
        for u in range(N):
            for v in range(u + 1, N):
                if u >= g or v >= g:
                    if random.random() < p:
                        edges.add((u, v))
        # sort outside vertices by their adjacency vector to the cycle (lex order)
        vec = {x: tuple(1 if (min(x, j), max(x, j)) in edges else 0 for j in range(g)) for x in range(g, N)}
        order = sorted(range(g, N), key=lambda x: vec[x])
        relabel = {i: i for i in range(g)}
        for newx, oldx in zip(range(g, N), order):
            relabel[oldx] = newx
        edges = set((min(relabel[u], relabel[v]), max(relabel[u], relabel[v])) for u, v in edges)
        assum = [E[pq] if pq in edges else -E[pq] for pq in sorted(E)]
        r = s.solve(assumptions=assum)
        soc = shortest_odd_cycle(N, sorted(edges))
        truth = (soc is None) or soc >= g
        counts[truth] += 1
        if r != truth:
            bad += 1
    s.delete()
    return bad, counts


def main():
    out = {}
    out['card_mismatches'] = test_card()
    for g in (7, 9):
        b, c = test_walk_encoding(g=g)
        out[f'walk_g{g}_mismatches'] = b
        out[f'walk_g{g}_true_false_counts'] = {str(k): v for k, v in c.items()}
    # witness from the T=4 run
    here = os.path.dirname(os.path.abspath(__file__))
    line = open(os.path.join(here, '..', 'out', 'run_N14_T4.txt')).readline()
    wit = [tuple(e) for e in json.loads(line)['witness_edges']]
    out['witness_T4_edges'] = len(wit)
    out['witness_T4_shortest_odd_cycle'] = shortest_odd_cycle(14, wit)
    out['witness_T4_exact_D2'] = cegar.exact_D2(14, wit)
    # blow-up C7[2]: vertex (i, a) -> 2i + a, adjacent iff classes are consecutive mod 7
    bl = [(min(2 * i + a, 2 * ((i + 1) % 7) + b), max(2 * i + a, 2 * ((i + 1) % 7) + b))
          for i in range(7) for a in range(2) for b in range(2)]
    out['C7[2]_edges'] = len(set(bl))
    out['C7[2]_shortest_odd_cycle'] = shortest_odd_cycle(14, bl)
    out['C7[2]_exact_D2'] = cegar.exact_D2(14, bl)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
