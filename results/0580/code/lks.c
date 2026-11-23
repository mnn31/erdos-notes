/* Exhaustive check of tree-embedding statements of Loebl / Komlos-Sos type.
 * Usage: lks N J D E graphsJ.txt treesE.txt nthreads [maxreport]
 *   N = number of host vertices, J = |L| (vertices required to have degree >= D),
 *   E = number of tree edges.  Statement checked: every graph on N vertices with
 *   at least J vertices of degree >= D contains every tree with E edges.
 * Reduction: L = J chosen vertices of degree >= D, S = other N-J vertices.
 *   Delete S-S edges; trim each u in L to exactly max(0, D - deg_L(u)) neighbours in S.
 *   (Every hypothesis graph contains such a graph; tree containment is monotone.)
 *   H = G[L] runs over graphs on J vertices up to isomorphism; the L-S bipartite part
 *   is a multiset of N-J columns (subsets of L, empty allowed) with row sums r_u.
 * Output: number of reduced host graphs checked and every counterexample (up to maxreport).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>

#define MAXV 32
#define MAXT 8000
typedef uint32_t mask;

static int N, J, D, E, NT, NS;
static int ngr; static mask (*gadj)[MAXV];
/* trees */
static int ntr; static int tsz;
static int tord[MAXT][MAXV], tpar[MAXT][MAXV], tdeg[MAXT][MAXV];

typedef struct { int h; mask c0; } work_t;
static work_t *works; static long nworks;
static atomic_long next_work, total_graphs, total_bad;
static int maxreport = 20;
static pthread_mutex_t pm = PTHREAD_MUTEX_INITIALIZER;

static int popc(mask x){ return __builtin_popcount(x); }

/* backtracking embedding of tree t into host adj (n vertices) */
typedef struct { mask adj[MAXV]; mask degge[MAXV+1]; int n; } host_t;
static int emb_rec(const host_t *g, int t, int i, int *img, mask used){
    if (i == tsz) return 1;
    int tv = tord[t][i];
    mask cand = g->adj[img[tpar[t][tv]]] & ~used & g->degge[tdeg[t][tv]];
    while (cand){
        int v = __builtin_ctz(cand); cand &= cand - 1;
        img[tv] = v;
        if (emb_rec(g, t, i+1, img, used | (1u<<v))) return 1;
    }
    return 0;
}
static int embeds(const host_t *g, int t){
    int img[MAXV];
    int r = tord[t][0];
    mask cand = g->degge[tdeg[t][r]];
    while (cand){
        int v = __builtin_ctz(cand); cand &= cand - 1;
        img[r] = v;
        if (emb_rec(g, t, 1, img, 1u<<v)) return 1;
    }
    return 0;
}

typedef struct { int h; mask cols[MAXV]; int rem[MAXV]; long cnt, bad; int order[MAXT]; } tstate;

static int countonly = 0; static long dumpevery = 0;
static void check_graph(tstate *st){
    if (countonly){ st->cnt++; return; }
    host_t g; memset(&g, 0, sizeof g); g.n = N;
    for (int u = 0; u < J; u++) g.adj[u] = gadj[st->h][u];
    for (int s = 0; s < NS; s++){
        mask c = st->cols[s]; int sv = J + s;
        g.adj[sv] = c;
        for (int u = 0; u < J; u++) if (c >> u & 1) g.adj[u] |= 1u << sv;
    }
    /* sanity: hypothesis holds */
    for (int u = 0; u < J; u++) if (popc(g.adj[u]) < D){ fprintf(stderr,"BUG degree\n"); exit(2); }
    for (int d = 0; d <= N; d++){ mask m = 0; for (int v = 0; v < N; v++) if (popc(g.adj[v]) >= d) m |= 1u<<v; g.degge[d] = m; }
    st->cnt++;
    if (dumpevery && st->cnt % dumpevery == 0){ pthread_mutex_lock(&pm); printf("HOST"); for (int v = 0; v < N; v++) printf(" %x", g.adj[v]); printf("\n"); pthread_mutex_unlock(&pm); }
    for (int i = 0; i < ntr; i++){
        int t = st->order[i];
        if (!embeds(&g, t)){
            st->bad++;
            /* move to front */
            for (int k = i; k > 0; k--) st->order[k] = st->order[k-1];
            st->order[0] = t;
            long b = atomic_fetch_add(&total_bad, 1);
            if (b < maxreport){
                pthread_mutex_lock(&pm);
                printf("COUNTEREXAMPLE tree#%d host adj(bitmasks):", t);
                for (int v = 0; v < N; v++) printf(" %x", g.adj[v]);
                printf("\n"); fflush(stdout);
                pthread_mutex_unlock(&pm);
            }
            return;
        }
    }
}

