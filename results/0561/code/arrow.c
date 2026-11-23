/* arrow.c : decide H -> (F1,F2) for star forests F1, F2 by trying all 2^e red/blue colourings.
   Usage: arrow "n1,n2,..." "m1,m2,..." graphfile [witnessfile]
   graphfile: one graph per line, edges "u-v" separated by spaces, vertices 0..31.
   For every graph prints nothing unless it arrows; writes for each non-arrowing graph a
   witness colouring (bitmask: bit i set = edge i red) to witnessfile.
   Summary line at end: total graphs, number arrowing.
   Containment of a star forest with sizes s_1>=...>=s_k in a graph R (bitmask adjacency):
   exhaustive backtracking: pick a centre c (unused) and a set of s_idx leaves among the
   unused neighbours of c, recurse. Complete: every embedding is found by this search, after
   renumbering stars of equal size so that their centres increase. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int nv;
static int sizes1[16], k1, sum1, sizes2[16], k2, sum2;

static int has_forest(const uint32_t *adj, const int *sz, int k, int idx, uint32_t used, int cmin) {
    if (idx == k) return 1;
    int need = sz[idx];
    /* symmetry breaking: stars of equal size are interchangeable, so their centres may be
       taken in increasing order (cmin = previous centre + 1 when sz[idx] == sz[idx-1]) */
    for (int c = cmin; c < nv; c++) {
        if (used >> c & 1) continue;
        uint32_t av = adj[c] & ~used & ~(1u << c);
        if (__builtin_popcount(av) < need) continue;
        /* enumerate subsets of av with exactly `need` bits */
        int L[32], nl = 0;
        for (int v = 0; v < nv; v++) if (av >> v & 1) L[nl++] = v;
        int ix[32];
        for (int i = 0; i < need; i++) ix[i] = i;
        while (1) {
            uint32_t s = 1u << c;
            for (int i = 0; i < need; i++) s |= 1u << L[ix[i]];
            if (has_forest(adj, sz, k, idx + 1, used | s, (idx + 1 < k && sz[idx + 1] == need) ? c + 1 : 0)) return 1;
            int i = need - 1;
            while (i >= 0 && ix[i] == nl - need + i) i--;
            if (i < 0) break;
            ix[i]++;
            for (int j = i + 1; j < need; j++) ix[j] = ix[j - 1] + 1;
        }
    }
    return 0;
}

static int parse_sizes(const char *s, int *a) {
    int k = 0; const char *p = s;
    while (*p) { a[k++] = atoi(p); while (*p && *p != ',') p++; if (*p) p++; }
    /* sort descending */
    for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) if (a[j] > a[i]) { int t = a[i]; a[i] = a[j]; a[j] = t; }
    return k;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
    k1 = parse_sizes(argv[1], sizes1); k2 = parse_sizes(argv[2], sizes2);
    sum1 = sum2 = 0;
    for (int i = 0; i < k1; i++) sum1 += sizes1[i];
    for (int i = 0; i < k2; i++) sum2 += sizes2[i];
    FILE *f = fopen(argv[3], "r");
    FILE *w = argc > 4 ? fopen(argv[4], "w") : NULL;
    char line[4096];
    long total = 0, arrowing = 0;
    while (fgets(line, sizeof line, f)) {
        int eu[64], ev[64], e = 0; nv = 0;
        char *p = line;
        while (*p) {
            while (*p == ' ' || *p == '\n') p++;
            if (!*p) break;
            int a = strtol(p, &p, 10); p++; int b = strtol(p, &p, 10);
            eu[e] = a; ev[e] = b; e++;
            if (a + 1 > nv) nv = a + 1;
            if (b + 1 > nv) nv = b + 1;
        }
        if (e == 0) continue;
        total++;
        long good = -1;
        for (long mask = 0; mask < (1L << e); mask++) {
            uint32_t R[32] = {0}, B[32] = {0};
            int nr = __builtin_popcountl(mask);
            for (int i = 0; i < e; i++) {
                if (mask >> i & 1) { R[eu[i]] |= 1u << ev[i]; R[ev[i]] |= 1u << eu[i]; }
                else { B[eu[i]] |= 1u << ev[i]; B[ev[i]] |= 1u << eu[i]; }
            }
            int red = (nr >= sum1) && has_forest(R, sizes1, k1, 0, 0, 0);
            if (red) continue;
            int blue = (e - nr >= sum2) && has_forest(B, sizes2, k2, 0, 0, 0);
            if (blue) continue;
            good = mask; break;
        }
        if (good < 0) { arrowing++; printf("ARROWS: %s", line); }
        if (w) fprintf(w, "%ld\t%s", good, line);
    }
    printf("total %ld arrowing %ld\n", total, arrowing);
    return 0;
}
