// Erdos 848, distinct-pairs variant (and diagonal variant as sanity check).
// Graph on {1..Nmax}: a~b (a!=b) iff ab+1 is NOT squarefree.
// diag mode: additionally only vertices v with v^2+1 not squarefree are allowed.
// D(N) = clique number of G restricted to [1,N].
//
// Phase 1 (sequential, N<=Nseq): exact incremental: D(N)=D(N-1)+1 iff the
//   neighbourhood of N inside [1,N-1] contains a clique of size D(N-1).
// Phase 2 (parallel, Nseq<N<=Nmax): hypothesis D(M)=c(M)=floor((M+18)/25) for M<N.
//   For N not = 7 mod 25 we must refute a clique of size c(N) in nbhd(N) ("test A").
//   For N = 7 mod 25 the residue class gives the witness. By induction (omega grows by
//   at most 1 per added vertex) all A-refutations together prove D(N)=c(N).
//   Test B ("mixed"): is there a clique of size c(N) with maximum element N that is not
//   a subset of C7 and not a subset of C18?  The set T of N where B succeeds determines
//   uniqueness of maximum sets (see RESULT.md).
// Exact: all arithmetic in 64-bit integers, adjacency from p^2 | ab+1 via modular inverse.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>

typedef uint64_t u64;
static int NMAX, W, DIAG, NSEQ, MIXMAX, NTHR, NLO;
static u64 *ADJ;          // ADJ[v*W + ...]
static u64 *ACTIVE;       // allowed vertices
static u64 *C7M, *C18M;   // class masks
#define ROW(v) (ADJ + (size_t)(v) * W)

static inline void setbit(u64 *b, int i) { b[i >> 6] |= 1ULL << (i & 63); }
static inline int getbit(const u64 *b, int i) { return (b[i >> 6] >> (i & 63)) & 1; }
static inline void clrbit(u64 *b, int i) { b[i >> 6] &= ~(1ULL << (i & 63)); }

static int64_t inv_mod(int64_t a, int64_t m) { // a coprime to m
    int64_t g = m, x = 0, x1 = 1, a1 = a % m; if (a1 < 0) a1 += m;
    int64_t r0 = m, r1 = a1; x = 0; x1 = 1;
    while (r1) { int64_t q = r0 / r1, t = r0 - q * r1; r0 = r1; r1 = t; t = x - q * x1; x = x1; x1 = t; }
    (void)g; if (r0 != 1) return -1; x %= m; if (x < 0) x += m; return x;
}
static int c_of(int N) { return (N + 18) / 25; }

static int nsf_trial(u64 x) { // independent check: x not squarefree?
    for (u64 p = 2; p * p <= x; p++) if (x % (p * p) == 0) return 1;
    return 0;
}

static void build(void) {
    W = (NMAX + 1 + 63) / 64;
    ADJ = calloc((size_t)(NMAX + 1) * W, sizeof(u64));
    ACTIVE = calloc(W, 8); C7M = calloc(W, 8); C18M = calloc(W, 8);
    char *comp = calloc(NMAX + 2, 1);
    for (int i = 2; (long)i * i <= NMAX + 1; i++) if (!comp[i]) for (int j = i * i; j <= NMAX + 1; j += i) comp[j] = 1;
    for (int p = 2; p <= NMAX + 1; p++) {
        if (comp[p]) continue;
        int64_t q = (int64_t)p * p;
        if (q > (int64_t)NMAX * NMAX + 1) break;
        for (int a = 1; a <= NMAX; a++) {
            if (a % p == 0) continue;
            int64_t b0 = (q - inv_mod(a, q)) % q; // ab0 = -1 mod q
            if (b0 == 0) continue;
            for (int64_t b = b0; b <= NMAX; b += q) if (b != a) setbit(ROW(a), (int)b);
        }
    }
    for (int v = 1; v <= NMAX; v++) {
        int ok = 1;
        if (DIAG) { // v^2+1 nonsquarefree
            u64 x = (u64)v * v + 1; ok = 0;
            for (u64 p = 2; p * p <= x; p++) if (x % (p * p) == 0) { ok = 1; break; }
        }
        if (ok) setbit(ACTIVE, v);
        if (v % 25 == 7) setbit(C7M, v);
        if (v % 25 == 18) setbit(C18M, v);
    }
    for (int v = 1; v <= NMAX; v++) {
        u64 *r = ROW(v);
        if (!getbit(ACTIVE, v)) { memset(r, 0, W * 8); continue; }
        for (int k = 0; k < W; k++) r[k] &= ACTIVE[k];
    }
    free(comp);
}