/* choose column s (s>=1 here), non-increasing masks */
static void rec(tstate *st, int s, mask prev){
    int left = NS - s;
    if (left == 0){
        for (int u = 0; u < J; u++) if (st->rem[u]) return;
        check_graph(st); return;
    }
    mask allowed = 0, forced = 0;
    for (int u = 0; u < J; u++){
        if (st->rem[u] > left) return;
        if (st->rem[u] > 0) allowed |= 1u<<u;
        if (st->rem[u] == left) forced |= 1u<<u;
    }
    /* iterate submasks c of allowed, c >= forced-superset, c <= prev, decreasing */
    mask c = allowed;
    for (;;){
        if (c <= prev && (c & forced) == forced){
            st->cols[s] = c;
            for (int u = 0; u < J; u++) if (c>>u&1) st->rem[u]--;
            rec(st, s+1, c);
            for (int u = 0; u < J; u++) if (c>>u&1) st->rem[u]++;
        }
        if (c == 0) break;
        c = (c - 1) & allowed;
    }
}

static void *worker(void *arg){
    tstate *st = (tstate*)arg;
    for (;;){
        long w = atomic_fetch_add(&next_work, 1);
        if (w >= nworks) break;
        if (nworks >= 50 && w % (nworks/50) == 0){ pthread_mutex_lock(&pm); fprintf(stderr, "progress %ld/%ld hosts_so_far(thread)=%ld\n", w, nworks, st->cnt); pthread_mutex_unlock(&pm); }
        int h = works[w].h; mask c0 = works[w].c0;
        st->h = h;
        for (int u = 0; u < J; u++){ int d = popc(gadj[h][u]); st->rem[u] = d >= D ? 0 : D - d; }
        st->cols[0] = c0;
        for (int u = 0; u < J; u++) if (c0>>u&1) st->rem[u]--;
        rec(st, 1, c0);
    }
    atomic_fetch_add(&total_graphs, st->cnt);
    return NULL;
}

static int read_line_graph(FILE *f, int *nv, int *m, int ed[][2]){
    if (fscanf(f, "%d %d", nv, m) != 2) return 0;
    for (int i = 0; i < *m; i++) if (fscanf(f, "%d %d", &ed[i][0], &ed[i][1]) != 2) return 0;
    return 1;
}

