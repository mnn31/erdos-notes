/* classify.c -- isomorph-free vertex-by-vertex classification of 3-uniform
 * families with no "generalized 4-cycle" (two distinct partitions of one 6-set
 * into two triples that are both fully present).
 *
 * Usage: ./classify N THR [dumpfile]
 *   Decides whether an avoiding family of >= THR triples on [N] exists, by
 *   listing (up to isomorphism) every avoiding family on [n] with at least
 *   thr_n triples, for n = 3..N, where thr_N = THR and
 *   thr_n = thr_{n+1} - floor(3*thr_{n+1}/(n+1)).
 *   Level n+1 is produced from level n by adding a new vertex w whose link L
 *   (a set of pairs of [n]) is an independent set of the conflict graph K(H),
 *   restricted to w having minimum degree.  (See WRITEUP.md, Lemmas 1-4.)
 *   If dumpfile is given, the level-N families are written to it (one per
 *   line, as lists of triples).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned __int128 u128;
#define MAXN 11
static int C2[64], C3[64];
static int tri_idx[MAXN][MAXN][MAXN];   /* colex index of {a<b<c} */
static int tri_v[200][3];
static int pair_idx[MAXN][MAXN];
static int pair_v[64][2];

static void init_tables(void){
  for(int i=0;i<64;i++){ C2[i]=i*(i-1)/2; C3[i]=i*(i-1)*(i-2)/6; }
  for(int c=0;c<MAXN;c++)for(int b=0;b<c;b++)for(int a=0;a<b;a++){
    int t=C3[c]+C2[b]+a; int s[3]={a,b,c};
    int p[6][3]={{a,b,c},{a,c,b},{b,a,c},{b,c,a},{c,a,b},{c,b,a}};
    for(int k=0;k<6;k++) tri_idx[p[k][0]][p[k][1]][p[k][2]]=t;
    memcpy(tri_v[t],s,sizeof s);
  }
  for(int b=0;b<MAXN;b++)for(int a=0;a<b;a++){int p=C2[b]+a; pair_idx[a][b]=pair_idx[b][a]=p; pair_v[p][0]=a; pair_v[p][1]=b;}
}
static inline int popc128(u128 x){ return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64)); }
static inline int bit(u128 x,int i){ return (int)((x>>i)&1); }
static inline u128 one(int i){ return ((u128)1)<<i; }

/* ---------- avoidance check (independent of the extension logic) ---------- */
static int is_avoiding(u128 F,int n){
  int v[6];
  for(v[0]=0;v[0]<n;v[0]++)for(v[1]=v[0]+1;v[1]<n;v[1]++)for(v[2]=v[1]+1;v[2]<n;v[2]++)
  for(v[3]=v[2]+1;v[3]<n;v[3]++)for(v[4]=v[3]+1;v[4]<n;v[4]++)for(v[5]=v[4]+1;v[5]<n;v[5]++){
    int cnt=0;
    for(int i=1;i<6;i++)for(int j=i+1;j<6;j++){ /* part containing v[0] is {v0,vi,vj} */
      int r[3],k=0; for(int q=1;q<6;q++) if(q!=i&&q!=j) r[k++]=v[q];
      if(bit(F,tri_idx[v[0]][v[i]][v[j]]) && bit(F,tri_idx[r[0]][r[1]][r[2]])) cnt++;
    }
    if(cnt>1) return 0;
  }
  return 1;
}

/* ---------- canonical form ---------- */
static uint64_t mix(uint64_t x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }
static int cmp_u64(const void*a,const void*b){ uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b; return x<y?-1:x>y; }

static int cn, cpos_vert[MAXN], cblock_start[MAXN], cblock_end[MAXN], cvert_cell[MAXN];
static int cperm[MAXN], cused[MAXN];
static int clist[200], clistn;
static u128 cbest;
static long long perms_tried;
static void canon_rec(int p){
  if(p==cn){
    perms_tried++;
    u128 m=0;
    for(int i=0;i<clistn;i++){ int t=clist[i]; m|=one(tri_idx[cperm[tri_v[t][0]]][cperm[tri_v[t][1]]][cperm[tri_v[t][2]]]); }
    if(m<cbest) cbest=m;
    return;
  }
  /* position p belongs to some block; choose an unused vertex whose cell equals that block */
  for(int u=0;u<cn;u++){
    if(cused[u]) continue;
    if(cvert_cell[u]!=cpos_vert[p]) continue;
    cused[u]=1; cperm[u]=p; canon_rec(p+1); cused[u]=0;
  }
}
/* returns canonical mask: min over all vertex maps consistent with an
   isomorphism-invariant ordered colouring */
