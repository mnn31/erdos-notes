/* independent wheel search: print every t in [TLO,THI] with L(t) >= n0, where only residues class k mod K
   of the wheel residue list are handled. usage: wsearch n0 TLO THI K k */
#include "common.h"
static int Et[100]; static int S[100], ns;
static u64 ipow(u64 q,int k){u64 r=1;while(k--)r*=q;return r;}
static int vq(u64 m,u64 q){int e=0;while(m%q==0){m/=q;e++;}return e;}
/* allowed residues r mod q^k : for all a in S, the q-adic data of r+a, where determined, is compatible with E */
static u64* allowed(u64 q,int k,int *cnt){ u64 M=ipow(q,k); u64 *o=malloc(8*M); int c=0;
  for(u64 r=0;r<M;r++){ int ok=1; for(int i=0;i<ns&&ok;i++){ u64 m=(r+S[i])%M; if(!m) continue; int e=vq(m,q);
      if(q==2){ if(e<=k-2 && ((m>>e)&3)!=1) ok=0; } else if(e&1) ok=0; }
    if(ok) o[c++]=r; } *cnt=c; return o; }
static u64 invm(u64 a,u64 m){ /* a invertible mod m, brute ext gcd */ long long t=0,nt=1; long long r=m,nr=a%m;
  while(nr){ long long qq=r/nr, tmp=t-qq*nt; t=nt; nt=tmp; tmp=r-qq*nr; r=nr; nr=tmp; } if(t<0)t+=m; return (u64)t; }
static int cmp(const void*a,const void*b){u64 x=*(u64*)a,y=*(u64*)b;return x<y?-1:x>y;}
int main(int argc,char**argv){ int n0=atoi(argv[1]); u64 TLO=strtoull(argv[2],0,10), THI=strtoull(argv[3],0,10); int K=atoi(argv[4]), kk=atoi(argv[5]);
  for(int a=1;a<=90;a++) Et[a]=inE(a); ns=0; for(int a=1;a<=n0;a++) if(Et[a]) S[ns++]=a;
  u64 wq[5]={2,3,7,11,19}; int wk[5]={9,5,3,2,2};
  u64 *L=malloc(8); L[0]=0; long long nL=1; u64 M=1;
  for(int j=0;j<5;j++){ int c; u64 *A=allowed(wq[j],wk[j],&c); u64 Q=ipow(wq[j],wk[j]); u64 iv=invm(M%Q,Q);
    if(kk==0) fprintf(stderr,"q=%llu^%d allowed %d/%llu\n",(unsigned long long)wq[j],wk[j],c,(unsigned long long)Q);
    u64 *N=malloc(8*nL*c); long long nn=0;
    for(long long i=0;i<nL;i++) for(int b=0;b<c;b++){ u64 r=L[i]; u64 d=((A[b]%Q)+Q-(r%Q))%Q; u64 x=r+M*mm(d,iv,Q); N[nn++]=x; }
    free(L); L=N; nL=nn; M*=Q; free(A); }
  qsort(L,nL,8,cmp);
  /* sanity: each residue satisfies the CRT system */
  if(kk==0) fprintf(stderr,"W=%llu residues=%lld\n",(unsigned long long)M,nL);
  /* sieve primes */
  int qs[600]; int nq=0; for(int q=23;q<=3000;q+=4){ int p=1; for(int d=2;d*d<=q;d++) if(q%d==0){p=0;break;} if(p) qs[nq++]=q; }
  uint8_t **tab=malloc(sizeof(void*)*nq); u64 tm[600];
  for(int j=0;j<nq;j++){ u64 q=qs[j]; u64 T = q<=250 ? q*q : q; tm[j]=T; tab[j]=calloc(T,1);
    for(u64 r=0;r<T;r++) for(int i=0;i<ns;i++){ u64 m=(r+S[i])%T; if(T==q*q){ if(m%q==0 && m!=0) tab[j][r]=1; } else { if(m==0) tab[j][r]=1; } } }
  long long surv=0, tested=0, hits=0;
  for(long long i=kk;i<nL;i+=K){ u64 r=L[i]; u64 s0 = TLO> r ? (TLO-r+M-1)/M : 0;
    for(u64 s=s0;;s++){ u64 t=M*s+r; if(t>THI) break; if(t<TLO||t==0) continue; tested++;
      int dead=0;
      for(int j=0;j<nq && !dead;j++){ u64 q=qs[j]; u64 x=t%tm[j]; if(!tab[j][x]) continue;
        if(tm[j]==q*q){ dead=1; break; }
        for(int a=0;a<ns;a++){ u64 m=t+S[a]; if(m%q==0 && (m/q)%q!=0){dead=1;break;} } }
      if(dead) continue; surv++;
      int Lt=0; while(Lt<80 && inE(t+Lt+1)==Et[Lt+1]) Lt++;
      if(Lt>=n0){ hits++; printf("%llu %d\n",(unsigned long long)t,Lt); fflush(stdout);} } }
  fprintf(stderr,"k=%d tested=%lld survivors=%lld hits=%lld\n",kk,tested,surv,hits);
  return 0; }
