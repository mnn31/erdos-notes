// g4.c: generate 4-regular graphs (all, incl. disconnected) by vertex insertion,
// canonical form by individualization-refinement (exhaustive leaves, lexmin matrix),
// and compute strong chromatic index (chi of L(G)^2) exactly.
// Records: n uint32 rows (bit j of row i = edge ij), canonical labelling.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
#define MAXN 24
static int N;
static u32 G[MAXN];
static u32 best[MAXN]; static int havebest;
static long long leaves;

static void leaf(int *lab){
  int pos[MAXN]; u32 row[MAXN];
  leaves++;
  for(int i=0;i<N;i++) pos[lab[i]]=i;
  for(int i=0;i<N;i++){ u32 a=G[lab[i]],r=0; while(a){int j=__builtin_ctz(a); a&=a-1; r|=1u<<pos[j];} row[i]=r; }
  if(!havebest){ memcpy(best,row,sizeof(u32)*N); havebest=1; return; }
  for(int i=0;i<N;i++){ if(row[i]<best[i]){ memcpy(best,row,sizeof(u32)*N); return;} if(row[i]>best[i]) return; }
}
// partition: lab[0..N-1], cell boundaries cs[0..nc] (cs[0]=0, cs[nc]=N)
static void refine(int *lab, int *cs, int *pnc){
  int nc=*pnc;
  int w=0;
  while(w<nc){
    u32 W=0; for(int i=cs[w];i<cs[w+1];i++) W|=1u<<lab[i];
    int cnt[MAXN]; for(int v=0;v<N;v++) cnt[v]=__builtin_popcount(G[v]&W);
    int split=0; int ncs[MAXN+1]; int nn=0; int nlab[MAXN]; int p=0;
    for(int c=0;c<nc;c++){
      int s=cs[c],e=cs[c+1];
      // stable insertion sort by cnt
      int tmp[MAXN]; int k=0; for(int i=s;i<e;i++) tmp[k++]=lab[i];
      for(int i=1;i<k;i++){int x=tmp[i],j=i-1; while(j>=0&&cnt[tmp[j]]>cnt[x]){tmp[j+1]=tmp[j];j--;} tmp[j+1]=x;}
      ncs[nn++]=p;
      for(int i=0;i<k;i++){ if(i>0 && cnt[tmp[i]]!=cnt[tmp[i-1]]){ ncs[nn++]=p; split=1;} nlab[p++]=tmp[i]; }
    }
    ncs[nn]=N;
    if(split){ memcpy(lab,nlab,sizeof(int)*N); memcpy(cs,ncs,sizeof(int)*(nn+1)); nc=nn; w=0; }
    else w++;
  }
  *pnc=nc;
}
static void search(int *lab,int *cs,int nc){
  refine(lab,cs,&nc);
  if(nc==N){ leaf(lab); return; }
  int t=-1,ts=1000;
  for(int c=0;c<nc;c++){int s=cs[c+1]-cs[c]; if(s>1 && s<ts){ts=s;t=c;}}
  int s=cs[t],e=cs[t+1];
  for(int k=s;k<e;k++){
    int lab2[MAXN], cs2[MAXN+1];
    memcpy(lab2,lab,sizeof(int)*N);
    int v=lab[k]; // move v to front of cell
    for(int i=k;i>s;i--) lab2[i]=lab2[i-1]; lab2[s]=v;
    int nc2=0; for(int c=0;c<=t;c++) cs2[nc2++]=cs[c]; cs2[nc2++]=s+1; for(int c=t+1;c<=nc;c++) cs2[nc2++]=cs[c];
    search(lab2,cs2,nc2-1);
  }
}
static void canon(u32 *g,int n,u32 *out){
  N=n; memcpy(G,g,sizeof(u32)*n); havebest=0;
  // initial invariant: (#edges among neighbours, |N2|)
  long inv[MAXN];
  for(int v=0;v<n;v++){ int t=0; u32 a=G[v]; u32 n2=0; while(a){int j=__builtin_ctz(a);a&=a-1; t+=__builtin_popcount(G[j]&G[v]); n2|=G[j];} n2&=~(G[v]|(1u<<v)); inv[v]=(long)t*100+__builtin_popcount(n2); }
  int lab[MAXN],cs[MAXN+1],nc=0;
  for(int i=0;i<n;i++) lab[i]=i;
  for(int i=1;i<n;i++){int x=lab[i],j=i-1; while(j>=0&&inv[lab[j]]>inv[x]){lab[j+1]=lab[j];j--;} lab[j+1]=x;}
  cs[nc++]=0; for(int i=1;i<n;i++) if(inv[lab[i]]!=inv[lab[i-1]]) cs[nc++]=i; cs[nc]=n;
  search(lab,cs,nc);
  memcpy(out,best,sizeof(u32)*n);
}
// ---------- hash set of records ----------
typedef struct { u32 *data; u64 cap, cnt; int n; } HS;
static u64 hrec(const u32*r,int n){ u64 h=1469598103934665603ULL; for(int i=0;i<n;i++){ h^=r[i]; h*=1099511628211ULL; h^=h>>29;} return h; }
static void hs_init(HS*h,int n,u64 cap){ h->n=n; h->cap=cap; h->cnt=0; h->data=calloc(cap*n,sizeof(u32)); }
static int hs_ins(HS*h,const u32*r);
static void hs_grow(HS*h){ HS g; hs_init(&g,h->n,h->cap*2); for(u64 i=0;i<h->cap;i++) if(h->data[i*h->n]) hs_ins(&g,h->data+i*h->n); free(h->data); *h=g; }
static int hs_ins(HS*h,const u32*r){ // rows nonzero for regular graphs => row0!=0 marks used
  if(h->cnt*2>h->cap) hs_grow(h);
  u64 i=hrec(r,h->n)&(h->cap-1);
  while(h->data[i*h->n]){ if(!memcmp(h->data+i*h->n,r,sizeof(u32)*h->n)) return 0; i=(i+1)&(h->cap-1); }
  memcpy(h->data+i*h->n,r,sizeof(u32)*h->n); h->cnt++; return 1;
}
static u32 *readall(const char*fn,int n,u64*cnt){
  FILE*f=fopen(fn,"rb"); if(!f){perror(fn);exit(1);} fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
  u32*d=malloc(sz+4); if(fread(d,1,sz,f)!=(size_t)sz){fprintf(stderr,"read err\n");exit(1);} fclose(f); *cnt=sz/(4*n); return d;
}
static int connected(const u32*g,int n){ u32 seen=1,fr=1; while(fr){u32 nf=0; u32 a=fr; while(a){int j=__builtin_ctz(a);a&=a-1; nf|=g[j];} nf&=~seen; seen|=nf; fr=nf;} return seen==((n==32)?0xffffffffu:((1u<<n)-1)); }

