/* Exact verifier: reads "n m" then m edges "u v" (0-based).
   Prints: n, m, min degree, whether 2-connected, and for each length L in [3,Lmax]
   whether the graph contains a cycle of length exactly L (exhaustive DFS:
   a cycle of length L through edge uv exists iff there is a u-v path with L-1 edges
   avoiding the edge uv; DFS with exact BFS-distance pruning, which never prunes a
   feasible branch because dist(y,v) <= remaining length is necessary). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
static int N; static u64 adj[64]; static int D[64]; static int T;
static void bfs(int t,u64 forbid){int q[64],h=0,tl=0;for(int i=0;i<N;i++)D[i]=999;D[t]=0;q[tl++]=t;
 while(h<tl){int x=q[h++];u64 m=adj[x]&~forbid;while(m){int y=__builtin_ctzll(m);m&=m-1;if(D[y]==999){D[y]=D[x]+1;q[tl++]=y;}}}}
static int dfs(int x,int rem,u64 used){ if(rem==1) return (adj[x]>>T)&1;
 u64 m=adj[x]&~used&~(1ULL<<T); while(m){int y=__builtin_ctzll(m);m&=m-1; if(D[y]>rem-1)continue; if(dfs(y,rem-1,used|(1ULL<<y)))return 1;} return 0;}
int main(int argc,char**argv){FILE*f=fopen(argv[1],"r");int Lmax=argc>2?atoi(argv[2]):16;int m;
 if(fscanf(f,"%d %d",&N,&m)!=2)return 1; int cnt=0,u,v; while(fscanf(f,"%d %d",&u,&v)==2){if(!((adj[u]>>v)&1)){adj[u]|=1ULL<<v;adj[v]|=1ULL<<u;cnt++;}}
 int mind=99;for(int i=0;i<N;i++){int d=__builtin_popcountll(adj[i]);if(d<mind)mind=d;}
 int twoconn=1; for(int x=0;x<N;x++){int s=(x==0)?1:0; bfs(s,1ULL<<x); for(int i=0;i<N;i++) if(i!=x&&D[i]==999) twoconn=0;}
 printf("n=%d edges=%d mindeg=%d 2-connected=%s\n",N,cnt,mind,twoconn?"yes":"no");
 printf("cycle lengths present:");
 for(int L=3;L<=Lmax&&L<=N;L++){int found=0;
   for(int a=0;a<N&&!found;a++){u64 mm=adj[a];while(mm&&!found){int b=__builtin_ctzll(mm);mm&=mm-1;if(b<a)continue;
     T=b; bfs(b,0); if(dfs(a,L-1,1ULL<<a)) found=1;}}
   if(found) printf(" %d",L);}
 printf("\n"); return 0;}
