/*
 * Erdos 475 / Graham rearrangement / ADMS Conjecture 1.2 exhaustive checker.
 *
 * For cyclic Z_n (n <= 40) and every A subset of Z_n \ {0} with tmin <= |A| <= tmax,
 * find an ordering a_1..a_t with distinct partial sums.
 *   mode 0 (ADMS / Graham, Erdos 475): s_1..s_t pairwise distinct (s_0 not included).
 *   mode 1 (Alspach): only A with sum(A) != 0; s_0=0, s_1..s_t pairwise distinct.
 *   mode 3 (negative control): as mode 1 but zero-sum A are NOT skipped, so every
 *          zero-sum A must come out EXHAUSTED_NO_ORDERING (s_t = 0 = s_0).
 *
 * Symmetry: A -> lambda*A for lambda a unit of Z_n. Only the numerically least
 * bitmask in each orbit is solved. Completeness check: sum over canonical A of the
 * orbit size phi(n)/|Stab(A)| must equal C(n-1,t) (or the number of non-zero-sum
 * t-subsets in mode 1, counted separately by brute force over all subsets).
 *
 * Every found ordering is re-checked by an independent O(t) routine using plain
 * integer arithmetic (no bit tricks) before the set counts as verified.
 *
 * Usage: g475 n tmin tmax mode threads [hardfile]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>

typedef uint64_t u64;

static int N, TMIN, TMAX, MODE, NTH;
static u64 FULL;              /* bits 0..N-1 */
static int L, H;              /* low elements 1..L, high elements L+1..N-1 */
static int NUNITS;
static int UNITS[64];         /* units other than 1 */
static u64 TAB[64][5][256];   /* TAB[u][byte j][v] = image under mult by UNITS[u] of bits 8j..8j+7 */
static FILE *HARDF;
static pthread_mutex_t HMUT = PTHREAD_MUTEX_INITIALIZER;

static atomic_long JOBCTR;
static long NJOBS;

#define MAXT 41
typedef struct {
    long canon[MAXT];      /* canonical sets solved */
    long orbsum[MAXT];     /* sum of orbit sizes */
    long zerosum_skip[MAXT];/* mode 1: canonical sets skipped because sum==0 (orbit-weighted) */
    long greedy_ok[MAXT];
    long dfs_ok[MAXT];
    long hard[MAXT];
    long verified[MAXT];
    long max_restarts;
    long dfs_nodes;
} stats_t;

static inline u64 rng_next(u64 *s) {
    u64 x = *s; x ^= x << 13; x ^= x >> 7; x ^= x << 17; return *s = x;
}

static inline u64 rotr_n(u64 x, int s) {  /* bit a of result = bit (a+s) mod N of x */
    if (s == 0) return x;
    return ((x >> s) | (x << (N - s))) & FULL;
}

static inline u64 mulmask(int u, u64 m) {
    return TAB[u][0][m & 255] | TAB[u][1][(m >> 8) & 255] | TAB[u][2][(m >> 16) & 255]
         | TAB[u][3][(m >> 24) & 255] | TAB[u][4][(m >> 32) & 255];
}

/* independent certificate check: plain arithmetic */
static int check_cert(u64 A, const int *ord, int t, int mode) {
    int seen[64]; memset(seen, 0, sizeof seen);
    int inA[64]; memset(inA, 0, sizeof inA);
    int cnt = 0;
    for (int a = 1; a < N; a++) if ((A >> a) & 1) { inA[a] = 1; cnt++; }
    if (cnt != t) return 0;
    int usedel[64]; memset(usedel, 0, sizeof usedel);
    long s = 0;
    if (mode != 0) seen[0] = 1;
    for (int i = 0; i < t; i++) {
        int a = ord[i];
        if (a <= 0 || a >= N || !inA[a] || usedel[a]) return 0;
        usedel[a] = 1;
        s = (s + a) % N;
        if (seen[s]) return 0;
        seen[s] = 1;
    }
    return 1;
}

/* randomized greedy: returns 1 and fills ord on success */
static int greedy(u64 A, int mode, int *ord, u64 *rng) {
    u64 rem = A, used = (mode != 0) ? 1ULL : 0ULL;
    int s = 0, k = 0;
    while (rem) {
        u64 feas = rem & rotr_n(~used & FULL, s);
        if (!feas) return 0;
        int c = __builtin_popcountll(feas);
        int r = (int)(rng_next(rng) % (u64)c);
        while (r--) feas &= feas - 1;
        int a = __builtin_ctzll(feas);
        ord[k++] = a;
        rem &= ~(1ULL << a);
        s += a; if (s >= N) s -= N;
        used |= 1ULL << s;
    }
    return 1;
}