// ---------- strong chromatic index ----------
static int M; static u64 H[64]; // L(G)^2 adjacency
static void build_l2(const u32*g,int n){
  int eu[64],ev[64]; M=0;
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(g[i]>>j&1){eu[M]=i;ev[M]=j;M++;}
  for(int a=0;a<M;a++){ H[a]=0; u32 na=g[eu[a]]|g[ev[a]]|(1u<<eu[a])|(1u<<ev[a]);
    for(int b=0;b<M;b++) if(b!=a){ if((na>>eu[b]&1)||(na>>ev[b]&1)) H[a]|=1ULL<<b; } }
}
static int bestw;
static void clq(u64 P,int sz){ if(!P){ if(sz>bestw) bestw=sz; return; }
  if(sz+__builtin_popcountll(P)<=bestw) return;
  while(P){ if(sz+__builtin_popcountll(P)<=bestw) return; int v=__builtin_ctzll(P); P&=P-1; clq(P&H[v],sz+1); } }
static int omega(void){ bestw=0; clq((M==64)?~0ULL:((1ULL<<M)-1),0); return bestw; }
// exact colouring: can we colour with k colours? DSATUR backtracking
static int col[64]; static long long nodes, nodelim;
static int dsat_k(int k,int ncol_used,int ncolored){
  if(ncolored==M) return 1;
  if(++nodes>nodelim) return -1;
  // pick uncoloured vertex with max saturation, tie max degree in uncoloured
  int bv=-1,bs=-1,bd=-1; u64 bforb=0;
  for(int v=0;v<M;v++) if(col[v]<0){ u64 forb=0; u64 a=H[v]; int d=0; while(a){int j=__builtin_ctzll(a);a&=a-1; if(col[j]>=0) forb|=1ULL<<col[j]; else d++;}
    int s=__builtin_popcountll(forb); if(s>bs||(s==bs&&d>bd)){bs=s;bd=d;bv=v;bforb=forb;} }
  if(bs>=k) return 0;
  for(int c=0;c<ncol_used && c<k;c++) if(!(bforb>>c&1)){ col[bv]=c; int r=dsat_k(k,ncol_used,ncolored+1); if(r) {if(r<0){col[bv]=-1;} return r;} col[bv]=-1; }
  if(ncol_used<k){ col[bv]=ncol_used; int r=dsat_k(k,ncol_used+1,ncolored+1); if(r){ if(r<0) col[bv]=-1; return r;} col[bv]=-1; }
  return 0;
}
static int colorable(int k){ for(int i=0;i<M;i++) col[i]=-1; nodes=0; return dsat_k(k,0,0); }
static int greedy_dsatur(void){ for(int i=0;i<M;i++) col[i]=-1; int used=0;
  for(int it=0;it<M;it++){ int bv=-1,bs=-1,bd=-1; u64 bforb=0;
    for(int v=0;v<M;v++) if(col[v]<0){ u64 forb=0,a=H[v]; int d=0; while(a){int j=__builtin_ctzll(a);a&=a-1; if(col[j]>=0) forb|=1ULL<<col[j]; else d++;}
      int s=__builtin_popcountll(forb); if(s>bs||(s==bs&&d>bd)){bs=s;bd=d;bv=v;bforb=forb;} }
    int c=__builtin_ctzll(~bforb); col[bv]=c; if(c+1>used) used=c+1; }
  return used; }

