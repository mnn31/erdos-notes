/* Independent brute force: build E up to LIM+64 by enumerating x^2+y^2 (no factoring, no wheel),
   then for every t <= LIM compute L(t) = largest n with a in E <=> a+t in E for all a <= n,
   and print the record values (least t_n). usage: brute LIM */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int c,char**v){ uint64_t LIM=strtoull(v[1],0,10), N=LIM+70;
  uint8_t *E=calloc(N/8+1,1);
  for(uint64_t x=0;x*x<=N;x++) for(uint64_t y=x;x*x+y*y<=N;y++){uint64_t m=x*x+y*y; E[m>>3]|=1<<(m&7);}
  #define IN(m) ((E[(m)>>3]>>((m)&7))&1)
  int best=0;
  for(uint64_t t=1;t<=LIM;t++){ int L=0; while(L<64 && IN(L+1)==IN(t+L+1)) L++;
    if(L>best){ for(int n=best+1;n<=L;n++) printf("t_%d = %llu\n",n,(unsigned long long)t); best=L; fflush(stdout);} }
  printf("all t <= %llu scanned; max L = %d\n",(unsigned long long)LIM,best); return 0; }
