/* gen.c -- exhaustive search for f(n), Erdos Problem 585.
 * f(n) = max #edges of an n-vertex graph with no two edge-disjoint cycles
 * having the same vertex set ("P-free").
 *
 * Method (see WRITEUP.md, Lemmas 1-4):
 *  A(k,t) = isomorphism classes of P-free graphs on k vertices with >= t edges.
 *  If G in A(k,t) and v is a vertex of minimum degree, then G-v in A(k-1, ceil(t(k-2)/k)).
 *  So A(k,t) is obtained by adding to each H in A(k-1, ceil(t(k-2)/k)) a new vertex v
 *  whose degree is <= every degree of the new graph, keeping P-free results, and
 *  reducing modulo isomorphism with a canonical form (individualisation-refinement,
 *  exhaustive over all leaves, no pruning).
 *
 * Usage: gen N L [nofilter]
 *   computes A(k,t_k) for k=1..N with t_N=L, t_{k-1}=ceil(t_k(k-2)/k);
 *   prints edge-count histogram per level, the max edge count, and the graphs
 *   attaining the max at each level (graph6).
 *   "nofilter": skip the P-test (validation: counts must equal A000088 / A008406).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 16
typedef unsigned __int128 u128;
typedef struct { uint16_t adj[MAXN]; } graph;

static int N;
static int nofilter = 0;

/* ---------------- canonical form ---------------- */
static int cn; static const uint16_t *cadj;
static u128 best; static int havebest;

/* refine: col[v] in 0..k-1 ; returns number of colours. Equitable refinement,
   new colour ordering determined only by (old colour, neighbour colour counts). */
static int refine(int *col, int k){
    int n=cn;
    for(;;){
        /* signature: old colour, then counts of neighbours in each colour */
        static int sig[MAXN][MAXN+1];
        for(int v=0;v<n;v++){
            sig[v][0]=col[v];
            for(int c=0;c<k;c++) sig[v][c+1]=0;
            for(int u=0;u<n;u++) if(cadj[v]>>u&1) sig[v][col[u]+1]++;
        }
        /* sort vertices by signature (insertion sort) */
        int ord[MAXN]; for(int i=0;i<n;i++) ord[i]=i;
        for(int i=1;i<n;i++){ int x=ord[i]; int j=i-1;
            while(j>=0 && memcmp(sig[ord[j]],sig[x],sizeof(int)*(k+1))>0){ ord[j+1]=ord[j]; j--; }
            ord[j+1]=x; }
        int nc[MAXN]; int k2=0;
        for(int i=0;i<n;i++){
            if(i>0 && memcmp(sig[ord[i-1]],sig[ord[i]],sizeof(int)*(k+1))!=0) k2++;
            nc[ord[i]]=k2;
        }
        k2++;
        for(int v=0;v<n;v++) col[v]=nc[v];
        if(k2==k) return k;
        k=k2;
    }
}

static void search(int *col, int k){
    int n=cn;
    k=refine(col,k);
    if(k==n){
        int pos[MAXN]; /* vertex at position i */
        for(int v=0;v<n;v++) pos[col[v]]=v;
        u128 code=0; int b=0;
        for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){
            if(cadj[pos[i]]>>pos[j]&1) code |= ((u128)1)<<b;
            b++;
        }
        if(!havebest || code<best){ best=code; havebest=1; }
        return;
    }
    /* first non-singleton colour */
    int cnt[MAXN]={0}; for(int v=0;v<n;v++) cnt[col[v]]++;
    int c=0; while(cnt[c]==1) c++;
    for(int v=0;v<n;v++) if(col[v]==c){
        int nc2[MAXN];
        for(int u=0;u<n;u++) nc2[u]=2*col[u]+1;
        nc2[v]=2*c; /* individualised vertex goes first in its cell */
        /* compress to 0..k */
        int map[2*MAXN+2]; for(int i=0;i<2*MAXN+2;i++) map[i]=-1;
        int used[2*MAXN+2]={0}; for(int u=0;u<n;u++) used[nc2[u]]=1;
        int r=0; for(int i=0;i<2*MAXN+2;i++) if(used[i]) map[i]=r++;
        for(int u=0;u<n;u++) nc2[u]=map[nc2[u]];
        search(nc2,r);
    }
}

static u128 canon(const graph *g, int n){
    cn=n; cadj=g->adj; havebest=0;
    int col[MAXN]; for(int v=0;v<n;v++) col[v]=0;
    search(col, n>0?1:0);
    return best;
}

/* ---------------- P-test ---------------- */
/* Does the graph (adjacency a[], vertex set mask S) have a Hamiltonian cycle
   through all of S? DFS from start s. */
static uint16_t ga[MAXN]; static uint16_t gS; static int gs; static int gsz;
static uint16_t ra[MAXN]; /* remaining graph for second cycle */

