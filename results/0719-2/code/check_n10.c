// Theorem B sanity test at N=10 (r=6, n=10): for sets T of t 4-subsets (complements of non-edges),
// nu = max packing of full triples (triples inside no member of T) pairwise sharing <=1 point.
// Checks t + 6*nu >= 30 (=C(10,3)/4) and Lemma B2: nu >= 12 - floor(48 t / 120) (b=12 mod-10 packing).
// Usage: ./check_n10 <samples per t> <seed>
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
#define N 10
static int Q[210],T3[120],nq=0,nt=0; static u64 pm[120]; static int pid[N][N]; static u64 vp[N];
static int best,nc,cand[120],cap_;
static void pack(u64 used,int st,int cnt){ if(cnt>best)best=cnt; if(best>=cap_) return; if(cnt+(nc-st)<=best) return;
  int cap=0; for(int x=0;x<N;x++) cap+=((N-1)-__builtin_popcountll(used&vp[x]))/2; if(cnt+cap/3<=best) return;
  for(int i=st;i<nc;i++) if(!(pm[cand[i]]&used)){ pack(used|pm[cand[i]],i+1,cnt+1); if(best>=cap_) return; } }
static int nu(int*T,int t){ nc=0; for(int i=0;i<nt;i++){int ok=1; for(int j=0;j<t;j++) if((T3[i]&Q[T[j]])==T3[i]){ok=0;break;} if(ok)cand[nc++]=i;} best=0; pack(0,0,0); return best;}
// returns min(nu, cap_): the search stops once cap_ disjoint triples are found

static u64 rs=1; static u64 rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
int main(int c,char**v){ long S=atol(v[1]); rs=strtoull(v[2],0,10);
 for(int s=0;s<(1<<N);s++){ if(__builtin_popcount(s)==4)Q[nq++]=s; if(__builtin_popcount(s)==3)T3[nt++]=s; }
 int p=0; for(int x=0;x<N;x++)for(int y=x+1;y<N;y++)pid[x][y]=pid[y][x]=p++;
 for(int x=0;x<N;x++){vp[x]=0;for(int y=0;y<N;y++)if(y!=x)vp[x]|=1ULL<<pid[x][y];}
 for(int i=0;i<nt;i++){int a[3],q=0;for(int x=0;x<N;x++)if(T3[i]>>x&1)a[q++]=x; pm[i]=(1ULL<<pid[a[0]][a[1]])|(1ULL<<pid[a[0]][a[2]])|(1ULL<<pid[a[1]][a[2]]);}
 long viol=0,lf=0;
 for(int t=0;t<=34;t++){ int mn=99; int lb=12-(48*t)/120, need=(30-t)>0?(30-t+5)/6:0; cap_=(lb>need?lb:need)+2;
  for(long s=0;s<S;s++){ int T[210],used[210]={0}; for(int j=0;j<t;j++){int e;do e=rnd()%nq;while(used[e]);used[e]=1;T[j]=e;}
    int n=nu(T,t); if(n<mn)mn=n; if(t+6*n<30)viol++; if(n<12-(48*t)/120)lf++; }
  int lsmin=99; for(int r=0;r<10;r++){ int T[210],used[210]={0}; for(int j=0;j<t;j++){int e;do e=rnd()%nq;while(used[e]);used[e]=1;T[j]=e;}
    int cur=t?nu(T,t):nu(T,0); for(int it=0;it<(t?1500:0);it++){int j=rnd()%t;int e;do e=rnd()%nq;while(used[e]);int old=T[j];T[j]=e;int vv=nu(T,t); if(vv<=cur){used[old]=0;used[e]=1;cur=vv;}else T[j]=old;}
    if(cur<lsmin)lsmin=cur; if(t+6*cur<30)viol++; if(cur<12-(48*t)/120)lf++; }
  printf("t=%2d [values are min(nu,%d)] random min=%d local-search min=%d  lemma bound 12-floor(48t/120)=%d  need ceil((30-t)/6)=%d\n",t,cap_,mn,lsmin,12-(48*t)/120,(30-t)>0?(30-t+5)/6:0); fflush(stdout); }
 printf("violations of t+6nu>=30: %ld ; failures of Lemma B2 bound: %ld\n",viol,lf); }
