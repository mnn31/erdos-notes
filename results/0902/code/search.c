/* Exhaustive search for Cayley tournaments Cay(G,S) with Schutte property S_k (k=2,3,4).
   Convention: x -> y iff x^{-1} y in S.  S contains exactly one of {g, g^{-1}} for g != e.
   Lemma 2 (WRITEUP): Cay(G,S) is S_k  iff  for every (k-1)-subset {a_1..a_{k-1}} of G\{e}
   there is t in S with t a_i in S for all i, i.e.  R(a_1) & ... & R(a_{k-1}) != 0 where
   R(a) = { t in S : t a in S }.
   Lemma 3: WLOG g0 in S where g0=(1,0,0) and phi:(x,y,w)->(-x,y,w) is an automorphism
   with phi(g0)=g0^{-1} (checked at run time).
   Usage: search GROUPNAME k nthreads [nohalve] */
#include "groups.h"
#include <pthread.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int K, P, NT, HALVE=1, g0;
static int reps[64], repinv[64];     /* free pairs */
static int perm[MAXN];               /* random order of non-identity elements */
static uint64_t NIDX;
static volatile uint64_t next_chunk=0; static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
static uint64_t total_found=0, total_tested=0; static int best_depth=-1; static u128 best_S=0;
static FILE *fout;
#define CHUNK (1ULL<<16)
#ifndef FOUNDCAP
#define FOUNDCAP 1000
#endif
static int test_S(u128 S, const int *Sl, int *depth){
  u128 R[MAXN];
  for(int ci=0; ci<gn-1; ci++){
    int c=perm[ci]; u128 r=0;
    for(int j=0;j<P;j++){ int t=Sl[j]; if((S>>gmul[t][c])&1) r|=((u128)1)<<t; }
    R[ci]=r; *depth=ci;
    if(!r) return 0;
    if(K>=3) for(int bi=0;bi<ci;bi++){ u128 rb=r&R[bi]; if(!rb) return 0;
      if(K>=4) for(int ai=0;ai<bi;ai++) if(!(rb&R[ai])) return 0; }
  }
  *depth=gn-1; return 1;
}
static void *worker(void *arg){
  (void)arg; int Sl[64]; uint64_t found=0,tested=0; int bd=-1; u128 bS=0;
  for(;;){
    pthread_mutex_lock(&mu); uint64_t st=next_chunk; next_chunk+=CHUNK; pthread_mutex_unlock(&mu);
    if(st>=NIDX) break; uint64_t en=st+CHUNK; if(en>NIDX) en=NIDX;
    for(uint64_t idx=st; idx<en; idx++){
      u128 S=0; int cnt=0;
      if(HALVE){ S|=((u128)1)<<g0; Sl[cnt++]=g0; }
      for(int j=0;j<P-HALVE;j++){ int g=((idx>>j)&1)?reps[j]:repinv[j]; S|=((u128)1)<<g; Sl[cnt++]=g; }
      int depth; int ok=test_S(S,Sl,&depth); tested++;
      if(depth>bd){bd=depth;bS=S;}
      if(ok){ pthread_mutex_lock(&mu);
        if(total_found<FOUNDCAP){ fprintf(fout,"S:"); for(int g=0;g<gn;g++) if((S>>g)&1) fprintf(fout," %d",g); fprintf(fout,"\n"); fflush(fout);} 
        total_found++; pthread_mutex_unlock(&mu); }
    }
  }
  pthread_mutex_lock(&mu); total_tested+=tested; if(bd>best_depth){best_depth=bd;best_S=bS;} pthread_mutex_unlock(&mu);
  return NULL;
}
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 1;}
  int gi=find_group(argv[1]); if(gi<0){fprintf(stderr,"no group\n");return 1;}
  K=atoi(argv[2]); NT=atoi(argv[3]); if(argc>4&&!strcmp(argv[4],"nohalve")) HALVE=0;
  gspec gs=(gi==999)?CUSTOM:GROUPS[gi]; build_group(gs);
  if(gn%2==0){fprintf(stderr,"even order\n");return 1;}
  P=(gn-1)/2;
  /* automorphism phi:(x,y,w)->(-x,y,w) */
  int kd=gs.k*gs.d, phi[MAXN];
  for(int a=0;a<gn;a++){ int x=a/kd, rest=a%kd; phi[a]=((gs.m-x)%gs.m)*kd+rest; }
  for(int a=0;a<gn;a++)for(int b=0;b<gn;b++) if(phi[gmul[a][b]]!=gmul[phi[a]][phi[b]]){fprintf(stderr,"phi not hom\n");return 1;}
  { int seen[MAXN]={0}; for(int a=0;a<gn;a++){ if(seen[phi[a]]){fprintf(stderr,"phi not bij\n");return 1;} seen[phi[a]]=1; } }
  g0=1*kd; if(phi[g0]!=ginv[g0]||g0==ginv[g0]){fprintf(stderr,"phi(g0)!=g0^-1\n");return 1;}
  /* pairs */
  int used[MAXN]={0}; used[0]=1; int np=0;
  if(HALVE){ used[g0]=used[ginv[g0]]=1; }
  for(int g=1;g<gn;g++) if(!used[g]){ if(ginv[g]==g){fprintf(stderr,"involution?\n");return 1;}
    reps[np]=g; repinv[np]=ginv[g]; used[g]=used[ginv[g]]=1; np++; }
  if(np!=P-HALVE){fprintf(stderr,"pair count\n");return 1;}
  NIDX=1ULL<<np;
  /* random permutation of non-identity elements */
  uint64_t s=0x9E3779B97F4A7C15ULL; for(int i=0;i<gn-1;i++) perm[i]=i+1;
  for(int i=gn-2;i>0;i--){ s^=s<<13; s^=s>>7; s^=s<<17; int j=(int)(s%(uint64_t)(i+1)); int t=perm[i];perm[i]=perm[j];perm[j]=t; }
  int mo=0; for(int a=0;a<gn;a++){int o=elt_order(a); if(o>mo)mo=o;}
  char fn[256]; snprintf(fn,sizeof fn,"found_%s_k%d.txt",gs.name,K); fout=fopen(fn,"w");
  printf("group %s n=%d abelian=%d maxorder=%d k=%d halve=%d g0=%d sets=2^%d\n",gs.name,gn,is_abelian(),mo,K,HALVE,g0,np); fflush(stdout);
  pthread_t th[64]; for(int i=0;i<NT;i++) pthread_create(&th[i],NULL,worker,NULL);
  for(int i=0;i<NT;i++) pthread_join(th[i],NULL);
  printf("RESULT group=%s n=%d k=%d tested=%llu found=%llu best_depth=%d/%d best_S:",gs.name,gn,K,(unsigned long long)total_tested,(unsigned long long)total_found,best_depth,gn-1);
  for(int g=0;g<gn;g++) if((best_S>>g)&1) printf(" %d",g); printf("\n");
  fclose(fout); return 0;
}