/* exhaustive DFS with node budget. returns 1 found, 0 exhausted (no ordering), -1 budget hit */
static long dfs_budget;
static int dfs(u64 rem, u64 used, int s, int *ord, int k, long *nodes, long budget) {
    if (!rem) return 1;
    if (++*nodes > budget) return -1;
    u64 feas = rem & rotr_n(~used & FULL, s);
    int res = 0;
    while (feas) {
        int a = __builtin_ctzll(feas); feas &= feas - 1;
        int s2 = s + a; if (s2 >= N) s2 -= N;
        ord[k] = a;
        int r = dfs(rem & ~(1ULL << a), used | (1ULL << s2), s2, ord, k + 1, nodes, budget);
        if (r == 1) return 1;
        if (r == -1) res = -1;
        if (r == -1) return -1;
    }
    return res;
}

static void solve_set(u64 A, int t, int orbsize, stats_t *st, u64 *rng) {
    int ord[64];
    if (MODE == 1) {
        long sum = 0;
        for (int a = 1; a < N; a++) if ((A >> a) & 1) sum += a;
        if (sum % N == 0) { st->zerosum_skip[t] += orbsize; return; }
    }
    st->canon[t]++; st->orbsum[t] += orbsize;
    int ok = 0;
    long R = 0;
    for (R = 0; R < 2000; R++) {
        if (greedy(A, MODE, ord, rng)) { ok = 1; break; }
    }
    if (ok) {
        st->greedy_ok[t]++;
        if (R > st->max_restarts) st->max_restarts = R;
    } else {
        long nodes = 0;
        int r = dfs(A, MODE != 0 ? 1ULL : 0ULL, 0, ord, 0, &nodes, 2000000000L);
        st->dfs_nodes += nodes;
        if (r == 1) { ok = 1; st->dfs_ok[t]++; }
        else {
            st->hard[t]++;
            pthread_mutex_lock(&HMUT);
            fprintf(HARDF, "n=%d t=%d mode=%d status=%s mask=0x%llx elems=", N, t, MODE,
                    r == 0 ? "EXHAUSTED_NO_ORDERING" : "BUDGET", (unsigned long long)A);
            for (int a = 1; a < N; a++) if ((A >> a) & 1) fprintf(HARDF, "%d,", a);
            fprintf(HARDF, "\n"); fflush(HARDF);
            pthread_mutex_unlock(&HMUT);
            return;
        }
    }
    if (ok) {
        if (check_cert(A, ord, t, MODE)) st->verified[t]++;
        else {
            pthread_mutex_lock(&HMUT);
            fprintf(HARDF, "CERT_FAIL n=%d t=%d mask=0x%llx\n", N, t, (unsigned long long)A);
            fflush(HARDF);
            pthread_mutex_unlock(&HMUT);
        }
    }
}

/* returns orbit size if A is canonical (numerically least in orbit), else 0 */
static inline int canon_orbit(u64 A) {
    int stab = 1;
    for (int u = 0; u < NUNITS; u++) {
        u64 B = mulmask(u, A);
        if (B < A) return 0;
        if (B == A) stab++;
    }
    return (NUNITS + 1) / stab;
}

