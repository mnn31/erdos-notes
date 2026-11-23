// Erdos 719, (r,n)=(4,8). Computational checks of every lemma in WRITEUP.md.
// Vertices V={0..7}. Edges of G: 4-subsets (bitmask over 8 bits). 70 of them.
// Usage: ./check48 <mode>
//   mode 1: structural lemmas (XOR SQS(8), extremal graph, Fano lines, uniformity)
//   mode 2: exhaustive, ALL G with t<=TMAX non-edges (arg2=TMAX), computed DIRECTLY in G-language:
//           nu(G) = max number of edge-disjoint K_5^4 copies (exact), check m-4nu<=56,
//           and also check nu equals the dual triple-packing number, and nu >= 7-floor(t/2).
//   mode 3: random + local search over t=6..20 non-edges (arg2 = samples per t, arg3 = seed)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static int E4[70], E5[56], E3[56]; static int id4[256], id3[256];
static u128 cl[56];           // cl[k] = edges (4-sets) of the K_5^4 on 5-set E5[k], as 70-bit mask
static unsigned pairmask[56]; // for triple E3[i]: its 3 pairs as bits in 28-bit pair index
static int pid[8][8]; static unsigned vpairs[8];
static int pc(unsigned x){return __builtin_popcount(x);}
// ---------- exact max packing of edge-disjoint K_5^4 in G (G as 70-bit mask) ----------
static int bestG, targetG; static int candG[56], ncG;
static void packG(u128 avail,int start,int cnt){ if(cnt>bestG)bestG=cnt; if(bestG>=targetG) return; if(cnt+(ncG-start)<=bestG) return;
  for(int i=start;i<ncG;i++){ u128 m=cl[candG[i]]; if((m&avail)==m){ packG(avail&~m,i+1,cnt+1); if(bestG>=targetG) return; } } }
// exact nu (target=99), or stop as soon as `target` edge-disjoint copies are found
static int nuG_t(u128 G,int target){ ncG=0; for(int k=0;k<56;k++) if((cl[k]&G)==cl[k]) candG[ncG++]=k; bestG=0; targetG=target; packG(G,0,0); return bestG; }
static int nuG(u128 G){ return nuG_t(G,99); }
// ---------- exact max packing of triples (pairwise share <=1 point) among full triples ----------
static int bestT; static int candT[56], ncT;
static void packT(unsigned used,int start,int cnt){ if(cnt>bestT)bestT=cnt; if(cnt+(ncT-start)<=bestT) return;
  if(cnt + (28-pc(used))/3 <= bestT) return;
  { int cap=0; for(int x=0;x<8;x++) cap += (7-pc(used & vpairs[x]))/2; if(cnt + cap/3 <= bestT) return; } // each vertex lies in <= floor(free pairs at x / 2) more triples
  for(int i=start;i<ncT;i++){ unsigned m=pairmask[candT[i]]; if(!(m&used)) packT(used|m,i+1,cnt+1);} }
// full triples: A is full iff no non-edge e is disjoint from A
static int nuT(const int *T,int t){ ncT=0; for(int i=0;i<56;i++){ int ok=1; for(int j=0;j<t;j++) if(!(E4[T[j]]&E3[i])){ok=0;break;} if(ok) candT[ncT++]=i;} bestT=0; packT(0,0,0); return bestT; }
static void init(void){ int a=0,b=0,c=0; for(int s=0;s<256;s++){ if(pc(s)==4){id4[s]=a;E4[a++]=s;} if(pc(s)==5)E5[b++]=s; if(pc(s)==3){id3[s]=c;E3[c++]=s;} }
  int p=0; for(int x=0;x<8;x++)for(int y=x+1;y<8;y++){pid[x][y]=pid[y][x]=p++;}
  for(int x=0;x<8;x++){vpairs[x]=0; for(int y=0;y<8;y++) if(y!=x) vpairs[x]|=1u<<pid[x][y];}
  for(int k=0;k<56;k++){ u128 m=0; for(int x=0;x<8;x++) if(E5[k]>>x&1) m|=(u128)1<<id4[E5[k]&~(1<<x)]; cl[k]=m; }
  for(int i=0;i<56;i++){ int v[3],q=0; for(int x=0;x<8;x++) if(E3[i]>>x&1) v[q++]=x; pairmask[i]=(1u<<pid[v[0]][v[1]])|(1u<<pid[v[0]][v[2]])|(1u<<pid[v[1]][v[2]]); } }
