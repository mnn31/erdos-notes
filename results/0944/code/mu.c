/* mu.c -- exact 3-colouring computations on small graphs (n <= 64).
 *
 * Input (stdin): one or more graphs, each given as
 *     n m
 *     u1 v1
 *     ...
 *     um vm
 * (0-based vertices, simple undirected), terminated by EOF.
 * For each graph, an optional mode word precedes it on its own line:
 *     CRIT   -> report: col3(G), all G-v 3-colourable?, all G-e 3-colourable?
 *     VCRIT  -> report: col3(G), all G-v 3-colourable?
 *     MU     -> report: mu(G) = min over c:V->{0,1,2} of #monochromatic edges
 *     ALL    -> CRIT + MU
 * Output: one line per graph.
 *
 * All searches are exhaustive (backtracking / branch and bound with an
 * admissible bound: the number of monochromatic edges among already-coloured
 * vertices never decreases), hence exact.
 *
 * Build: cc -O2 -o mu mu.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 64
typedef uint64_t u64;

static int n, m;
static int eu[4096], ev[4096];
static u64 adj[MAXN];

/* ---------- proper 3-colourability of G[active] with edge `skip` removed ---- */
static int order_[MAXN], ordn;
static int col[MAXN];
static int skipu = -1, skipv = -1;

static int adjacent(int a, int b) {
    if ((a == skipu && b == skipv) || (a == skipv && b == skipu)) return 0;
    return (adj[a] >> b) & 1ULL;
}

static void make_order(u64 active) {
    /* BFS-like order: repeatedly pick the active vertex with most neighbours
       among already ordered vertices (ties: larger degree). */
    u64 done = 0; ordn = 0;
    int cnt = __builtin_popcountll(active);
    while (ordn < cnt) {
        int best = -1, bs = -1, bd = -1;
        for (int v = 0; v < n; v++) if (((active >> v) & 1) && !((done >> v) & 1)) {
            int s = __builtin_popcountll(adj[v] & done);
            int d = __builtin_popcountll(adj[v] & active);
            if (s > bs || (s == bs && d > bd)) { best = v; bs = s; bd = d; }
        }
        order_[ordn++] = best; done |= 1ULL << best;
    }
}

static int bt(int i, int maxc) {
    if (i == ordn) return 1;
    int v = order_[i];
    for (int c = 0; c < 3 && c <= maxc; c++) {
        int ok = 1;
        for (int j = 0; j < i; j++) { int w = order_[j]; if (col[w] == c && adjacent(v, w)) { ok = 0; break; } }
        if (!ok) continue;
        col[v] = c;
        if (bt(i + 1, (c == maxc) ? maxc + 1 : maxc)) return 1;
    }
    return 0;
}

static int col3(u64 active, int su, int sv) {
    skipu = su; skipv = sv;
    make_order(active);
    int r = bt(0, 0); /* symmetry breaking: colours introduced in order */
    skipu = skipv = -1;
    return r;
}

/* ---------- mu: min number of monochromatic edges over all 3-colourings ---- */
static int best;
static void bb(int i, int maxc, int bad) {
    if (bad >= best) return;
    if (i == ordn) { best = bad; return; }
    int v = order_[i];
    for (int c = 0; c < 3 && c <= maxc; c++) {
        int add = 0;
        for (int j = 0; j < i; j++) { int w = order_[j]; if (col[w] == c && ((adj[v] >> w) & 1)) add++; }
        col[v] = c;
        bb(i + 1, (c == maxc) ? maxc + 1 : maxc, bad + add);
    }
}
static int mu(void) {
    u64 all = (n == 64) ? ~0ULL : ((1ULL << n) - 1);
    make_order(all);
    best = m + 1;
    bb(0, 0, 0);
    return best;
}

int main(void) {
    char mode[32];
    while (scanf("%31s", mode) == 1) {
        if (scanf("%d %d", &n, &m) != 2) return 1;
        if (n > MAXN || m > 4096) { fprintf(stderr, "too big\n"); return 1; }
        memset(adj, 0, sizeof adj);
        for (int i = 0; i < m; i++) {
            if (scanf("%d %d", &eu[i], &ev[i]) != 2) return 1;
            adj[eu[i]] |= 1ULL << ev[i]; adj[ev[i]] |= 1ULL << eu[i];
        }
        u64 all = (n == 64) ? ~0ULL : ((1ULL << n) - 1);
        int doc = !strcmp(mode, "CRIT") || !strcmp(mode, "ALL");
        int dov = doc || !strcmp(mode, "VCRIT");
        int dom = !strcmp(mode, "MU") || !strcmp(mode, "ALL");
        printf("n=%d m=%d", n, m);
        if (dov) {
            int c = col3(all, -1, -1);
            int vc = 1;
            for (int v = 0; v < n && vc; v++) if (!col3(all & ~(1ULL << v), -1, -1)) vc = 0;
            printf(" col3=%d allVdel3col=%d", c, vc);
            if (doc) {
                int ec = 1;
                for (int i = 0; i < m && ec; i++) if (!col3(all, eu[i], ev[i])) ec = 0;
                printf(" allEdel3col=%d", ec);
            }
        }
        if (dom) printf(" mu=%d", mu());
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
