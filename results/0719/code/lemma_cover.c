// Erdos 719, n = r+3 (dual s = 3).  Checks the covering lemma (Lemma 4 of WRITEUP.md):
// for every graph F on [N], the explicit construction of the proof produces a set C of
// triples covering every edge of F with |C| <= nu(F)*ceil(N/2), and asserts every structural
// claim used in the proof (U independent; per matching edge either one endpoint has no
// U-neighbour, or both have exactly one, common, U-neighbour).
// usage: lemma_cover exhaustive N      (all 2^C(N,2) graphs, N <= 8)
//        lemma_cover random N count seed
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int N, P; static int pu[512], pv[512];
static uint32_t adj[32];
static int bestk, cur[32][2], best[32][2];
static void mm(uint32_t avail, int k){
  if(k + __builtin_popcount(avail)/2 <= bestk) return;
  if(!avail){ bestk=k; for(int i=0;i<k;i++){best[i][0]=cur[i][0];best[i][1]=cur[i][1];} return; }
  int v=__builtin_ctz(avail); uint32_t rest=avail&~(1u<<v);
  uint32_t nb=adj[v]&rest;
  while(nb){ int u=__builtin_ctz(nb); nb&=nb-1; cur[k][0]=v; cur[k][1]=u; mm(rest&~(1u<<u),k+1); }
  mm(rest,k); // v unmatched
}
static long fails=0, structfail=0, tight=0; static int maxratio_num=0;
static uint32_t C[4096]; static int nc;
static void addtri(int a,int b,int c){ C[nc++]=(1u<<a)|(1u<<b)|(1u<<c); }
static int third(int a,int b){ for(int x=0;x<N;x++) if(x!=a&&x!=b) return x; return -1; }
static void check(void){
  bestk=0; mm((N==32)?0xffffffffu:((1u<<N)-1),0); int k=bestk;
  uint32_t W=0; for(int i=0;i<k;i++) W|=(1u<<best[i][0])|(1u<<best[i][1]);
  uint32_t U=((1u<<N)-1)&~W;
  for(int x=0;x<N;x++) if((U>>x&1) && (adj[x]&U)) { structfail++; return; } // U independent
  nc=0;
  // step 1: all pairs inside W
  int w[32],m=0; for(int x=0;x<N;x++) if(W>>x&1) w[m++]=x;
  for(int j=0;j<m;j++){ int l=j+1; while(l<m){ if(l+1<m){addtri(w[j],w[l],w[l+1]); l+=2;} else {addtri(w[j],w[l],third(w[j],w[l])); l++;} } }
  // step 2: W-U edges
  int uu[32],nu_=0; for(int x=0;x<N;x++) if(U>>x&1) uu[nu_++]=x;
  for(int i=0;i<k;i++){ int a=best[i][0], b=best[i][1]; uint32_t NA=adj[a]&U, NB=adj[b]&U; int hub;
    if(NB==0) hub=a; else if(NA==0) hub=b;
    else { if(!(NA==NB && __builtin_popcount(NA)==1)){ structfail++; return; }
           addtri(a,b,__builtin_ctz(NA)); continue; }
    for(int l=0;l<nu_;l+=2){ if(l+1<nu_) addtri(hub,uu[l],uu[l+1]); else addtri(hub,uu[l],third(hub,uu[l])); }
  }
  int bound=k*((N+1)/2);
  if(nc>bound){ fails++; return; }
  if(nc==bound && k>0) tight++;
  for(int p=0;p<P;p++){ int a=pu[p],b=pv[p]; if(!(adj[a]>>b&1)) continue; int ok=0;
    for(int c=0;c<nc;c++) if((C[c]>>a&1)&&(C[c]>>b&1)){ok=1;break;} if(!ok){ fails++; return; } }
}
static uint64_t rs; static uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int argc,char**argv){
  N=atoi(argv[2]); P=0; for(int a=0;a<N;a++) for(int b=a+1;b<N;b++){pu[P]=a;pv[P]=b;P++;}
  long cnt=0;
  if(argv[1][0]=='e'){
    for(uint64_t g=0; g<(1ull<<P); g++){ for(int x=0;x<N;x++) adj[x]=0;
      for(int p=0;p<P;p++) if(g>>p&1){adj[pu[p]]|=1u<<pv[p]; adj[pv[p]]|=1u<<pu[p];}
      check(); cnt++; }
  } else {
    long R=atol(argv[3]); rs=strtoull(argv[4],0,10)|1;
    for(long it=0; it<R; it++){ for(int x=0;x<N;x++) adj[x]=0;
      int dens = rnd()%101; // edge probability in percent, varies per sample
      int mode = rnd()%3;    // 0: G(N,p); 1: star-ish (few centres); 2: clique on random subset
      if(mode==0){ for(int p=0;p<P;p++) if((int)(rnd()%100)<dens){adj[pu[p]]|=1u<<pv[p]; adj[pv[p]]|=1u<<pu[p];} }
      else if(mode==1){ int c=1+rnd()%3; for(int p=0;p<P;p++) if((pu[p]<c||pv[p]<c) && (int)(rnd()%100)<dens){adj[pu[p]]|=1u<<pv[p]; adj[pv[p]]|=1u<<pu[p];} }
      else { int s=1+rnd()%N; for(int p=0;p<P;p++) if(pu[p]<s&&pv[p]<s && (int)(rnd()%100)<dens+20){adj[pu[p]]|=1u<<pv[p]; adj[pv[p]]|=1u<<pu[p];} }
      // random relabel to avoid structure aligned with labels
      int perm[32]; for(int x=0;x<N;x++) perm[x]=x; for(int x=N-1;x>0;x--){int y=rnd()%(x+1); int t=perm[x];perm[x]=perm[y];perm[y]=t;}
      uint32_t a2[32]; for(int x=0;x<N;x++){ a2[perm[x]]=0; for(int y=0;y<N;y++) if(adj[x]>>y&1) a2[perm[x]]|=1u<<perm[y]; }
      for(int x=0;x<N;x++) adj[x]=a2[x];
      check(); cnt++; }
  }
  printf("N=%d graphs=%ld construction_fail=%ld structural_assert_fail=%ld tight(|C|=k*ceil(N/2))=%ld  [bound k*ceil(N/2) <= k*(N-3) iff N>=6]\n",N,cnt,fails,structfail,tight);
  return (fails||structfail)?1:0;
}