static int xorset(int s){ int x=0; for(int v=0;v<8;v++) if(s>>v&1) x^=v; return x; }
static void mode1(void){
  // XOR SQS(8)
  int B[70],nb=0; for(int i=0;i<70;i++) if(xorset(E4[i])==0) B[nb++]=E4[i];
  printf("XOR-zero 4-sets: %d\n",nb);
  int cov[56]; memset(cov,0,sizeof cov); for(int j=0;j<nb;j++) for(int i=0;i<56;i++) if((E3[i]&B[j])==E3[i]) cov[i]++;
  int mn=99,mx=0; for(int i=0;i<56;i++){ if(cov[i]<mn)mn=cov[i]; if(cov[i]>mx)mx=cov[i]; } printf("each triple in min %d max %d XOR-zero 4-sets\n",mn,mx);
  int closed=1; for(int j=0;j<nb;j++) if(xorset(255&~B[j])!=0) closed=0; printf("complement-closed: %d\n",closed);
  // extremal graph G* = 4-sets with nonzero XOR
  u128 Gs=0; int m=0; for(int i=0;i<70;i++) if(xorset(E4[i])!=0){Gs|=(u128)1<<i;m++;}
  int ncl=0; for(int k=0;k<56;k++) if((cl[k]&Gs)==cl[k]) ncl++; printf("G*: edges %d, K_5^4 copies %d, nu %d, m-4nu=%d\n",m,ncl,nuG(Gs),m-4*nuG(Gs));
  // Fano lines {a,b,a^b}, a,b nonzero in F_2^3
  int L[7],nl=0; for(int i=0;i<56;i++){ int s=E3[i]; if(s&1) continue; int v[3],q=0; for(int x=0;x<8;x++) if(s>>x&1) v[q++]=x; if((v[0]^v[1])==v[2]) L[nl++]=s; }
  printf("Fano lines: %d :",nl); for(int i=0;i<nl;i++){ printf(" {"); for(int x=0;x<8;x++) if(L[i]>>x&1) printf("%d",x); printf("}"); } printf("\n");
  int okint=1; for(int i=0;i<nl;i++)for(int j=i+1;j<nl;j++) if(pc(L[i]&L[j])!=1) okint=0; printf("pairwise |Li cap Lj|=1: %d\n",okint);
  // uniformity: over all 8! permutations, each triple is image of a line exactly 7*8!/56 times
  static long cnt[256]; int perm[8]={0,1,2,3,4,5,6,7}; long np=0;
  // iterate permutations (Heap's algorithm, iterative)
  int cidx[8]={0}; 
  #define VISIT { np++; for(int l=0;l<7;l++){ int s=0; for(int x=0;x<8;x++) if(L[l]>>x&1) s|=1<<perm[x]; cnt[s]++; } }
  VISIT; int i=0; while(i<8){ if(cidx[i]<i){ int j=(i%2==0)?0:cidx[i]; int tmp=perm[j];perm[j]=perm[i];perm[i]=tmp; VISIT; cidx[i]++; i=0;} else {cidx[i]=0;i++;} }
  long a=-1; int uni=1; for(int k=0;k<56;k++){ if(a<0)a=cnt[E3[k]]; if(cnt[E3[k]]!=a) uni=0; }
  printf("permutations %ld; each triple is a line-image %ld times (uniform=%d); 7*8!/56=%ld\n",np,a,uni,7L*40320/56);
  // Sum_lines P(sigma(L) subset Q) for a 4-set Q: exact count
  long tot=0; for(int k=0;k<56;k++) if((E3[k]&0x0F)==E3[k]) tot+=cnt[E3[k]];
  printf("for Q={0,1,2,3}: sum over perms of #lines mapped into Q = %ld = 8!/2? %d\n",tot, tot==40320/2);
}
// mode 2: exhaustive over sets of non-edges of size <= TMAX
static long cntt[71]; static int maxdef[71], minnu[71], viol=0, dualmis=0, fanofail=0;
static int Tst[20];
static long directfail=0, directlow=0, directchecked=0; static int tfull=99;
static void rec(int start,int t,int tmax,u128 G){
  int m=70-t; int nut=nuT(Tst,t); int nu=nut;
  // direct G-language check (independent of the duality): find ceil((m-56)/4) edge-disjoint K_5^4 copies
  int need=(m-56>0)?(m-56+3)/4:0; if(nuG_t(G,need)<need) directfail++;
  // direct search must also reach the dual value (direct nu >= dual nu)
  if(t<=tfull){ directchecked++; if(nuG_t(G,nut)<nut) directlow++; }
  if(m-4*nu>56) {viol++; if(viol<5) printf("VIOLATION t=%d\n",t);}
  if(nu < 7 - t/2) fanofail++;
  cntt[t]++; if(m-4*nu>maxdef[t]) maxdef[t]=m-4*nu; if(nu<minnu[t]) minnu[t]=nu;
  if(t==tmax) return;
  for(int e=start;e<70;e++){ Tst[t]=e; rec(e+1,t+1,tmax,G&~((u128)1<<e)); }
}
static void mode2(int tmax){ for(int t=0;t<71;t++){maxdef[t]=-999;minnu[t]=99;} u128 all=(((u128)1)<<70)-1; rec(0,0,tmax,all);
  for(int t=0;t<=tmax;t++) printf("t=%d graphs=%ld min nu=%d max(m-4nu)=%d  (Lemma bound 7-floor(t/2)=%d)\n",t,cntt[t],minnu[t],maxdef[t],7-t/2);
  printf("violations of m-4nu<=56 (dual nu): %d ; direct G-language failures to find ceil((m-56)/4) copies: %ld ; direct search below dual nu: %ld (of %ld graphs checked, t<=%d) ; failures of nu>=7-floor(t/2): %d\n",viol,directfail,directlow,directchecked,tfull,fanofail); }
