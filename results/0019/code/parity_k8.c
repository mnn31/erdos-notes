/* Exhaustive check (Lemma 3, c=8, and analogues c=4,6):
   Let K_c sit on vertices 0..c-1 inside a vertex set of size c+2t.
   For every set F of at most t extra edges (edges of K_{c+2t} not inside K_c),
   check whether K_c + F has ALL vertex degrees even.
   Lemma 3 predicts: never, as long as t <= c-1.
   c+2t vertices suffice: t edges touch at most 2t vertices outside K_c. */
#include <stdio.h>
#include <stdlib.h>
static int c, t, N, ne, eu[400], ev[400], deg[64];
static long long checked = 0, found = 0;
static int odd_count;
static void flip(int v){ deg[v]^=1; odd_count += deg[v]?1:-1; }
static void rec(int start, int depth){
  checked++;
  if(odd_count==0){ found++; }
  if(depth==t) return;
  for(int i=start;i<ne;i++){
    flip(eu[i]); flip(ev[i]);
    rec(i+1, depth+1);
    flip(eu[i]); flip(ev[i]);
  }
}
int main(int argc,char**argv){
  c=atoi(argv[1]); t=atoi(argv[2]); N=c+2*t; ne=0; odd_count=0;
  for(int u=0;u<N;u++) for(int v=u+1;v<N;v++) if(!(u<c && v<c)){ eu[ne]=u; ev[ne]=v; ne++; }
  for(int v=0;v<N;v++){ deg[v]=0; }
  for(int v=0;v<c;v++){ if((c-1)&1) flip(v); }   /* degree c-1 in K_c */
  rec(0,0);
  printf("c=%d t=%d N=%d candidate_extra_edges=%d edge_sets_checked=%lld all_even_found=%lld\n",
         c,t,N,ne,checked,found);
  return 0;
}
