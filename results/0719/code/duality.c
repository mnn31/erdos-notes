// Erdos 719, n = r+3.  Checks the complement duality (Lemma 1-2 of WRITEUP.md) directly on
// r-graphs G on [n]:  nu(G) [max # pairwise edge-disjoint K_{r+1}^r, computed by brute-force
// packing in the ORIGINAL hypergraph]  ==  matching number of F, where F = pairs A of [n] such
// that every r-set disjoint from A... i.e. all (r+1)-set [n]\A spans a clique.
// Also, mode 'full' (r=3,n=6) enumerates all 2^20 graphs and reports ex and max(m - r*nu).
// usage: duality full            |  duality random r count seed
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int r,n,E,K; static int eid[1<<12]; static u128 cl[64]; static int clA[64][2];
static int best;
static void pack(u128 avail,int start,int cnt){ if(cnt>best)best=cnt; for(int k=start;k<K;k++) if((cl[k]&avail)==cl[k]) pack(avail&~cl[k],k+1,cnt+1);}
static uint32_t adj[16]; static int bm;
static void mm(uint32_t av,int k){ if(k+__builtin_popcount(av)/2<=bm) return; if(!av){bm=k;return;}
  int v=__builtin_ctz(av); uint32_t rest=av&~(1u<<v); uint32_t nb=adj[v]&rest;
  while(nb){int u=__builtin_ctz(nb); nb&=nb-1; mm(rest&~(1u<<u),k+1);} mm(rest,k);}
static int nuF(u128 G){ // F = pairs A whose complement clique is present
  for(int x=0;x<n;x++) adj[x]=0;
  for(int k=0;k<K;k++) if((cl[k]&G)==cl[k]){int a=clA[k][0],b=clA[k][1]; adj[a]|=1u<<b; adj[b]|=1u<<a;}
  bm=0; mm((1u<<n)-1,0); return bm; }
static uint64_t rs; static uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int argc,char**argv){
  int full = argv[1][0]=='f';
  if(full){ r=3; } else r=atoi(argv[2]); n=r+3;
  E=0; for(int s=0;s<(1<<n);s++) if(__builtin_popcount(s)==r) eid[s]=E++;
  K=0; for(int s=0;s<(1<<n);s++) if(__builtin_popcount(s)==r+1){ u128 m=0; for(int x=0;x<n;x++) if(s>>x&1) m|=(u128)1<<eid[s&~(1<<x)];
      int c=((1<<n)-1)&~s; clA[K][0]=__builtin_ctz(c); clA[K][1]=31-__builtin_clz(c); cl[K++]=m; }
  long mism=0, cnt=0;
  if(full){ int ex=0,mx=-1; long viol=0;
    for(uint64_t g=0; g<(1ull<<E); g++){ u128 G=g; int m=__builtin_popcountll(g); best=0; pack(G,0,0);
      if(nuF(G)!=best) mism++; if(best==0&&m>ex) ex=m; if(m-r*best>mx) mx=m-r*best; cnt++; }
    for(uint64_t g=0; g<(1ull<<E); g++){ u128 G=g; int m=__builtin_popcountll(g); best=0; pack(G,0,0); if(m-r*best>ex) viol++; }
    printf("r=3 n=6: graphs=%ld nu(G)!=nu(F) mismatches=%ld ex=%d max(m-3nu)=%d violations=%ld\n",cnt,mism,ex,mx,viol);
    return mism?1:0; }
  long R=atol(argv[3]); rs=strtoull(argv[4],0,10)|1; long hist[8]={0};
  for(long it=0;it<R;it++){ // biased to dense graphs so that cliques exist: delete few random edges
    u128 G=(E==128)?~(u128)0:(((u128)1<<E)-1); int del=rnd()%(E/3+1); if(rnd()%4==0) del=rnd()%E;
    for(int d=0;d<del;d++) G&=~((u128)1<<(rnd()%E));
    best=0; pack(G,0,0); int f=nuF(G); if(f!=best) mism++; hist[best<8?best:7]++; cnt++; }
  printf("r=%d n=%d E=%d K=%d samples=%ld nu(G)!=nu(F) mismatches=%ld  nu histogram:",r,n,E,K,cnt,mism);
  for(int i=0;i<8;i++) printf(" %ld",hist[i]); printf("\n"); return mism?1:0; }