// ---- Tomita/BBMC decision search: is there a clique of size >= t in P (bitset, Wn words)?
typedef struct { int *stack; int found; long nodes; int Wn; } Ctx;

static int expand(Ctx *cx, u64 *P, int size, int t) {
    int Wn = cx->Wn;
    cx->nodes++;
    int n = 0; for (int k = 0; k < Wn; k++) n += __builtin_popcountll(P[k]);
    if (size + n < t) return 0;
    int *order = malloc(sizeof(int) * (n + 1)), *col = malloc(sizeof(int) * (n + 1));
    u64 *Q = malloc(Wn * 8), *R = malloc(Wn * 8), *NP = malloc(Wn * 8);
    memcpy(Q, P, Wn * 8);
    int m = 0, k = 0, lo = 0;
    int need = t - size; // vertices with color < need are never branched on
    while (1) {
        while (lo < Wn && !Q[lo]) lo++;
        if (lo >= Wn) break;
        k++;
        memcpy(R + lo, Q + lo, (Wn - lo) * 8);
        int rl = lo;
        while (1) {
            while (rl < Wn && !R[rl]) rl++;
            if (rl >= Wn) break;
            int v = rl * 64 + __builtin_ctzll(R[rl]);
            const u64 *av = ROW(v);
            R[rl] &= R[rl] - 1;
            for (int j = rl; j < Wn; j++) R[j] &= ~av[j];
            clrbit(Q, v);
            if (k >= need) { order[m] = v; col[m] = k; m++; }
        }
    }
    int res = 0;
    for (int i = m - 1; i >= 0; i--) {
        if (size + col[i] < t) break;
        int v = order[i];
        const u64 *av = ROW(v);
        int cnt = 0;
        for (int j = 0; j < Wn; j++) { NP[j] = P[j] & av[j]; cnt += __builtin_popcountll(NP[j]); }
        cx->stack[size] = v;
        if (size + 1 >= t) { res = 1; break; }
        if (size + 1 + cnt >= t && expand(cx, NP, size + 1, t)) { res = 1; break; }
        clrbit(P, v);
    }
    free(order); free(col); free(Q); free(R); free(NP);
    return res;
}

// clique of size >= t inside P (P is modified)? stack receives witness (first t entries)
static int has_clique(u64 *P, int Wn, int t, int *stack, long *nodes) {
    if (t <= 0) return 1;
    Ctx cx = { stack, 0, 0, Wn };
    int r = expand(&cx, P, 0, t);
    if (nodes) *nodes += cx.nodes;
    return r;
}

static void nbhd(int N, u64 *U, int Wn) { // nbhd of N inside [1,N-1]
    memcpy(U, ROW(N), Wn * 8);
    for (int j = 0; j < Wn; j++) {
        int lo = j * 64;
        if (lo + 63 < N) continue;
        u64 mask = 0; for (int b = 0; b < 64; b++) if (lo + b < N) mask |= 1ULL << b;
        U[j] &= mask;
    }
}

static int verify_clique(const int *S, int k) { // independent trial-division check
    for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++) {
        if (S[i] == S[j]) return 0;
        if (!nsf_trial((u64)S[i] * S[j] + 1)) return 0;
    }
    if (DIAG) for (int i = 0; i < k; i++) if (!nsf_trial((u64)S[i] * S[i] + 1)) return 0;
    return 1;
}

// ---- results of phase 2
static signed char *RA, *RB; static long *NODES;
static atomic_int NEXT;
static int **BW; static int *BWn; // witnesses for B successes

static int cmpint(const void *a, const void *b) { return *(int *)a - *(int *)b; }

