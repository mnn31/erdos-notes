/* Independent checker for the delta = 4 computation (Erdos #776 variant).
 *
 *   check w FILE         verify every block of a witness file:
 *                          "W n r k cnt ..." : cnt sets (hex bitmasks) form an antichain of subsets of
 *                                              [n], pairwise distinct, every occurring size occurs >= r
 *                                              times, exactly k sizes occur, and k >= n-4.
 *                          "K q r s cnt nf"  : core: cnt sets form an antichain on [q], every level
 *                                              2..s has >= r members, no other level occurs; then nf
 *                                              == r further sets ("free sets"), pairwise distinct, each
 *                                              of size s-1, subsets of [q], none containing a core member.
 *   check i r N [CERT]   enumerate ALL 3-subsets M of {1..N-1} and confirm that for L = {1..N-1}\M the
 *                        prescribed-profile recurrence overflows (some m_i > C(N,i)); if CERT is given,
 *                        confirm it lists exactly the same (M, i, m_i, C(N,i)) lines in the same order.
 *   check s r NMAX       for every n = 5..NMAX decide by full enumeration whether some M passes;
 *                        print the list of n for which no M passes, and the largest such n.
 *
 * The Kruskal-Katona cascade is implemented here from scratch (unsigned __int128), independently of
 * the Python generator.  Sets are unsigned __int128 bitmasks (n <= 127).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
#define MAXB 128
static u128 B[MAXB + 1][MAXB + 1];

static void init_binom(void) {
    for (int a = 0; a <= MAXB; a++) {
        B[a][0] = 1;
        for (int b = 1; b <= MAXB; b++) B[a][b] = (a == 0) ? 0 : B[a - 1][b - 1] + B[a - 1][b];
    }
}
static u128 binom(int a, int b) {
    if (b < 0 || a < 0 || b > a) return 0;
    return B[a][b];
}

/* KK_k(m): minimum (k-1)-shadow of m k-sets, by the cascade m = sum_{j} C(a_j, j). */
static u128 kk(int k, u128 m) {
    u128 res = 0;
    int j = k, a = MAXB;
    /* the cascade needs a_k <= MAXB; refuse inputs with m >= C(MAXB,k) (never occur: the
       recurrence only calls kk on m <= C(n,k), n <= 127) */
    if (k >= 1 && k <= MAXB && m >= binom(MAXB, k)) { fprintf(stderr, "kk: m out of range\n"); exit(2); }
    while (m > 0) {
        if (j < 1) { fprintf(stderr, "kk: cascade failed\n"); exit(2); }
        /* largest a with C(a,j) <= m; a_j strictly decreasing so we can scan down from previous a */
        while (a >= j && binom(a, j) > m) a--;
        if (a < j) { fprintf(stderr, "kk: no a\n"); exit(2); }
        res += binom(a, j - 1);
        m -= binom(a, j);
        j--;
        a--; /* next a_{j-1} < a_j */
    }
    return res;
}

/* recurrence for occupied levels given as bitmask lev (bit i = level i). returns -1 if ok, else
 * overflow level i (first from the top) with m_i in *mi. */
static int recur(int n, u128 lev, int r, u128 *mi) {
    int T = -1;
    for (int i = 0; i < 128; i++) if ((lev >> i) & 1) T = i;
    if (T < 0 || n > 127) { fprintf(stderr, "recur: bad input\n"); exit(2); }
    u128 cur = 0;
    for (int i = T; i >= 0; i--) {
        u128 f = ((lev >> i) & 1) ? (u128)r : 0;
        cur = f + (i < T ? kk(i + 1, cur) : 0);
        if (cur > binom(n, i)) { *mi = cur; return i; }
    }
    return -1;
}

static void p128(FILE *o, u128 x) {
    char buf[64]; int k = 0;
    if (x == 0) { fputc('0', o); return; }
    while (x) { buf[k++] = '0' + (int)(x % 10); x /= 10; }
    while (k) fputc(buf[--k], o);
}

static int pc(u128 x) {
    return __builtin_popcountll((unsigned long long)x) + __builtin_popcountll((unsigned long long)(x >> 64));
}

static u128 parsehex(const char *s) {
    u128 x = 0;
    for (; *s; s++) {
        int d;
        if (*s >= '0' && *s <= '9') d = *s - '0';
        else if (*s >= 'a' && *s <= 'f') d = *s - 'a' + 10;
        else if (*s == '\n' || *s == '\r' || *s == ' ') break;
        else { fprintf(stderr, "bad hex\n"); exit(2); }
        if (x >> 124) { fprintf(stderr, "hex overflow\n"); exit(2); }
        x = (x << 4) | (u128)d;
    }
    return x;
}

