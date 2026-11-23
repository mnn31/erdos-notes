/* Heuristic search for dense C10-free graphs on N vertices (disproof side).
   A counterexample to R_3(C_10)<=37 via the colour-class route would need a
   C10-free graph on 37 vertices with >= 222 edges (necessary, not sufficient).
   Local search: random edge additions keeping C10-freeness, random removals.
   C10 test for adding uv: is there a u-v path with exactly 9 edges? (exact DFS)
   Usage: ./c10search N seconds seed outfile */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#define MAXN 64
typedef uint64_t u64;
static int N; static u64 adj[MAXN];
static int dist_to_t[MAXN];
static void bfs(int t){ int q[MAXN],h=0,tl=0; for(int i=0;i<N;i++)dist_to_t[i]=99; dist_to_t[t]=0;q[tl++]=t;
  while(h<tl){int x=q[h++]; u64 m=adj[x]; while(m){int y=__builtin_ctzll(m); m&=m-1; if(dist_to_t[y]==99){dist_to_t[y]=dist_to_t[x]+1;q[tl++]=y;}}}}
static int T;
static int dfs(int x,int rem,u64 used){ /* path from x to T with exactly rem more edges, avoiding used */
  if(rem==1) return (adj[x]>>T)&1;
  u64 m=adj[x]&~used&~(1ULL<<T);
  while(m){int y=__builtin_ctzll(m); m&=m-1; if(dist_to_t[y]>rem-1) continue; if(dfs(y,rem-1,used|(1ULL<<y))) return 1;}
  return 0;}
static int path9(int u,int v){ T=v; bfs(v); if(dist_to_t[u]>9) return 0; return dfs(u,9,(1ULL<<u)); }
static int ne(void){int s=0; for(int i=0;i<N;i++) s+=__builtin_popcountll(adj[i]); return s/2;}
int main(int argc,char**argv){
  N=atoi(argv[1]); double secs=atof(argv[2]); unsigned seed=atoi(argv[3]); srand(seed);
  int best=0; u64 bestadj[MAXN]; clock_t t0=clock();
  memset(adj,0,sizeof adj);
  while((double)(clock()-t0)/CLOCKS_PER_SEC<secs){
    /* try additions in random order */
    int improved=1;
    while(improved){ improved=0;
      int order[MAXN*MAXN],k=0; for(int i=0;i<N;i++)for(int j=i+1;j<N;j++) if(!((adj[i]>>j)&1)) order[k++]=i*MAXN+j;
      for(int a=k-1;a>0;a--){int b=rand()%(a+1);int t=order[a];order[a]=order[b];order[b]=t;}
      for(int a=0;a<k;a++){int i=order[a]/MAXN,j=order[a]%MAXN; if((adj[i]>>j)&1) continue;
        if(!path9(i,j)){adj[i]|=1ULL<<j;adj[j]|=1ULL<<i;improved=1;}}
    }
    int e=ne(); if(e>best){best=e; memcpy(bestadj,adj,sizeof adj); fprintf(stderr,"N=%d best=%d t=%.1f\n",N,best,(double)(clock()-t0)/CLOCKS_PER_SEC);}
    /* perturb: remove a few random edges (from current), sometimes restart from best */
    if(rand()%20==0) memcpy(adj,bestadj,sizeof adj);
    int rm=1+rand()%6;
    for(int r=0;r<rm;r++){ int i=rand()%N; if(!adj[i]) continue; int c=__builtin_popcountll(adj[i]); int s=rand()%c; u64 m=adj[i]; for(int q=0;q<s;q++) m&=m-1; int j=__builtin_ctzll(m); adj[i]&=~(1ULL<<j); adj[j]&=~(1ULL<<i);}
  }
  FILE*f=fopen(argv[4],"w"); fprintf(f,"%d %d\n",N,best);
  for(int i=0;i<N;i++)for(int j=i+1;j<N;j++) if((bestadj[i]>>j)&1) fprintf(f,"%d %d\n",i,j);
  fclose(f); printf("N=%d best=%d\n",N,best); return 0;}
