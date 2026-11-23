/* Least n-shifts for E = {m >= 1 : m = x^2 + y^2}.
   t >= 1 is an n-shift if for all 1 <= a <= n:  a in E  <=>  a+t in E.
   usage: lshift NMAX XMAX Q0 NSTART TSTART
   Scans t in [TSTART, XMAX] in increasing order and prints, for each n in [NSTART, NMAX],
   the least n-shift t_n >= TSTART (t_n is nondecreasing in n), or "none <= XMAX".
   Exclusion of a t uses only NECESSARY conditions (see WRITEUP, Lemma C1):
     (i)  q = 3 mod 4 prime, a in E, a <= n  =>  v_q(a+t) even;
     (ii) a in E  =>  oddpart(a+t) = 1 mod 4.
   Every surviving t is then tested exactly with isE() for all a <= n. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;

static int *pr; static int npr;
static void mkprimes(int L){ char *s=calloc(L+1,1); pr=malloc(sizeof(int)*(L/2+10)); npr=0;
  for(int i=2;i<=L;i++){ if(!s[i]){pr[npr++]=i; for(long long j=(long long)i*i;j<=L;j+=i) s[j]=1;} } free(s);}
static u64 mulmod(u64 a,u64 b,u64 m){return (u128)a*b%m;}
static u64 powmod(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static int isprime64(u64 n){ if(n<2)return 0; static const u64 B[]={2,3,5,7,11,13,17,19,23,29,31,37};
  for(int i=0;i<12;i++){if(n%B[i]==0)return n==B[i];}
  u64 d=n-1;int s=0;while(!(d&1)){d>>=1;s++;}
  for(int i=0;i<12;i++){u64 x=powmod(B[i],d,n); if(x==1||x==n-1)continue; int ok=0;
    for(int r=1;r<s;r++){x=mulmod(x,x,n); if(x==n-1){ok=1;break;}} if(!ok)return 0;} return 1;}
static u64 gcdu(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static u64 rho(u64 n){ for(u64 c=1;;c++){ u64 x=2,y=2,d=1; while(d==1){x=(mulmod(x,x,n)+c)%n; y=(mulmod(y,y,n)+c)%n; y=(mulmod(y,y,n)+c)%n; d=gcdu(x>y?x-y:y-x,n);} if(d!=n)return d; } }
static u64 isqrt64(u64 m){u64 r=(u64)sqrtl((long double)m); while(r*r>m)r--; while((r+1)*(r+1)<=m)r++; return r;}
/* exact membership in E for 1 <= m < 2^62 */
static int isE(u64 m){
  while(!(m&1)) m>>=1;
  int i;
  for(i=1;i<npr;i++){ u64 p=pr[i]; if(p*p*p>m)break;
    if(m%p==0){int e=0; while(m%p==0){m/=p;e++;} if((p&3)==3 && (e&1)) return 0;} }
  if(i>=npr){ fprintf(stderr,"prime table too small\n"); exit(2);}
  if(m==1) return 1;
  /* now every prime factor of m exceeds p, and p^3 > m: m has at most 2 prime factors */
  if(isprime64(m)) return (m&3)==1;
  u64 r=isqrt64(m); if(r*r==m) return 1;            /* m = q^2 */
  if((m&3)==3) return 0;                            /* m = q1*q2 with exactly one = 3 mod 4 */
  u64 d=rho(m); return (d&3)==1;                    /* m = q1*q2, both 1 or both 3 mod 4 */
}
static int NMAX; static char Etab[4096];
/* largest L <= NMAX such that t is an L-shift (0 if fails at a=1) */
static int Lof(u64 t){ for(int a=1;a<=NMAX;a++){ if(isE(t+a)!=Etab[a]) return a-1;} return NMAX; }

/* local allowed residues mod q^e for prime q, given n */
static int vq(u64 m,u64 q){int v=0;while(m%q==0){m/=q;v++;}return v;}
static u64 *allowed_local(int n,u64 q,int e,u64 *mod,int *cnt){
  u64 M=1; for(int j=0;j<e;j++) M*=q; *mod=M; u64 *res=malloc(sizeof(u64)*M); int c=0;
  for(u64 r=0;r<M;r++){ int ok=1;
    for(int a=1;a<=n && ok;a++){ if(!Etab[a])continue; u64 m=(r+a)%M; if(m==0)continue; int v=vq(m,q);
      if(q==2){ if(v<=e-2){ u64 o=(m>>v)&3; if(o!=1) ok=0; } }
      else { if(v&1) ok=0; } }
    if(ok) res[c++]=r; }
  *cnt=c; return res; }
static int cmpu(const void*x,const void*y){u64 a=*(u64*)x,b=*(u64*)y;return a<b?-1:a>b;}
static long long inv_mod(long long a,long long m){ long long g=m,x=0,x1=1,a1=a%m; if(a1<0)a1+=m; long long b=a1;
  long long old_r=b,r=m,old_s=1,s=0; while(r){long long qq=old_r/r,t=old_r-qq*r;old_r=r;r=t;t=old_s-qq*s;old_s=s;s=t;} (void)g;(void)x;(void)x1;
  old_s%=m; if(old_s<0)old_s+=m; return old_s; }