int main(int argc,char**argv){
  if(argc<2){fprintf(stderr,"usage\n");return 1;}
  if(!strcmp(argv[1],"expand")){ // expand in n_in out wid nw
    const char*in=argv[2]; int n=atoi(argv[3]); const char*out=argv[4]; int wid=atoi(argv[5]),nw=atoi(argv[6]);
    u64 cnt; u32*d=readall(in,n,&cnt); int OP=getenv("OP")?atoi(getenv("OP")):0; int n2=(OP==3)?n:(OP==4)?n+5:n+1+(OP==1?1:0)+(OP==2?2:0); HS h; hs_init(&h,n2,1<<16);
    for(u64 r=wid;r<cnt;r+=nw){ u32*g=d+r*n; int eu[64],ev[64],m=0;
      for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(g[i]>>j&1){eu[m]=i;ev[m]=j;m++;}
      if(OP==3){ // double-edge switch: ab,cd -> ac,bd and ad,bc (same n)
        for(int a=0;a<m;a++) for(int b=a+1;b<m;b++){ int p=eu[a],q=ev[a],r=eu[b],t=ev[b];
          if(p==r||p==t||q==r||q==t) continue;
          for(int o=0;o<2;o++){ int x1=p,y1=(o?r:t), x2=q,y2=(o?t:r); // new edges x1y1, x2y2
            if((g[x1]>>y1&1)||(g[x2]>>y2&1)) continue;
            u32 ng[MAXN]; memcpy(ng,g,sizeof(u32)*n);
            ng[p]&=~(1u<<q); ng[q]&=~(1u<<p); ng[r]&=~(1u<<t); ng[t]&=~(1u<<r);
            ng[x1]|=1u<<y1; ng[y1]|=1u<<x1; ng[x2]|=1u<<y2; ng[y2]|=1u<<x2;
            u32 c[MAXN]; canon(ng,n,c); hs_ins(&h,c); } }
        continue; }
      if(OP==4){ // edge xy -> x-p, y-q with {p,q,r,s,t}=K5 minus pq
        for(int e=0;e<m;e++){ int x=eu[e],y=ev[e]; u32 ng[MAXN]; memcpy(ng,g,sizeof(u32)*n);
          ng[x]&=~(1u<<y); ng[y]&=~(1u<<x); int p=n,q=n+1; u32 K=0; for(int i=0;i<5;i++) K|=1u<<(n+i);
          for(int i=0;i<5;i++) ng[n+i]=K&~(1u<<(n+i));
          ng[p]&=~(1u<<q); ng[q]&=~(1u<<p); ng[p]|=1u<<x; ng[x]|=1u<<p; ng[q]|=1u<<y; ng[y]|=1u<<q;
          u32 c[MAXN]; canon(ng,n2,c); hs_ins(&h,c); }
        continue; }
      if(OP==1){ // triangle xyz -> delete its edges, add adjacent twins v,w joined to x,y,z
        for(int x=0;x<n;x++) for(int y=x+1;y<n;y++) if(g[x]>>y&1) for(int z=y+1;z<n;z++) if((g[x]>>z&1)&&(g[y]>>z&1)){
          u32 ng[MAXN]; memcpy(ng,g,sizeof(u32)*n); int v=n,w=n+1;
          ng[x]&=~((1u<<y)|(1u<<z)); ng[y]&=~((1u<<x)|(1u<<z)); ng[z]&=~((1u<<x)|(1u<<y));
          u32 T=(1u<<x)|(1u<<y)|(1u<<z); ng[v]=T|(1u<<w); ng[w]=T|(1u<<v);
          ng[x]|=(1u<<v)|(1u<<w); ng[y]|=(1u<<v)|(1u<<w); ng[z]|=(1u<<v)|(1u<<w);
          u32 c[MAXN]; canon(ng,n2,c); hs_ins(&h,c); }
        continue; }
      if(OP==2){ // vertex x -> K4, each K4 vertex takes one old neighbour of x
        for(int x=0;x<n;x++){ int nb[4],k=0; u32 a=g[x]; while(a){nb[k++]=__builtin_ctz(a);a&=a-1;}
          u32 ng[MAXN]; memcpy(ng,g,sizeof(u32)*n); // reuse slot x as one K4 vertex
          int q[4]={x,n,n+1,n+2}; u32 K=0; for(int i=0;i<4;i++) K|=1u<<q[i];
          for(int i=0;i<4;i++){ ng[nb[i]]&=~(1u<<x); }
          for(int i=0;i<4;i++){ ng[q[i]]=(K&~(1u<<q[i]))|(1u<<nb[i]); ng[nb[i]]|=1u<<q[i]; }
          u32 c[MAXN]; canon(ng,n2,c); hs_ins(&h,c); }
        continue; }
      for(int a=0;a<m;a++) for(int b=a+1;b<m;b++){
        if(eu[a]==eu[b]||eu[a]==ev[b]||ev[a]==eu[b]||ev[a]==ev[b]) continue;
        u32 ng[MAXN]; memcpy(ng,g,sizeof(u32)*n);
        ng[eu[a]]&=~(1u<<ev[a]); ng[ev[a]]&=~(1u<<eu[a]); ng[eu[b]]&=~(1u<<ev[b]); ng[ev[b]]&=~(1u<<eu[b]);
        int v=n; ng[v]=(1u<<eu[a])|(1u<<ev[a])|(1u<<eu[b])|(1u<<ev[b]);
        ng[eu[a]]|=1u<<v; ng[ev[a]]|=1u<<v; ng[eu[b]]|=1u<<v; ng[ev[b]]|=1u<<v;
        u32 c[MAXN]; canon(ng,n2,c); hs_ins(&h,c);
      } }
    FILE*f=fopen(out,"wb"); for(u64 i=0;i<h.cap;i++) if(h.data[i*n2]) fwrite(h.data+i*n2,4,n2,f); fclose(f);
    fprintf(stderr,"worker %d: %llu unique\n",wid,(unsigned long long)h.cnt); return 0; }
  if(!strcmp(argv[1],"merge")){ // merge n out in1 in2 ...  (also canonicalises: pass "recanon" via env)
    int n=atoi(argv[2]); const char*out=argv[3]; HS h; hs_init(&h,n,1<<20); int rc=getenv("RECANON")!=NULL; u64 tot=0;
    for(int a=4;a<argc;a++){ u64 cnt; u32*d=readall(argv[a],n,&cnt); tot+=cnt; for(u64 r=0;r<cnt;r++){ if(rc){u32 c[MAXN]; canon(d+r*n,n,c); hs_ins(&h,c);} else hs_ins(&h,d+r*n);} free(d);} 
    FILE*f=fopen(out,"wb"); u64 con=0; for(u64 i=0;i<h.cap;i++) if(h.data[i*n]){ fwrite(h.data+i*n,4,n,f); con+=connected(h.data+i*n,n);} fclose(f);
    printf("n=%d total_unique=%llu connected=%llu disconnected=%llu (input recs %llu)\n",n,(unsigned long long)h.cnt,(unsigned long long)con,(unsigned long long)(h.cnt-con),(unsigned long long)tot); return 0; }
  if(!strcmp(argv[1],"sq")){ // sq in n wid nw outprefix : histogram of exact sq over CONNECTED graphs
    const char*in=argv[2]; int n=atoi(argv[3]); int wid=atoi(argv[4]),nw=atoi(argv[5]); const char*outp=argv[6];
    int THR=getenv("THRESH")?atoi(getenv("THRESH")):0;
    nodelim = getenv("NODELIM")?atoll(getenv("NODELIM")):2000000;
    u64 cnt; u32*d=readall(in,n,&cnt); long long hist[80]={0}; long long gap=0, hard=0; int maxsq=0;
    char fn[512]; snprintf(fn,512,"%s.w%d.txt",outp,wid); FILE*fo=fopen(fn,"w");
    for(u64 r=wid;r<cnt;r+=nw){ u32*g=d+r*n; if(!connected(g,n)) continue;
      build_l2(g,n); int U=greedy_dsatur(); if(U<=THR){ hist[0]++; continue; } int w=omega(); int chi;
      if(U==w) chi=w; else { gap++; chi=U; // find smallest k colourable, from w upward
        int k; for(k=w;k<U;k++){ int rr=colorable(k); if(rr<0){ hard++; fprintf(fo,"HARD %llu k=%d w=%d U=%d\n",(unsigned long long)r,k,w,U); chi=-1; break;} if(rr==1){chi=k;break;} }
      }
      if(chi<0) continue;
      hist[chi]++; if(chi>maxsq) maxsq=chi;
      if(chi>=atoi(getenv("REPORT")?getenv("REPORT"):"99")){ fprintf(fo,"G %llu sq=%d omega=%d rows",(unsigned long long)r,chi,w); for(int i=0;i<n;i++) fprintf(fo," %u",g[i]); fprintf(fo,"\n"); }
    }
    fprintf(fo,"SUMMARY gap=%lld hard=%lld max=%d hist",gap,hard,maxsq); for(int i=0;i<80;i++) if(hist[i]) fprintf(fo," %d:%lld",i,hist[i]); fprintf(fo,"\n"); fclose(fo); return 0; }
  return 1;
}