static int path2[MAXN];
static int ham2_dfs(int u, uint16_t vis, int len){
    if(len==gsz) return (ra[u]>>gs)&1;
    uint16_t cand = ra[u] & gS & ~vis;
    while(cand){ int w=__builtin_ctz(cand); cand&=cand-1;
        path2[len]=w;
        if(ham2_dfs(w, vis|(1u<<w), len+1)) return 1; }
    return 0;
}
static int second_ham(void){
    /* ra = ga restricted to S minus first cycle edges; need all deg>=2 */
    for(int u=0;u<N;u++) if(gS>>u&1) if(__builtin_popcount(ra[u]&gS)<2) return 0;
    path2[0]=gs;
    return ham2_dfs(gs, (uint16_t)(1u<<gs), 1);
}
static int path[MAXN];
static int ham1_dfs(int u, uint16_t vis, int len){
    if(len==gsz){
        if(!((ga[u]>>gs)&1)) return 0;
        /* first cycle: path[0..gsz-1], closing edge u-gs */
        for(int x=0;x<N;x++) ra[x]=ga[x]&gS;
        for(int i=0;i<gsz;i++){ int a=path[i], b=path[(i+1)%gsz];
            ra[a]&=~(1u<<b); ra[b]&=~(1u<<a); }
        return second_ham();
    }
    uint16_t cand = ga[u] & gS & ~vis;
    while(cand){ int w=__builtin_ctz(cand); cand&=cand-1;
        path[len]=w;
        if(ham1_dfs(w, vis|(1u<<w), len+1)) return 1; }
    return 0;
}
/* independent check of a witness: c1,c2 are cyclic sequences of L distinct
   vertices, consecutive vertices adjacent in g, same vertex set, no common edge. */
static long nwit=0;
static void verify_witness(const graph *g, int n, const int *c1, const int *c2, int L){
    uint32_t s1=0,s2=0; int E1[MAXN][MAXN]; memset(E1,0,sizeof E1);
    if(L<3){ fprintf(stderr,"BAD WITNESS len\n"); exit(2); }
    for(int i=0;i<L;i++){ int a=c1[i], b=c1[(i+1)%L];
        if(a<0||a>=n||b<0||b>=n||!((g->adj[a]>>b)&1)){ fprintf(stderr,"BAD WITNESS edge1\n"); exit(2);} 
        if(s1>>a&1){ fprintf(stderr,"BAD WITNESS repeat1\n"); exit(2);} s1|=1u<<a; E1[a][b]=E1[b][a]=1; }
    for(int i=0;i<L;i++){ int a=c2[i], b=c2[(i+1)%L];
        if(a<0||a>=n||b<0||b>=n||!((g->adj[a]>>b)&1)){ fprintf(stderr,"BAD WITNESS edge2\n"); exit(2);} 
        if(s2>>a&1){ fprintf(stderr,"BAD WITNESS repeat2\n"); exit(2);} s2|=1u<<a;
        if(E1[a][b]){ fprintf(stderr,"BAD WITNESS shared edge\n"); exit(2);} }
    if(s1!=s2){ fprintf(stderr,"BAD WITNESS vertex sets\n"); exit(2);} 
    nwit++;
}
/* is there S (containing vertex v if v>=0) with |S|>=5 such that G[S]
   has two edge-disjoint Hamiltonian cycles? */
static int hasP(const graph *g, int n, int v){
    int nn=n; N=n;
    for(int x=0;x<n;x++) ga[x]=g->adj[x];
    for(uint32_t S=0; S < (1u<<nn); S++){
        if(v>=0 && !((S>>v)&1)) continue;
        int sz=__builtin_popcount(S); if(sz<5) continue;
        int ok=1;
        for(int x=0;x<n && ok;x++) if(S>>x&1) if(__builtin_popcount(g->adj[x]&S)<4) ok=0;
        if(!ok) continue;
        gS=(uint16_t)S; gsz=sz; gs = (v>=0)? v : __builtin_ctz(S);
        path[0]=gs;
        if(ham1_dfs(gs, (uint16_t)(1u<<gs), 1)){ verify_witness(g,n,path,path2,sz); return 1; }
    }
    return 0;
}

/* ---------------- hash set ---------------- */
typedef struct { u128 *keys; uint8_t *used; size_t cap, cnt; } hset;
static void hs_init(hset *h, size_t cap){ h->cap=cap; h->cnt=0; h->keys=calloc(cap,sizeof(u128)); h->used=calloc(cap,1); }
static size_t hsh(u128 x){ uint64_t a=(uint64_t)x, b=(uint64_t)(x>>64); uint64_t z=a*0x9E3779B97F4A7C15ULL ^ (b+0x632BE59BD9B4E019ULL)*0xC2B2AE3D27D4EB4FULL; z^=z>>31; return (size_t)z; }
static int hs_insert(hset *h, u128 x){ /* returns 1 if new */
    if(2*(h->cnt+1) > h->cap){
        hset g; hs_init(&g, h->cap*2);
        for(size_t i=0;i<h->cap;i++) if(h->used[i]) hs_insert(&g, h->keys[i]);
        free(h->keys); free(h->used); *h=g;
    }
    size_t i=hsh(x)&(h->cap-1);
    while(h->used[i]){ if(h->keys[i]==x) return 0; i=(i+1)&(h->cap-1); }
    h->used[i]=1; h->keys[i]=x; h->cnt++; return 1;
}