static void *worker(void *arg) {
    (void)arg;
    int *stack = malloc(sizeof(int) * (NMAX + 2));
    u64 *U = malloc(W * 8), *P = malloc(W * 8), *X = malloc(W * 8);
    while (1) {
        int idx = atomic_fetch_add(&NEXT, 1);
        int N = NMAX - idx;
        if (N <= NSEQ || N < NLO) break;
        int Wn = N / 64 + 1;
        long nodes = 0;
        RA[N] = -1; RB[N] = -1;
        if (!getbit(ACTIVE, N)) { RA[N] = 0; RB[N] = 0; NODES[N] = 0; continue; }
        int c = c_of(N);
        int r7 = (N % 25 == 7), r18 = (N % 25 == 18);
        nbhd(N, U, Wn);
        // test A: clique of size c(N) in U (only meaningful when N not = 7 mod 25)
        if (!r7) { memcpy(P, U, Wn * 8); RA[N] = has_clique(P, Wn, c, stack, &nodes); }
        else RA[N] = 2; // witness by class
        // test B (mixed) only up to MIXMAX
        if (N <= MIXMAX) {
            if (!r7 && !r18) {
                if (RA[N] == 1) RB[N] = 1;
                else { memcpy(P, U, Wn * 8); RB[N] = has_clique(P, Wn, c - 1, stack, &nodes); }
                if (RB[N] == 1) { int k = c - 1; int *S = malloc(sizeof(int) * (k + 1)); memcpy(S, stack, k * sizeof(int)); S[k] = N; BW[N] = S; BWn[N] = k + 1; }
            } else {
                const u64 *cls = r7 ? C7M : C18M;
                for (int j = 0; j < Wn; j++) X[j] = U[j] & ~cls[j];
                int res = 0;
                for (int j = 0; j < Wn && !res; j++) {
                    while (X[j] && !res) {
                        int x = j * 64 + __builtin_ctzll(X[j]);
                        X[j] &= X[j] - 1;
                        const u64 *ax = ROW(x);
                        int cnt = 0;
                        // P = U & N(x) minus earlier-processed X elements (those < x in X order)
                        for (int k = 0; k < Wn; k++) {
                            u64 keep = U[k] & ax[k];
                            // remove processed non-class elements: non-class elements of U with index < x
                            u64 noncls = U[k] & ~cls[k];
                            u64 below;
                            if (k < j) below = ~0ULL; else if (k > j) below = 0; else below = (x & 63) ? ((1ULL << (x & 63)) - 1) : 0;
                            keep &= ~(noncls & below);
                            P[k] = keep; cnt += __builtin_popcountll(keep);
                        }
                        if (cnt < c - 2) continue;
                        if (has_clique(P, Wn, c - 2, stack, &nodes)) {
                            res = 1;
                            int k = c - 2; int *S = malloc(sizeof(int) * (k + 2)); memcpy(S, stack, k * sizeof(int)); S[k] = x; S[k + 1] = N; BW[N] = S; BWn[N] = k + 2;
                        }
                    }
                }
                RB[N] = res;
            }
        }
        NODES[N] = nodes;
    }
    free(stack); free(U); free(P); free(X);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: d848 Nmax distinct|diag Nseq MIXMAX threads [outprefix]\n"); return 1; }
    NMAX = atoi(argv[1]); DIAG = !strcmp(argv[2], "diag"); NSEQ = atoi(argv[3]); MIXMAX = atoi(argv[4]); NTHR = atoi(argv[5]);
    const char *pre = argc > 6 ? argv[6] : "out";
    NLO = argc > 7 ? atoi(argv[7]) : 0; // phase 2 only tests N >= NLO (lower N covered by an earlier run)
    if (NSEQ > NMAX) NSEQ = NMAX;
    time_t t0 = time(NULL);
    build();
    fprintf(stderr, "built adjacency N=%d W=%d in %lds\n", NMAX, W, (long)(time(NULL) - t0));
    // adjacency spot check vs trial division
    srand(12345);
    for (int s = 0; s < 200000; s++) {
        int a = 1 + rand() % NMAX, b = 1 + rand() % NMAX; if (a == b) continue;
        int e = getbit(ROW(a), b);
        int want = getbit(ACTIVE, a) && getbit(ACTIVE, b) && nsf_trial((u64)a * b + 1);
        if (e != want) { fprintf(stderr, "ADJ MISMATCH %d %d\n", a, b); return 2; }
    }
    fprintf(stderr, "adjacency spot check OK (200000 random pairs)\n");
    char fn[512];
    snprintf(fn, sizeof fn, "%s_records.txt", pre);
    FILE *fr = fopen(fn, "w");
    // ---- phase 1 sequential
    int D = 0; int *stack = malloc(sizeof(int) * (NMAX + 2)); u64 *U = malloc(W * 8);
    int *Dseq = calloc(NSEQ + 2, sizeof(int));
    long nodes1 = 0;
    for (int N = 1; N <= NSEQ; N++) {
        if (getbit(ACTIVE, N)) {
            int Wn = N / 64 + 1;
            nbhd(N, U, Wn);
            if (has_clique(U, Wn, D, stack, &nodes1)) {
                int S[4096]; int k = 0;
                for (int i = 0; i < D; i++) S[k++] = stack[i];
                S[k++] = N; qsort(S, k, sizeof(int), cmpint);
                D++;
                if (!verify_clique(S, k)) { fprintf(stderr, "WITNESS FAIL at %d\n", N); return 3; }
                fprintf(fr, "%d %d %d", N, D, c_of(N));
                for (int i = 0; i < k; i++) fprintf(fr, i ? ",%d" : " %d", S[i]);
                fprintf(fr, "\n");
            }
        }
        Dseq[N] = D;
    }
    fclose(fr);
    fprintf(stderr, "phase1 done to N=%d D=%d c=%d nodes=%ld t=%lds\n", NSEQ, D, c_of(NSEQ), nodes1, (long)(time(NULL) - t0));
    snprintf(fn, sizeof fn, "%s_Dseq.txt", pre);
    FILE *fd = fopen(fn, "w"); for (int N = 1; N <= NSEQ; N++) fprintf(fd, "%d %d %d\n", N, Dseq[N], c_of(N)); fclose(fd);
    if (NMAX <= NSEQ) return 0;
    if (D != c_of(NSEQ)) { fprintf(stderr, "D(Nseq) != c(Nseq): phase 2 hypothesis not applicable\n"); return 4; }
    // ---- phase 2 parallel
    RA = malloc(NMAX + 1); RB = malloc(NMAX + 1); NODES = calloc(NMAX + 1, sizeof(long));
    BW = calloc(NMAX + 1, sizeof(int *)); BWn = calloc(NMAX + 1, sizeof(int));
    atomic_store(&NEXT, 0);
    pthread_t th[64];
    for (int i = 0; i < NTHR; i++) pthread_create(&th[i], NULL, worker, NULL);
    for (int i = 0; i < NTHR; i++) pthread_join(th[i], NULL);
    fprintf(stderr, "phase2 done t=%lds\n", (long)(time(NULL) - t0));
    snprintf(fn, sizeof fn, "%s_phase2.txt", pre);
    FILE *f2 = fopen(fn, "w");
    int firstA = -1; long totnodes = 0; int nB = 0;
    for (int N = (NLO > NSEQ + 1 ? NLO : NSEQ + 1); N <= NMAX; N++) {
        fprintf(f2, "%d %d %d %d %ld\n", N, c_of(N), RA[N], RB[N], NODES[N]);
        totnodes += NODES[N];
        if (RA[N] == 1 && firstA < 0) firstA = N;
        if (RB[N] == 1) nB++;
    }
    fclose(f2);
    snprintf(fn, sizeof fn, "%s_mixed_witnesses.txt", pre);
    FILE *fw = fopen(fn, "w");
    for (int N = (NLO > NSEQ + 1 ? NLO : NSEQ + 1); N <= NMAX; N++) if (BW[N]) {
        qsort(BW[N], BWn[N], sizeof(int), cmpint);
        int ok = verify_clique(BW[N], BWn[N]);
        fprintf(fw, "%d %d %d %s", N, c_of(N), BWn[N], ok ? "OK" : "BAD");
        for (int i = 0; i < BWn[N]; i++) fprintf(fw, i ? ",%d" : " %d", BW[N][i]);
        fprintf(fw, "\n");
        if (!ok) fprintf(stderr, "BAD mixed witness at %d\n", N);
    }
    fclose(fw);
    printf("NMAX=%d mode=%s NSEQ=%d MIXMAX=%d\n", NMAX, DIAG ? "diag" : "distinct", NSEQ, MIXMAX);
    printf("D(NSEQ)=%d=c(NSEQ)\n", D);
    printf("first N with test A success (hypothesis break): %d\n", firstA);
    printf("number of N in (NSEQ,MIXMAX] with mixed clique of size c(N) ending at N: %d\n", nB);
    printf("total search nodes phase2: %ld, wall %lds\n", totnodes, (long)(time(NULL) - t0));
    return 0;
}