int main(int argc, char **argv){
    if (argc < 8){ fprintf(stderr, "usage\n"); return 1; }
    N = atoi(argv[1]); J = atoi(argv[2]); D = atoi(argv[3]); E = atoi(argv[4]);
    NT = atoi(argv[7]); if (argc > 8) maxreport = atoi(argv[8]);
    long wlo = argc > 9 ? atol(argv[9]) : 0, whi = argc > 10 ? atol(argv[10]) : -1;
    NS = N - J; countonly = getenv("COUNTONLY") != NULL; if (getenv("DUMPEVERY")) dumpevery = atol(getenv("DUMPEVERY"));
    if (N > MAXV || J > N || NS < 1){ fprintf(stderr,"bad params\n"); return 1; }
    static int ed[1000][2]; int nv, m;
    /* graphs */
    FILE *f = fopen(argv[5], "r"); if (!f){ perror("graphs"); return 1; }
    gadj = calloc(20000, sizeof *gadj); ngr = 0;
    while (read_line_graph(f, &nv, &m, ed)){
        if (nv != J){ fprintf(stderr,"graph size mismatch\n"); return 1; }
        for (int i = 0; i < m; i++){ gadj[ngr][ed[i][0]] |= 1u<<ed[i][1]; gadj[ngr][ed[i][1]] |= 1u<<ed[i][0]; }
        ngr++;
    }
    fclose(f);
    /* trees: root at a max-degree vertex, BFS order */
    f = fopen(argv[6], "r"); if (!f){ perror("trees"); return 1; }
    ntr = 0;
    while (read_line_graph(f, &nv, &m, ed)){
        if (m != E || nv != E+1){ fprintf(stderr,"tree size mismatch\n"); return 1; }
        tsz = nv; int deg[MAXV] = {0}; mask ad[MAXV] = {0};
        for (int i = 0; i < m; i++){ ad[ed[i][0]] |= 1u<<ed[i][1]; ad[ed[i][1]] |= 1u<<ed[i][0]; deg[ed[i][0]]++; deg[ed[i][1]]++; }
        int root = 0; for (int v = 0; v < nv; v++) if (deg[v] > deg[root]) root = v;
        int seen[MAXV] = {0}; int q = 0, qe = 0; tord[ntr][qe++] = root; seen[root] = 1; tpar[ntr][root] = -1;
        while (q < qe){ int x = tord[ntr][q++];
            /* children in decreasing degree order */
            for (int dd = nv; dd >= 0; dd--) for (int y = 0; y < nv; y++) if ((ad[x]>>y&1) && !seen[y] && deg[y]==dd){ seen[y]=1; tpar[ntr][y]=x; tord[ntr][qe++]=y; } }
        if (qe != nv){ fprintf(stderr,"tree not connected\n"); return 1; }
        for (int v = 0; v < nv; v++) tdeg[ntr][v] = deg[v];
        ntr++;
    }
    fclose(f);
    if (E + 1 > N){ printf("trivial: tree larger than host\n"); }
    /* work items */
    works = malloc(sizeof(work_t) * (long)ngr * (1L<<J)); nworks = 0;
    long skippedH = 0;
    for (int h = 0; h < ngr; h++){
        int rem[MAXV]; mask allowed = 0, forced = 0; int ok = 1;
        for (int u = 0; u < J; u++){ int d = popc(gadj[h][u]); rem[u] = d >= D ? 0 : D - d;
            if (rem[u] > NS) ok = 0; if (rem[u] > 0) allowed |= 1u<<u; if (rem[u] == NS) forced |= 1u<<u; }
        if (!ok){ skippedH++; continue; }
        mask c = allowed;
        for (;;){ if ((c & forced) == forced){ works[nworks].h = h; works[nworks].c0 = c; nworks++; }
            if (c == 0) break; c = (c-1) & allowed; }
    }
    /* shuffle work order for balance (deterministic) */
    srand(12345);
    for (long i = nworks-1; i > 0; i--){ long j = ((long)rand()*RAND_MAX + rand()) % (i+1); work_t t = works[i]; works[i] = works[j]; works[j] = t; }
    if (whi < 0 || whi > nworks) whi = nworks; if (wlo > whi) wlo = whi; works += wlo; nworks = whi - wlo;
    fprintf(stderr, "work range [%ld,%ld)\n", wlo, whi);
    pthread_t th[64]; tstate *sts = calloc(NT, sizeof(tstate));
    for (int i = 0; i < NT; i++){ for (int t = 0; t < ntr; t++) sts[i].order[t] = t; pthread_create(&th[i], NULL, worker, &sts[i]); }
    for (int i = 0; i < NT; i++) pthread_join(th[i], NULL);
    printf("RESULT range=[%ld,%ld) N=%d J=%d D=%d E=%d graphsH=%d infeasibleH=%ld trees=%d reduced_hosts=%ld counterexamples=%ld\n",
           wlo, whi, N, J, D, E, ngr, skippedH, ntr, (long)total_graphs, (long)total_bad);
    return 0;
}