static u128 canon(u128 F,int n){
  uint64_t col[MAXN], ncol[MAXN];
  clistn=0; for(int t=0;t<C3[n];t++) if(bit(F,t)) clist[clistn++]=t;
  for(int u=0;u<n;u++) col[u]=0;
  for(int i=0;i<clistn;i++) for(int k=0;k<3;k++) col[tri_v[clist[i]][k]]++;
  for(int round=0;round<n;round++){
    for(int u=0;u<n;u++){
      uint64_t ms[64]; int k=0;
      for(int i=0;i<clistn;i++){ int *v=tri_v[clist[i]];
        if(v[0]==u||v[1]==u||v[2]==u){
          uint64_t o[2]; int j=0; for(int q=0;q<3;q++) if(v[q]!=u) o[j++]=col[v[q]];
          if(o[0]>o[1]){uint64_t s=o[0];o[0]=o[1];o[1]=s;}
          ms[k++]=mix(o[0]*0x9e3779b97f4a7c15ULL+mix(o[1]));
        }
      }
      qsort(ms,k,sizeof(uint64_t),cmp_u64);
      uint64_t h=mix(col[u]+0x1234567ULL);
      for(int i=0;i<k;i++) h=mix(h^ms[i])+i;
      ncol[u]=h;
    }
    memcpy(col,ncol,sizeof col);
  }
  /* order distinct colours increasingly; block j = vertices of j-th colour */
  uint64_t d[MAXN]; int nd=0;
  for(int u=0;u<n;u++){ int f=0; for(int j=0;j<nd;j++) if(d[j]==col[u]) f=1; if(!f) d[nd++]=col[u]; }
  qsort(d,nd,sizeof(uint64_t),cmp_u64);
  int p=0;
  for(int j=0;j<nd;j++){
    cblock_start[j]=p;
    for(int u=0;u<n;u++) if(col[u]==d[j]){ cvert_cell[u]=j; cpos_vert[p++]=j; }
    cblock_end[j]=p;
  }
  cn=n; memset(cused,0,sizeof cused); cbest=~(u128)0;
  canon_rec(0);
  return cbest;
}

/* ---------- hash set of u128 ---------- */
typedef struct { u128 *keys; char *used; size_t cap, cnt; } hset;
static void hs_init(hset*h,size_t cap){ h->cap=cap; h->cnt=0; h->keys=calloc(cap,sizeof(u128)); h->used=calloc(cap,1); }
static void hs_free(hset*h){ free(h->keys); free(h->used); }
static int hs_add(hset*h,u128 k);
static void hs_grow(hset*h){
  hset g; hs_init(&g,h->cap*2);
  for(size_t i=0;i<h->cap;i++) if(h->used[i]) hs_add(&g,h->keys[i]);
  hs_free(h); *h=g;
}
static int hs_add(hset*h,u128 k){
  if(2*(h->cnt+1)>h->cap) hs_grow(h);
  size_t i=(size_t)(mix((uint64_t)k ^ mix((uint64_t)(k>>64))) % h->cap);
  while(h->used[i]){ if(h->keys[i]==k) return 0; i=(i+1)%h->cap; }
  h->used[i]=1; h->keys[i]=k; h->cnt++; return 1;
}

/* ---------- extension ---------- */
static uint64_t K[64];      /* conflict graph adjacency on pairs of [n] */
static int ext_n, ext_P, ext_need, ext_degH[MAXN];
static u128 ext_H;
static hset *ext_out;
static int ext_L[64], ext_Ln;
static long long ext_count_raw;
static int ext_max_total;

