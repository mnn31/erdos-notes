// Exhaustive check of f_1(n;k,l) for all k<=n, all l=0..C(k,2)+1, small n.
// f_1(n;k,l) = least m such that every graph on [n] with exactly m edges has a k-set spanning >= l edges
// (equivalently contains some k-vertex l-edge graph as a not-necessarily-induced subgraph).
// Computed two independent ways:
//   (A) directly from the definition: minD[k][m] = min over graphs with m edges of D_k(G),
//       D_k(G) = max #edges spanned by a k-set; f = least m with (m > C(n,2) or minD[k][m] >= l).
//   (B) via Lemma 1: f = 1 + M, M = max #edges of a graph all of whose k-sets span <= l-1 edges.
// Then checks (A)==(B), strict increase of l -> f on 0..C(k,2)+1 (Theorem), and prints the table.
// Usage: f1_all n   (n <= 8)
#include <stdio.h>
#include <stdlib.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]);
  int E=n*(n-1)/2, eu[64],ev[64],c=0;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){eu[c]=i;ev[c]=j;c++;}
  static unsigned int sm[9][256]; int ns[9]={0};
  for(int s=0;s<(1<<n);s++){ int k=__builtin_popcount(s);
    unsigned int m=0; for(int e=0;e<E;e++) if(((s>>eu[e])&1)&&((s>>ev[e])&1)) m|=1u<<e;
    sm[k][ns[k]++]=m; }
  static int minD[9][40], maxE[9][40];
  for(int k=0;k<=n;k++) for(int x=0;x<40;x++){minD[k][x]=1000; maxE[k][x]=-1;}
  for(unsigned long long g=0; g<(1ULL<<E); g++){
    int e=__builtin_popcountll(g);
    for(int k=0;k<=n;k++){
      int D=0; for(int i=0;i<ns[k];i++){int t=__builtin_popcount((unsigned)g&sm[k][i]); if(t>D)D=t;}
      if(D<minD[k][e]) minD[k][e]=D;
      if(e>maxE[k][D]) maxE[k][D]=e;
    }
  }
  int bad=0;
  for(int k=0;k<=n;k++){
    int kk=k*(k-1)/2; int prev=-1;
    printf("n=%d k=%d f1(l), l=0..%d:",n,k,kk+1);
    for(int l=0;l<=kk+1;l++){
      int fA=-1; for(int m=0;;m++){ if(m>E || minD[k][m]>=l){fA=m;break;} }
      int M=-1; for(int d=0;d<l;d++) if(maxE[k][d]>M) M=maxE[k][d];
      int fB=M+1;
      if(fA!=fB){printf(" [MISMATCH A=%d B=%d]",fA,fB);bad++;}
      if(fA<=prev){printf(" [NOT STRICT at l=%d]",l);bad++;}
      prev=fA; printf(" %d",fA);
    }
    printf("\n");
  }
  printf("n=%d: %s\n",n,bad?"FAILURES":"all checks passed (A==B, strictly increasing on 0..C(k,2)+1 for every k<=n)");
  return bad;
}
