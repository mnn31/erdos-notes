/* brute.c -- independent upper-bound check for small n (no canonical forms,
 * no degree lemma). Enumerates EVERY labelled graph on n vertices with exactly
 * m edges (all m-subsets of the C(n,2) edges, via Gosper's hack) and decides
 * P(G) by an independent method: for every vertex subset S with |S|>=5 it lists
 * all Hamiltonian cycles of G[S] as edge bitmasks and looks for two disjoint ones.
 * Usage: brute n m   -> prints #graphs with m edges, #P-free among them.
 * By monotonicity (Lemma 1), "#P-free = 0 at m" proves f(n) < m.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int n, ne; static int eu[64], ev[64]; static int eid[16][16];
static uint32_t adj[16];
static uint64_t cyc[200000]; static int ncyc;
static int S_, s0, sz, pth[16];
static void dfs(int u, uint32_t vis, int len, uint64_t em){
    if(len==sz){ if(adj[u]>>s0&1){ uint64_t e=em|(1ULL<<eid[u][s0]);
            if(pth[1]<pth[sz-1]) cyc[ncyc++]=e; } return; }
    uint32_t c=adj[u]&S_&~vis;
    while(c){ int w=__builtin_ctz(c); c&=c-1; pth[len]=w; dfs(w,vis|1u<<w,len+1,em|(1ULL<<eid[u][w])); }
}
static int hasP(void){
    for(uint32_t S=0;S<(1u<<n);S++){
        int k=__builtin_popcount(S); if(k<5) continue;
        int ok=1; for(int x=0;x<n;x++) if(S>>x&1) if(__builtin_popcount(adj[x]&S)<4){ok=0;break;}
        if(!ok) continue;
        S_=S; s0=__builtin_ctz(S); sz=k; ncyc=0; pth[0]=s0;
        dfs(s0,1u<<s0,1,0);
        for(int i=0;i<ncyc;i++) for(int j=i+1;j<ncyc;j++) if(!(cyc[i]&cyc[j])) return 1;
    }
    return 0;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); int m=atoi(argv[2]); ne=0;
    for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ eu[ne]=i; ev[ne]=j; eid[i][j]=eid[j][i]=ne; ne++; }
    uint64_t x=(m==0)?0:((1ULL<<m)-1); uint64_t lim=1ULL<<ne;
    long long tot=0, free_=0;
    while(x<lim){
        for(int i=0;i<n;i++) adj[i]=0;
        for(int e=0;e<ne;e++) if(x>>e&1){ adj[eu[e]]|=1u<<ev[e]; adj[ev[e]]|=1u<<eu[e]; }
        tot++; if(!hasP()) free_++;
        if(m==0) break;
        uint64_t c=x&-x, r=x+c; x=(((r^x)>>2)/c)|r;
    }
    printf("n=%d m=%d labelled_graphs=%lld P_free=%lld\n",n,m,tot,free_);
    return 0;
}