/* ---------------- graph list ---------------- */
typedef struct { graph *g; size_t cnt, cap; } glist;
static void gl_push(glist *l, const graph *g){ if(l->cnt==l->cap){ l->cap=l->cap?2*l->cap:1024; l->g=realloc(l->g,l->cap*sizeof(graph)); } l->g[l->cnt++]=*g; }

static int nedges(const graph *g,int n){ int e=0; for(int i=0;i<n;i++) e+=__builtin_popcount(g->adj[i]); return e/2; }

static void graph6(const graph *g, int n, char *out){
    int k=0; out[k++]=63+n; int bits=0, val=0;
    for(int j=1;j<n;j++) for(int i=0;i<j;i++){
        val = (val<<1) | ((g->adj[i]>>j)&1); bits++;
        if(bits==6){ out[k++]=63+val; bits=0; val=0; }
    }
    if(bits>0){ val<<= (6-bits); out[k++]=63+val; }
    out[k]=0;
}

int main(int argc, char **argv){
    if(argc<3){ fprintf(stderr,"usage: gen N L [nofilter]\n"); return 1; }
    int NN=atoi(argv[1]); int L=atoi(argv[2]);
    if(argc>3 && !strcmp(argv[3],"nofilter")) nofilter=1;
    int t[MAXN+1]; t[NN]=L;
    for(int k=NN;k>=2;k--){ long num=(long)t[k]*(k-2); t[k-1]=(int)((num + k-1)/k); if(t[k-1]<0) t[k-1]=0; }
    t[1]=0; /* a 1-vertex graph has 0 edges */
    printf("thresholds:"); for(int k=1;k<=NN;k++) printf(" t_%d=%d",k,t[k]); printf("\n");
    glist cur={0}; graph g0; memset(&g0,0,sizeof g0); gl_push(&cur,&g0); /* k=1 */
    for(int k=2;k<=NN;k++){
        glist nxt={0}; hset hs; hs_init(&hs, 1<<16);
        int v=k-1;
        for(size_t i=0;i<cur.cnt;i++){
            graph H=cur.g[i]; int eH=nedges(&H,k-1);
            int degH[MAXN]; int mindeg=99;
            for(int x=0;x<k-1;x++){ degH[x]=__builtin_popcount(H.adj[x]); }
            for(uint32_t Nb=0; Nb < (1u<<(k-1)); Nb++){
                int d=__builtin_popcount(Nb);
                if(eH+d < t[k]) continue;
                int ok=1;
                for(int x=0;x<k-1;x++) if(degH[x] + (int)((Nb>>x)&1) < d){ ok=0; break; }
                if(!ok) continue;
                graph G=H; G.adj[v]=(uint16_t)Nb;
                for(int x=0;x<k-1;x++) if(Nb>>x&1) G.adj[x]|=(uint16_t)(1u<<v);
                if(!nofilter && hasP(&G,k,v)) continue;
                u128 c=canon(&G,k);
                if(hs_insert(&hs,c)) gl_push(&nxt,&G);
            }
            (void)mindeg;
        }
        free(hs.keys); free(hs.used);
        /* histogram */
        int hist[200]={0}; int mx=-1;
        for(size_t i=0;i<nxt.cnt;i++){ int e=nedges(&nxt.g[i],k); hist[e]++; if(e>mx) mx=e; }
        printf("n=%d t=%d classes=%zu max_edges=%d witnesses_verified=%ld  hist:",k,t[k],nxt.cnt,mx,nwit);
        for(int e=0;e<=mx;e++) if(hist[e]) printf(" %d:%d",e,hist[e]);
        printf("\n");
        if(getenv("DUMP")){
            for(size_t i=0;i<nxt.cnt;i++){ char s[64]; graph6(&nxt.g[i],k,s); printf("  class n=%d e=%d g6=%s\n",k,nedges(&nxt.g[i],k),s); }
        }
        if(!nofilter){
            for(size_t i=0;i<nxt.cnt;i++) if(nedges(&nxt.g[i],k)==mx){ char s[64]; graph6(&nxt.g[i],k,s); printf("  extremal n=%d e=%d g6=%s\n",k,mx,s); }
        }
        fflush(stdout);
        free(cur.g); cur=nxt;
    }
    return 0;
}
