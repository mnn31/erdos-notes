/* shiftsearch.c -- for t in [TLO, THI), compute the largest n <= NMAX such that
   a in E  <=>  a+t in E  for all 1 <= a <= n   (E = sums of two squares),
   and print, for each n, the first t in the range achieving it.
   E-membership of m via: m in E iff v_q(m) even for all primes q = 3 mod 4.
   Segmented: divide out all q = 3 mod 4 with q <= sqrt(max m) (tracking parity of v_q),
   strip powers of 2; the remaining odd cofactor is a product of primes = 1 mod 4 and at most
   one prime q = 3 mod 4 above sqrt(max m) (two such would exceed max m). So it is = 3 mod 4
   iff such a prime is present (to the first power).
   usage: shiftsearch TLO THI NMAX */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
static int inE_small(u64 m){ /* direct, for the pattern */
  for(u64 q=3;q*q<=m;q+=2){ int v=0; while(m%q==0){m/=q;v++;} if((q%4==3)&&(v&1)) return 0; }
  while(m%2==0) m/=2; return (m%4)!=3; }
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 1;}
  u64 TLO=strtoull(argv[1],0,10), THI=strtoull(argv[2],0,10); int NMAX=atoi(argv[3]);
  u64 MAXM=THI+NMAX+1; u64 SQ=(u64)sqrtl((long double)MAXM)+2;
  /* primes up to SQ */
  char*comp=calloc(SQ+1,1); u64*qs=malloc(sizeof(u64)*(SQ/2+10)); size_t nq=0;
  for(u64 i=2;i<=SQ;i++){ if(!comp[i]){ if(i%4==3) qs[nq++]=i; for(u64 j=i*i;j<=SQ;j+=i) comp[j]=1; } }
  char P[1024]; for(int a=1;a<=NMAX;a++) P[a]=inE_small(a);
  const u64 S=1u<<22; u64*rem=malloc(sizeof(u64)*(S+NMAX+2)); unsigned char*odd=malloc(S+NMAX+2); unsigned char*Eb=malloc(S+NMAX+2);
  u64 first[1024]; for(int i=0;i<=NMAX;i++) first[i]=0; int curmax=0;
  for(u64 lo=TLO; lo<THI; lo+=S){
    u64 hi = lo+S<THI? lo+S: THI;           /* t in [lo,hi) */
    u64 L=lo+1, R=hi-1+NMAX;                 /* m in [L,R] */
    u64 len=R-L+1;
    for(u64 i=0;i<len;i++){ rem[i]=L+i; odd[i]=0; }
    for(size_t k=0;k<nq;k++){ u64 q=qs[k]; if(q*q>R) break;
      u64 st=((L+q-1)/q)*q;
      for(u64 m=st;m<=R;m+=q){ u64 i=m-L; int v=0; u64 r=rem[i]; do{ r/=q; v++; }while(r%q==0); rem[i]=r; if(v&1) odd[i]=1; }
    }
    for(u64 i=0;i<len;i++){ u64 r=rem[i]; r>>=__builtin_ctzll(r); Eb[i]=(!odd[i])&&((r&3)!=3); }
    for(u64 t=lo;t<hi;t++){ u64 base=t-L; /* index of m=t+a is base+a */
      if(t==0) continue;
      int a=1; while(a<=NMAX && Eb[base+a]==P[a]) a++;
      int ml=a-1;
      if(ml>curmax){ for(int n=curmax+1;n<=ml;n++) first[n]=t; curmax=ml; }
    }
  }
  for(int n=1;n<=curmax;n++) printf("%d %llu\n",n,(unsigned long long)first[n]);
  return 0; }
