/* dfs_count.c -- labeled exhaustive count, no symmetry reduction, no use of
 * the vertex-extension lemmas.  Counts the avoiding families of exactly M
 * triples on [n] (n <= 8, so <= 56 triples fit in a uint64).
 * Forbidden 4-sets {A,B,C,D}: A,B disjoint, C,D disjoint, A|B = C|D, {A,B} != {C,D}.
 * Usage: ./dfs_count n M
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, M, NT;
static int tv[64][3];
static uint64_t tmask_v[64];           /* vertex mask of triple */
/* for each triple t, list of 3-sets (as bitmask of triples) completing a forbidden 4-set */
static uint64_t *comp[64]; static int ncomp[64];
static long long count, nodes;

static void rec(int i, uint64_t chosen, uint64_t banned, int k){
  nodes++;
  if(k==M){ count++; return; }
  /* remaining candidates */
  uint64_t rest = (i<64? (~0ULL<<i):0) & ((NT==64)?~0ULL:((1ULL<<NT)-1)) & ~banned;
  if(k+__builtin_popcountll(rest) < M) return;
  if(i==NT) return;
  if(!((banned>>i)&1)){
    /* include triple i: ban any triple that would complete a forbidden 4-set */
    uint64_t nb=banned; uint64_t nc=chosen|(1ULL<<i);
    for(int j=0;j<ncomp[i];j++){
      uint64_t c=comp[i][j];
      uint64_t missing=c&~nc;
      if(__builtin_popcountll(missing)==1) nb|=missing;
    }
    rec(i+1,nc,nb,k+1);
  }
  rec(i+1,chosen,banned|(1ULL<<i),k);
}
int main(int argc,char**argv){
  n=atoi(argv[1]); M=atoi(argv[2]);
  NT=0;
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++){ tv[NT][0]=a;tv[NT][1]=b;tv[NT][2]=c; tmask_v[NT]=(1ULL<<a)|(1ULL<<b)|(1ULL<<c); NT++; }
  for(int t=0;t<NT;t++){ comp[t]=malloc(sizeof(uint64_t)*4096); ncomp[t]=0; }
  /* enumerate unordered pairs of distinct disjoint pairs {A,B},{C,D} with same union */
  for(int A=0;A<NT;A++)for(int B=A+1;B<NT;B++){ if(tmask_v[A]&tmask_v[B]) continue;
    for(int C=0;C<NT;C++)for(int D=C+1;D<NT;D++){ if(tmask_v[C]&tmask_v[D]) continue;
      if((tmask_v[A]|tmask_v[B])!=(tmask_v[C]|tmask_v[D])) continue;
      if(A==C&&B==D) continue;
      if(A>C || (A==C && B>D)) continue;   /* each unordered pair of partitions once */
      int q[4]={A,B,C,D};
      for(int s=0;s<4;s++){ uint64_t m=0; for(int r=0;r<4;r++) if(r!=s) m|=1ULL<<q[r]; comp[q[s]][ncomp[q[s]]++]=m; }
    }
  }
  rec(0,0,0,0);
  printf("n=%d M=%d labeled avoiding families of size exactly M: %lld (nodes %lld)\n",n,M,count,nodes);
  return 0;
}