static int cmp_pc(const void *a, const void *b) {
    u128 x = *(const u128 *)a, y = *(const u128 *)b;
    int px = pc(x), py = pc(y);
    if (px != py) return px - py;
    return (x < y) ? -1 : (x > y);
}

/* antichain + distinctness for an array; returns 1 if ok */
static int antichain(u128 *S, long cnt) {
    qsort(S, cnt, sizeof(u128), cmp_pc);
    for (long a = 0; a + 1 < cnt; a++)
        if (S[a] == S[a + 1]) return 0; /* duplicates adjacent after sort */
    for (long a = 0; a < cnt; a++) {
        int pa = pc(S[a]);
        for (long b = a + 1; b < cnt; b++) {
            if (pc(S[b]) == pa) continue; /* equal size distinct sets are incomparable */
            if ((S[a] & ~S[b]) == 0) return 0; /* S[a] subset of S[b] (pc(S[a]) < pc(S[b])) */
        }
    }
    return 1;
}

static char line[4096];

static int mode_w(const char *fn) {
    FILE *f = fopen(fn, "r");
    if (!f) { perror(fn); return 2; }
    long nblocks = 0; int bad = 0;
    while (fgets(line, sizeof line, f)) {
        if (line[0] == 'W') {
            int n, r, k; long cnt;
            if (sscanf(line, "W %d %d %d %ld", &n, &r, &k, &cnt) != 4) { fprintf(stderr, "bad W header\n"); return 2; }
            u128 *S = malloc(sizeof(u128) * cnt);
            int cntsz[MAXB + 1]; memset(cntsz, 0, sizeof cntsz);
            u128 full = (n >= 128) ? ~(u128)0 : (((u128)1 << n) - 1);
            for (long t = 0; t < cnt; t++) {
                if (!fgets(line, sizeof line, f)) { fprintf(stderr, "EOF\n"); return 2; }
                S[t] = parsehex(line);
                if (S[t] & ~full) { printf("FAIL W n=%d r=%d: set not in [n]\n", n, r); bad = 1; }
                cntsz[pc(S[t])]++;
            }
            int nsizes = 0, multok = 1;
            for (int s = 0; s <= n; s++) if (cntsz[s]) { nsizes++; if (cntsz[s] < r) multok = 0; }
            int ac = antichain(S, cnt);
            int ok = ac && multok && nsizes == k && k >= n - 4;
            printf("%s W n=%d r=%d sets=%ld sizes=%d antichain=%d mult>=r=%d\n", ok ? "OK" : "FAIL", n, r, cnt, nsizes, ac, multok);
            if (!ok) bad = 1;
            nblocks++;
            free(S);
        } else if (line[0] == 'K') {
            int q, r, s; long cnt, nf;
            if (sscanf(line, "K %d %d %d %ld %ld", &q, &r, &s, &cnt, &nf) != 5) { fprintf(stderr, "bad K header\n"); return 2; }
            u128 *S = malloc(sizeof(u128) * cnt), *G = malloc(sizeof(u128) * (nf > 0 ? nf : 1));
            int cntsz[MAXB + 1]; memset(cntsz, 0, sizeof cntsz);
            u128 full = (((u128)1 << q) - 1);
            int ok = 1;
            for (long t = 0; t < cnt; t++) {
                if (!fgets(line, sizeof line, f)) return 2;
                S[t] = parsehex(line);
                if (S[t] & ~full) ok = 0;
                cntsz[pc(S[t])]++;
            }
            for (int l = 0; l <= q; l++) {
                if (l >= 2 && l <= s) { if (cntsz[l] < r) ok = 0; }
                else if (cntsz[l]) ok = 0;
            }
            for (long t = 0; t < nf; t++) {
                if (!fgets(line, sizeof line, f)) return 2;
                G[t] = parsehex(line);
                if (G[t] & ~full) ok = 0;
                if (pc(G[t]) != s - 1) ok = 0;
                for (long u = 0; u < t; u++) if (G[u] == G[t]) ok = 0;
                for (long e = 0; e < cnt; e++) if ((S[e] & ~G[t]) == 0) ok = 0; /* core member inside G */
            }
            if (nf != r) ok = 0;
            int ac = antichain(S, cnt);
            ok = ok && ac;
            printf("%s K q=%d r=%d s=%d core_sets=%ld free=%ld antichain=%d\n", ok ? "OK" : "FAIL", q, r, s, cnt, nf, ac);
            if (!ok) bad = 1;
            nblocks++;
            free(S); free(G);
        }
    }
    fclose(f);
    printf("%s %s blocks=%ld\n", bad ? "FILE-FAIL" : "FILE-OK", fn, nblocks);
    return bad;
}