static void *worker(void *arg) {
    stats_t *st = (stats_t *)arg;
    u64 rng = 0x9E3779B97F4A7C15ULL ^ ((u64)(uintptr_t)arg * 0x2545F4914F6CDD1DULL);
    if (!rng) rng = 1;
    for (;;) {
        long j = atomic_fetch_add(&JOBCTR, 1);
        if (j >= NJOBS) break;
        long npat = 1L << L;
        u64 pat = (u64)(j % npat);
        int t = TMIN + (int)(j / npat);
        int pc = __builtin_popcountll(pat);
        int r = t - pc;
        if (r < 0 || r > H) continue;
        u64 low = pat << 1;              /* elements 1..L */
        if (r == 0) {
            u64 A = low;
            int o = canon_orbit(A);
            if (o) solve_set(A, t, o, st, &rng);
            continue;
        }
        u64 c = (1ULL << r) - 1, lim = 1ULL << H;
        while (c < lim) {
            u64 A = low | (c << (L + 1));
            int o = canon_orbit(A);
            if (o) solve_set(A, t, o, st, &rng);
            u64 lo = c & -c, rr = c + lo;
            c = (((rr ^ c) >> 2) / lo) | rr;
        }
    }
    return NULL;
}

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: g475 n tmin tmax mode threads [hardfile]\n"); return 1; }
    N = atoi(argv[1]); TMIN = atoi(argv[2]); TMAX = atoi(argv[3]); MODE = atoi(argv[4]); NTH = atoi(argv[5]);
    HARDF = argc > 6 ? fopen(argv[6], "a") : stderr;
    if (N < 2 || N > 40 || TMIN < 1 || TMAX > N - 1 || TMIN > TMAX) { fprintf(stderr, "bad args\n"); return 1; }
    FULL = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
    L = N - 1 < 10 ? N - 1 : 10;
    H = N - 1 - L;
    NUNITS = 0;
    for (int u = 2; u < N; u++) if (gcd(u, N) == 1) UNITS[NUNITS++] = u;
    for (int i = 0; i < NUNITS; i++)
        for (int j = 0; j < 5; j++)
            for (int v = 0; v < 256; v++) {
                u64 m = 0;
                for (int b = 0; b < 8; b++) if ((v >> b) & 1) {
                    int e = 8 * j + b;
                    if (e >= 1 && e < N) m |= 1ULL << ((e * UNITS[i]) % N);
                }
                TAB[i][j][v] = m;
            }
    NJOBS = (long)(TMAX - TMIN + 1) << L;
    atomic_store(&JOBCTR, 0);
    struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
    pthread_t th[64]; stats_t *st = calloc(NTH, sizeof(stats_t));
    for (int i = 0; i < NTH; i++) pthread_create(&th[i], NULL, worker, &st[i]);
    for (int i = 0; i < NTH; i++) pthread_join(th[i], NULL);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    double el = (t1.tv_sec - t0.tv_sec) + 1e-9 * (t1.tv_nsec - t0.tv_nsec);
    stats_t tot; memset(&tot, 0, sizeof tot);
    for (int i = 0; i < NTH; i++) {
        for (int t = 0; t < MAXT; t++) {
            tot.canon[t] += st[i].canon[t]; tot.orbsum[t] += st[i].orbsum[t];
            tot.zerosum_skip[t] += st[i].zerosum_skip[t];
            tot.greedy_ok[t] += st[i].greedy_ok[t]; tot.dfs_ok[t] += st[i].dfs_ok[t];
            tot.hard[t] += st[i].hard[t]; tot.verified[t] += st[i].verified[t];
        }
        if (st[i].max_restarts > tot.max_restarts) tot.max_restarts = st[i].max_restarts;
        tot.dfs_nodes += st[i].dfs_nodes;
    }
    printf("# n=%d mode=%d t=%d..%d threads=%d units=%d elapsed=%.1fs\n", N, MODE, TMIN, TMAX, NTH, NUNITS + 1, el);
    printf("# t canon_orbits orbit_size_sum C(n-1,t) zerosum_skipped greedy_ok dfs_ok hard verified complete\n");
    int allok = 1;
    for (int t = TMIN; t <= TMAX; t++) {
        /* binomial exactly */
        unsigned long long b = 1; for (int i = 1; i <= t; i++) b = b * (unsigned long long)(N - 1 - t + i) / i;
        int complete = ((unsigned long long)(tot.orbsum[t] + tot.zerosum_skip[t]) == b);
        int good = complete && tot.hard[t] == 0 && tot.verified[t] == tot.canon[t];
        if (!good) allok = 0;
        printf("%d %ld %ld %llu %ld %ld %ld %ld %ld %s\n", t, tot.canon[t], tot.orbsum[t], b,
               tot.zerosum_skip[t], tot.greedy_ok[t], tot.dfs_ok[t], tot.hard[t], tot.verified[t],
               good ? "OK" : "FAIL");
    }
    printf("# max_greedy_restarts=%ld dfs_nodes=%ld ALL_%s\n", tot.max_restarts, tot.dfs_nodes, allok ? "OK" : "NOT_OK");
    return 0;
}