int main(int argc,char**argv){
  if(argc<6){fprintf(stderr,"usage: lshift NMAX XMAX Q0 NSTART TSTART\n");return 1;}
  NMAX=atoi(argv[1]); u64 XMAX=strtoull(argv[2],0,10); int Q0=atoi(argv[3]); int ncur=atoi(argv[4]); u64 tlo=strtoull(argv[5],0,10);
  mkprimes(2200000);
  for(int a=1;a<=NMAX;a++) Etab[a]=isE(a);
  /* sieve primes q = 3 mod 4, q <= Q0, excluding wheel primes 3,7,11 */
  int *Q=malloc(sizeof(int)*npr); int nq=0; for(int i=0;i<npr && pr[i]<=Q0;i++) if((pr[i]&3)==3 && pr[i]!=3 && pr[i]!=7 && pr[i]!=11) Q[nq++]=pr[i];
  while(ncur<=NMAX){
    /* wheel: 2^e2 * 3^e3 * 7^e7 * 11^e11 */
    int e2=3; while((1LL<<(e2-3))<=ncur) e2++;      /* 2^(e2-3) > n */
    int e3=1; {u64 m=3; while(m<=(u64)ncur){m*=3;e3++;}} e3++;
    int e7=1; {u64 m=7; while(m<=(u64)ncur){m*=7;e7++;}} 
    int e11=1; {u64 m=11; while(m<=(u64)ncur){m*=11;e11++;}}
    u64 m2,m3,m7,m11; int c2,c3,c7,c11;
    u64 *A2=allowed_local(ncur,2,e2,&m2,&c2), *A3=allowed_local(ncur,3,e3,&m3,&c3), *A7=allowed_local(ncur,7,e7,&m7,&c7), *A11=allowed_local(ncur,11,e11,&m11,&c11);
    u64 W=m2*m3*m7*m11; long long R=(long long)c2*c3*c7*c11;
    u64 *res=malloc(sizeof(u64)*R); long long k=0;
    for(int i2=0;i2<c2;i2++)for(int i3=0;i3<c3;i3++)for(int i7=0;i7<c7;i7++)for(int i11=0;i11<c11;i11++){
      /* CRT */
      u64 r=0; u64 mods[4]={m2,m3,m7,m11}; u64 vals[4]={A2[i2],A3[i3],A7[i7],A11[i11]};
      for(int j=0;j<4;j++){ u64 Mj=W/mods[j]; u64 inv=(u64)inv_mod((long long)(Mj%mods[j]),(long long)mods[j]); r=(r+ (u64)((u128)vals[j]*inv%mods[j]*Mj % W))%W; }
      res[k++]=r; }
    qsort(res,R,sizeof(u64),cmpu);
    int S[4096],ns=0; for(int a=1;a<=ncur;a++) if(Etab[a]) S[ns++]=a;
    fprintf(stderr,"n=%d W=%llu (2^%d 3^%d 7^%d 11^%d) residues=%lld density=%.3e |S|=%d\n",ncur,W,e2,e3,e7,e11,R,(double)R/W,ns);
    /* precompute W^{-1} mod q */
    long long *Winv=malloc(sizeof(long long)*nq); for(int j=0;j<nq;j++) Winv[j]=inv_mod((long long)(W%Q[j]),Q[j]);
    u64 s=tlo/W; u64 SCHMAX=(u64)(2e12/W)+1; if(SCHMAX>1000000) SCHMAX=1000000; u64 SCH=(tlo>1000000?tlo:1000000)/W+1; if(SCH>SCHMAX) SCH=SCHMAX;
    int found=0;
    char *bad=malloc(SCHMAX+1);
    u64 *cand=NULL; size_t ccap=0;
    while(!found){
      if(W*s > XMAX) break;
      u64 sB=s+SCH; size_t nc=0;
      for(long long ri=0;ri<R;ri++){ u64 r=res[ri]; memset(bad,0,SCH);
        for(int j=0;j<nq;j++){ long long q=Q[j]; long long wi=Winv[j];
          for(int ai=0;ai<ns;ai++){ long long a=S[ai];
            long long s0 = (long long)((u128)((q - (long long)((r + a)%q))%q) * wi % q);  /* W s + r + a = 0 mod q */
            long long st = (long long)(s % q); long long off = s0 - st; if(off<0) off+=q;
            for(u64 x=off; x<SCH; x+=q){ if(bad[x]) continue; u64 t=W*(s+x)+r; u64 m=(t+a)/q; if(m%q) bad[x]=1; }
          } }
        for(u64 x=0;x<SCH;x++) if(!bad[x]){ u64 t=W*(s+x)+r; if(t<tlo||t<1||t>XMAX) continue; if(nc==ccap){ccap=ccap?2*ccap:1024; cand=realloc(cand,ccap*sizeof(u64));} cand[nc++]=t; }
      }
      qsort(cand,nc,sizeof(u64),cmpu);
      for(size_t i=0;i<nc;i++){ u64 t=cand[i]; int L=Lof(t); if(L>=ncur){
          for(int n=ncur;n<=L;n++) printf("t_%d = %llu\n",n,t);
          fflush(stdout); ncur=L+1; tlo=t+1; found=1; break; } }
      fprintf(stderr,"  scanned t < %llu, candidates %zu\n", W*sB, nc);
      s=sB; SCH*=2; if(SCH>SCHMAX) SCH=SCHMAX;
    }
    free(bad); free(Winv); free(res); free(A2);free(A3);free(A7);free(A11);
    if(!found){ printf("t_%d : none <= %llu (so t_%d > %llu)\n",ncur,XMAX,ncur,XMAX); break; }
  }
  return 0;
}
