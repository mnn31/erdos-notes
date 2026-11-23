/* segmented factor sieve: E membership for m in [1, N]; then records of L(t) for t <= LIM */
#include "common.h"
int main(int c,char**v){ int N0=atoi(v[2]); u64 LIM=strtoull(v[1],0,10), N=LIM+100; u64 R=1; while(R*R<=N) R++;
  char *comp=calloc(R+1,1); int *P=malloc(sizeof(int)*(R+1)); int np=0;
  for(u64 i=2;i<=R;i++){ if(!comp[i]){P[np++]=i; for(u64 j=i*i;j<=R;j+=i) comp[j]=1;} }
  u64 SEG=1<<22; u64 *rem=malloc(8*SEG); uint8_t *bad=malloc(SEG);
  /* rolling window of E bits: keep E for [base, base+SEG) plus need first 80 values */
  uint8_t *Eall=malloc(N+1); /* 1 byte per m; for 1e9 fine (1 GB) -> use bits instead */
  free(Eall);
  uint8_t *Eb=calloc(N/8+2,1);
  for(u64 lo=1; lo<=N; lo+=SEG){ u64 hi=lo+SEG-1; if(hi>N) hi=N; u64 L=hi-lo+1;
    for(u64 i=0;i<L;i++){ rem[i]=lo+i; bad[i]=0; }
    for(int k=0;k<np;k++){ u64 p=P[k]; if(p*p>hi) break; u64 st=((lo+p-1)/p)*p;
      for(u64 x=st;x<=hi;x+=p){ u64 i=x-lo; int e=0; while(rem[i]%p==0){rem[i]/=p;e++;} if((p&3)==3 && (e&1)) bad[i]=1; } }
    for(u64 i=0;i<L;i++){ u64 r=rem[i]; if(r>1 && (r&3)==3) bad[i]=1; /* leftover prime > sqrt */
      if(!bad[i]){ u64 m=lo+i; Eb[m>>3]|=1<<(m&7);} } }
  #define IN(m) ((Eb[(m)>>3]>>((m)&7))&1)
  int best=0;
  for(u64 t=1;t<=LIM;t++){ int L=0; while(L<80 && IN((u64)L+1)==IN(t+L+1)) L++;
    if(L>=N0) printf("%llu %d\n",(unsigned long long)t,L); if(L>best) best=L; }
  /* spot-check bits against inE() */
  for(u64 m=1;m<=N;m+=99991) if(IN(m)!=inE(m)){ printf("MISMATCH %llu\n",(unsigned long long)m); return 1; }
  printf("brute2: all t <= %llu scanned; max L = %d\n",(unsigned long long)LIM,best); return 0; }
