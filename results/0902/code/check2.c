/* Independent second implementation (different formulation, no symmetry reduction).
   For every connection set S (all 2^((n-1)/2), no halving), and every 4-set {e,a,b,c}
   (a<b<c, natural order), test In(e)&In(a)&In(b)&In(c) != 0 where
   In(x) = { z : z -> x } = { z : z^{-1} x in S } = { x s^{-1} : s in S }.
   Usage: check2 GROUPNAME nthreads [part nparts]   (optional: only the part-th of nparts equal index ranges) */
#include "groups.h"
#include <pthread.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int P, NT; static int reps[64], repinv[64]; static uint64_t NIDX;
static uint64_t next_chunk=0, total_found=0, total=0; static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
static FILE *fout;
static int test(const int *Sl){
  u128 In[MAXN]; unsigned char have[MAXN]; memset(have,0,sizeof have);
  #define GETIN(x) do{ if(!have[x]){ u128 bm_=0; for(int j_=0;j_<P;j_++) bm_|=((u128)1)<<gmul[x][ginv[Sl[j_]]]; In[x]=bm_; have[x]=1; } }while(0)
  GETIN(0);
  for(int a=1;a<gn;a++){ GETIN(a); u128 ea=In[0]&In[a]; if(!ea) return 0;
    for(int b=a+1;b<gn;b++){ GETIN(b); u128 eab=ea&In[b]; if(!eab) return 0;
      for(int c=b+1;c<gn;c++){ GETIN(c); if(!(eab&In[c])) return 0; } } }
  return 1;
}
static void *worker(void*arg){ (void)arg; int Sl[64]; uint64_t cnt=0;
  for(;;){ pthread_mutex_lock(&mu); uint64_t st=next_chunk; next_chunk+=1ULL<<16; pthread_mutex_unlock(&mu);
    if(st>=NIDX) break; uint64_t en=st+(1ULL<<16); if(en>NIDX) en=NIDX;
    for(uint64_t idx=st;idx<en;idx++){ for(int j=0;j<P;j++) Sl[j]=((idx>>j)&1)?reps[j]:repinv[j]; cnt++;
      if(test(Sl)){ pthread_mutex_lock(&mu); total_found++; fprintf(fout,"S:"); int bits[MAXN]={0}; for(int j=0;j<P;j++) bits[Sl[j]]=1; for(int g=0;g<gn;g++) if(bits[g]) fprintf(fout," %d",g); fprintf(fout,"\n"); pthread_mutex_unlock(&mu);} } }
  pthread_mutex_lock(&mu); total+=cnt; pthread_mutex_unlock(&mu); return NULL; }
int main(int argc,char**argv){ int gi=find_group(argv[1]); if(gi<0) return 1; NT=atoi(argv[2]);
  build_group(gi==999?CUSTOM:GROUPS[gi]); P=(gn-1)/2; int used[MAXN]={0}; used[0]=1; int np=0;
  for(int g=1;g<gn;g++) if(!used[g]){ reps[np]=g; repinv[np]=ginv[g]; used[g]=used[ginv[g]]=1; np++; }
  if(np!=P) return 2; NIDX=1ULL<<P; int part=0,nparts=1; if(argc>4){part=atoi(argv[3]);nparts=atoi(argv[4]);} uint64_t lo=NIDX/nparts*part, hi=NIDX/nparts*(part+1); next_chunk=lo; NIDX=hi;
  char fn[256]; snprintf(fn,sizeof fn,"check2_found_%s_p%dof%d.txt",argv[1],part,nparts); fout=fopen(fn,"w");
  pthread_t th[64]; for(int i=0;i<NT;i++) pthread_create(&th[i],NULL,worker,NULL); for(int i=0;i<NT;i++) pthread_join(th[i],NULL);
  printf("CHECK2 group=%s n=%d part=%d/%d tested=%llu found=%llu\n",argv[1],gn,part,nparts,(unsigned long long)total,(unsigned long long)total_found); fclose(fout); return 0; }