static int mode_i(int r, int N, const char *cert) {
    FILE *f = NULL;
    if (cert) {
        f = fopen(cert, "r");
        if (!f) { perror(cert); return 2; }
        /* skip comments, read header */
        int hr, hN; long hc;
        do { if (!fgets(line, sizeof line, f)) return 2; } while (line[0] == '#');
        if (sscanf(line, "C %d %d %ld", &hr, &hN, &hc) != 3 || hr != r || hN != N) { printf("FAIL cert header\n"); return 1; }
    }
    if (N < 5 || N > 127) return 2;
    u128 one = 1, all = ((one << N) - 1) & ~one; /* levels 1..N-1 */
    long count = 0, fails = 0, mismatch = 0;
    for (int a = 1; a <= N - 1; a++)
        for (int b = a + 1; b <= N - 1; b++)
            for (int c = b + 1; c <= N - 1; c++) {
                u128 lev = all & ~(one << a) & ~(one << b) & ~(one << c);
                u128 mi = 0;
                int i = recur(N, lev, r, &mi);
                count++;
                if (i < 0) { fails++; printf("FEASIBLE M={%d,%d,%d}\n", a, b, c); continue; }
                if (f) {
                    int A, Bb, C, I; char smi[128], sb[128];
                    if (!fgets(line, sizeof line, f) || sscanf(line, "%d %d %d %d %127s %127s", &A, &Bb, &C, &I, smi, sb) != 6) { mismatch++; continue; }
                    /* compare decimal strings */
                    char buf1[128], buf2[128];
                    FILE *m1 = fmemopen(buf1, sizeof buf1, "w"); p128(m1, mi); fputc(0, m1); fclose(m1);
                    FILE *m2 = fmemopen(buf2, sizeof buf2, "w"); p128(m2, binom(N, i)); fputc(0, m2); fclose(m2);
                    if (A != a || Bb != b || C != c || I != i || strcmp(smi, buf1) || strcmp(sb, buf2)) mismatch++;
                }
            }
    if (f) { if (fgets(line, sizeof line, f)) mismatch++; fclose(f); }
    int ok = (fails == 0) && (mismatch == 0) && count == (long)((N - 1) * (N - 2) * (N - 3) / 6);
    printf("%s INFEAS r=%d N=%d triples=%ld feasible=%ld cert_mismatch=%ld\n", ok ? "OK" : "FAIL", r, N, count, fails, mismatch);
    return !ok;
}

static int mode_s(int r, int nmax) {
    if (nmax > 127) return 2;
    int last = 0;
    printf("r=%d failing n:", r);
    for (int n = 5; n <= nmax; n++) {
        u128 one = 1, all = ((one << n) - 1) & ~one;
        int feas = 0;
        for (int a = 1; a <= n - 1 && !feas; a++)
            for (int b = a + 1; b <= n - 1 && !feas; b++)
                for (int c = b + 1; c <= n - 1 && !feas; c++) {
                    u128 mi;
                    if (recur(n, all & ~(one << a) & ~(one << b) & ~(one << c), r, &mi) < 0) feas = 1;
                }
        if (!feas) { printf(" %d", n); last = n; }
    }
    printf("  | largest failing n <= %d: %d\n", nmax, last);
    return 0;
}

int main(int argc, char **argv) {
    init_binom();
    if (argc >= 3 && !strcmp(argv[1], "w")) return mode_w(argv[2]);
    if (argc >= 4 && !strcmp(argv[1], "i")) return mode_i(atoi(argv[2]), atoi(argv[3]), argc >= 5 ? argv[4] : NULL);
    if (argc >= 4 && !strcmp(argv[1], "s")) return mode_s(atoi(argv[2]), atoi(argv[3]));
    if (argc >= 4 && !strcmp(argv[1], "k")) { /* print KK_k(m) for testing */
        u128 m = 0; for (const char *c = argv[3]; *c; c++) { if (*c < '0' || *c > '9') return 2; m = m * 10 + (u128)(*c - '0'); }
        p128(stdout, kk(atoi(argv[2]), m)); printf("\n"); return 0;
    }
    fprintf(stderr, "usage: check w FILE | check i r N [CERT] | check s r NMAX | check k k m\n");
    return 2;
}