static void build_K(u128 H,int n){
  int P=C2[n]; for(int p=0;p<P;p++) K[p]=0;
  int v[5];
  for(v[0]=0;v[0]<n;v[0]++)for(v[1]=v[0]+1;v[1]<n;v[1]++)for(v[2]=v[1]+1;v[2]<n;v[2]++)
  for(v[3]=v[2]+1;v[3]<n;v[3]++)for(v[4]=v[3]+1;v[4]<n;v[4]++){
    int good[10],g=0;
    for(int i=0;i<5;i++)for(int j=i+1;j<5;j++){
      int r[3],k=0; for(int q=0;q<5;q++) if(q!=i&&q!=j) r[k++]=v[q];
      if(bit(H,tri_idx[r[0]][r[1]][r[2]])) good[g++]=pair_idx[v[i]][v[j]];
    }
    for(int a=0;a<g;a++)for(int b=0;b<g;b++) if(a!=b) K[good[a]]|=(1ULL<<good[b]);
  }
}
static void ext_leaf(void){
  int n=ext_n, L=ext_Ln;
  int degL[MAXN]={0};
  for(int i=0;i<L;i++){ degL[pair_v[ext_L[i]][0]]++; degL[pair_v[ext_L[i]][1]]++; }
  for(int u=0;u<n;u++) if(ext_degH[u]+degL[u] < L) return;   /* new vertex must be of minimum degree */
  u128 G=ext_H;
  for(int i=0;i<L;i++) G|=one(C3[n]+ext_L[i]);
  ext_count_raw++;
  u128 c=canon(G,n+1);
  hs_add(ext_out,c);
}
static void ext_rec(int p,uint64_t forbidden){
  /* bound: even taking every remaining non-forbidden pair cannot reach need */
  int avail=0; for(int q=p;q<ext_P;q++) if(!((forbidden>>q)&1)) avail++;
  if(ext_Ln+avail < ext_need) return;
  if(p==ext_P){ ext_leaf(); return; }
  if(!((forbidden>>p)&1)){
    ext_L[ext_Ln++]=p; ext_rec(p+1,forbidden|K[p]); ext_Ln--;
  }
  ext_rec(p+1,forbidden);
}
/* maximum independent set size of K restricted to pairs >= p, not in forbidden */
static int mis_rec(int p,uint64_t forbidden,int cur,int best){
  int avail=0; for(int q=p;q<ext_P;q++) if(!((forbidden>>q)&1)) avail++;
  if(cur+avail<=best) return best;
  if(p==ext_P) return cur>best?cur:best;
  if(!((forbidden>>p)&1)) best=mis_rec(p+1,forbidden|K[p],cur+1,best);
  best=mis_rec(p+1,forbidden,cur,best);
  return best;
}

int main(int argc,char**argv){
  if(argc<3){ fprintf(stderr,"usage: %s N THR [dumpfile]\n",argv[0]); return 1; }
  int N=atoi(argv[1]), THR=atoi(argv[2]);
  init_tables();
  int thr[MAXN+1];
  thr[N]=THR;
  for(int n=N-1;n>=3;n--){ thr[n]=thr[n+1]-(3*thr[n+1])/(n+1); if(thr[n]<0) thr[n]=0; }
  printf("thresholds:"); for(int n=3;n<=N;n++) printf(" thr_%d=%d",n,thr[n]); printf("\n");
  /* level 3: families on [3]: {} and {012} */
  hset cur; hs_init(&cur,1024);
  if(thr[3]<=0) hs_add(&cur,0);
  if(thr[3]<=1) hs_add(&cur,one(0));
  for(int n=3;n<N;n++){
    hset nxt; hs_init(&nxt,1024);
    ext_out=&nxt; ext_count_raw=0; perms_tried=0;
    int maxtot=-1;
    for(size_t i=0;i<cur.cap;i++){ if(!cur.used[i]) continue;
      u128 H=cur.keys[i];
      ext_n=n; ext_P=C2[n]; ext_H=H; ext_need=thr[n+1]-popc128(H); if(ext_need<0) ext_need=0;
      for(int u=0;u<n;u++) ext_degH[u]=0;
      for(int t=0;t<C3[n];t++) if(bit(H,t)) for(int k=0;k<3;k++) ext_degH[tri_v[t][k]]++;
      build_K(H,n); ext_Ln=0;
      int a=mis_rec(0,0,0,-1); if(popc128(H)+a>maxtot) maxtot=popc128(H)+a;
      ext_rec(0,0);
    }
    /* statistics for level n+1 */
    int hist[200]={0}, mx=-1; long long bad=0;
    for(size_t i=0;i<nxt.cap;i++){ if(!nxt.used[i]) continue; int s=popc128(nxt.keys[i]); hist[s]++; if(s>mx) mx=s;
      if(!is_avoiding(nxt.keys[i],n+1)) bad++; }
    printf("level %d (thr %d): %zu iso classes from %lld raw extensions; max size %d; max(|H|+alpha(K(H))) over level-%d reps = %d; non-avoiding found = %lld; perms tried %lld\n",
      n+1,thr[n+1],nxt.cnt,ext_count_raw,mx,n,maxtot,bad,perms_tried);
    printf("  size histogram:"); for(int s=0;s<200;s++) if(hist[s]) printf(" %d:%d",s,hist[s]); printf("\n");
    fflush(stdout);
    hs_free(&cur); cur=nxt;
  }
  if(argc>=4){
    FILE*f=fopen(argv[3],"w");
    for(size_t i=0;i<cur.cap;i++){ if(!cur.used[i]) continue; u128 F=cur.keys[i];
      fprintf(f,"%d",popc128(F));
      for(int t=0;t<C3[N];t++) if(bit(F,t)) fprintf(f," %d%d%d",tri_v[t][0],tri_v[t][1],tri_v[t][2]);
      fprintf(f,"\n"); }
    fclose(f);
  }
  return 0;
}