static u64 rs; static u64 rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static void mode3(long S,u64 seed){ rs=seed?seed:88172645463325252ULL; u128 all=(((u128)1)<<70)-1; long viol=0,mis=0,ff=0;
  for(int t=6;t<=20;t++){ int mn=99, mxd=-999;
    for(long s=0;s<S;s++){ int T[70]; int used[70]={0}; for(int j=0;j<t;j++){ int e; do e=rnd()%70; while(used[e]); used[e]=1; T[j]=e; }
      u128 G=all; for(int j=0;j<t;j++) G&=~((u128)1<<T[j]);
      int nu=nuG(G), nut=nuT(T,t); if(nu!=nut) mis++; if(70-t-4*nu>56) viol++; if(nu<7-t/2 && 7-t/2>0) ff++; if(nu<mn)mn=nu; if(70-t-4*nu>mxd)mxd=70-t-4*nu; }
    // local search: try to minimise nu at fixed t (swap moves), several restarts
    int lsmin=99; for(int rst=0;rst<20;rst++){ int T[70]; int used[70]={0}; for(int j=0;j<t;j++){ int e; do e=rnd()%70; while(used[e]); used[e]=1; T[j]=e; }
      int cur=nuT(T,t); for(int it=0;it<3000;it++){ int j=rnd()%t; int e; do e=rnd()%70; while(used[e]); int old=T[j]; T[j]=e; int v=nuT(T,t);
        if(v<=cur){ used[old]=0; used[e]=1; cur=v; } else T[j]=old; }
      if(cur<lsmin) lsmin=cur; u128 G=all; for(int j=0;j<t;j++) G&=~((u128)1<<T[j]); int nu=nuG(G); if(nu!=cur) mis++; if(70-t-4*nu>56) viol++; if(nu<7-t/2&&7-t/2>0) ff++; }
    printf("t=%2d random samples=%ld: min nu=%d max(m-4nu)=%d ; local-search min nu=%d ; bound 7-floor(t/2)=%d ; need ceil((14-t)/4)=%d\n",t,S,mn,mxd,lsmin,7-t/2,(14-t)>0?(14-t+3)/4:0);
  }
  printf("violations %ld, direct-vs-dual mismatches %ld, Fano-bound failures %ld\n",viol,mis,ff); }
int main(int c,char**v){ init(); int mode=atoi(v[1]); if(mode==1) mode1(); else if(mode==2){ if(c>3) tfull=atoi(v[3]); mode2(atoi(v[2])); } else mode3(atol(v[2]), c>3?strtoull(v[3],0,10):0); return 0; }
