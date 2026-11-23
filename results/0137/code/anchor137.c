// Erdos #137 anchor search.
// Claim searched: for k in {3,4,5,6,7,10,11}, is n(n+1)...(n+k-1) powerful for some n>=1 with an
// "anchor" term T <= X?  Every length-k window (k in that set) contains a term T coprime to all
// primes < k (Jacobsthal: j(2)=2, j(6)=4, j(30)=6, j(210)=10).  Primes >= k divide at most one
// term of the window, so T must be powerful, and every other term N must have no prime p >= k
// with p || N.  Odd powerful T = a^2 b^3 (b squarefree, a,b odd) is enumerated by b, then a;
// for fixed b the neighbours N = b^3 a^2 + d (|d|<=10) are sieved over a by primes 3..Y with
// Y^5 > X+10 (roots of b^3 a^2 = -d mod p, Hensel-lifted to p^2 so p^2 | N is never killed).
// Survivors get an exact check: strip 2,3,5,7 and the sieved square primes; the Y-rough cofactor
// c < Y^5 is powerful iff c==1, square or cube.  Then small-prime exponents are summed.
// Build: cc -O2 -o anchor137 anchor137.c     Run: ./anchor137 X workers [dump]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <time.h>
static double TS=0,TE=0; static double now(){struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec;}

typedef unsigned __int128 u128;
typedef uint64_t u64; typedef uint32_t u32;

#define DMAX 10
#define ND (2*DMAX+1)
#define SEG 32768
#define WORDS (SEG/64)
#define CHUNK (1ull<<22)
#ifndef DIRECT_T
#define DIRECT_T 24
#endif

static u128 X; static u64 Y; static int dumpmode=0;
static u32 *pr; static int np;
// per prime tables
static u32 *inv2p, *gnq, *ginv; static u64 *fm; // fastmod magic
static int8_t *legd; static u32 *ssd; // [np*ND] legendre(-d) and ssq(-d)

static inline u32 fmod32(u32 a, u32 d, u64 M){ u64 low=M*a; return (u32)(((u128)low*d)>>64); }
static u64 powmod(u64 b,u64 e,u64 m){u64 r=1;b%=m;while(e){if(e&1)r=r*b%m;b=b*b%m;e>>=1;}return r;}
static int legendre(u64 x,u64 p){x%=p; if(!x) return 0; return powmod(x,(p-1)/2,p)==1?1:-1;}
static u64 tonelli(u64 n,u64 p){ // n QR, p odd prime
  n%=p; if(n==0) return 0;
  if(p%4==3) return powmod(n,(p+1)/4,p);
  u64 q=p-1; int s=0; while(!(q&1)){q>>=1;s++;}
  u64 z=2; while(legendre(z,p)!=-1) z++;
  u64 M=s,c=powmod(z,q,p),t=powmod(n,q,p),R=powmod(n,(q+1)/2,p);
  while(t!=1){ u64 i=0,tt=t; while(tt!=1){tt=tt*tt%p;i++;} u64 bb=c; for(u64 j=0;j<M-i-1;j++) bb=bb*bb%p; M=i;c=bb*bb%p;t=t*c%p;R=R*bb%p;}
  return R;
}
static u64 modinv(u64 a,u64 m){ long long t=0,nt=1; long long r=m,nr=a%m; while(nr){long long q=r/nr,tmp=t-q*nt;t=nt;nt=tmp;tmp=r-q*nr;r=nr;nr=tmp;} if(t<0)t+=m; return (u64)t;}
static u64 isqrt128(u128 n){ u64 r=(u64)sqrt((double)n); while((u128)r*r>n) r--; while((u128)(r+1)*(r+1)<=n) r++; return r;}
static u64 icbrt128(u128 n){ u64 r=(u64)cbrt((double)n); while(r>0 && (u128)r*r*r>n) r--; while((u128)(r+1)*(r+1)*(r+1)<=n) r++; return r;}
static int dclass(u32 p){ return p==3?0:p==5?1:p==7?2:3; }
static int Dp(u32 p){ return p-1<DMAX? (int)p-1 : DMAX; }

static void print128(FILE*f,u128 v){ char b[64]; int i=63; b[i]=0; if(!v){fputs("0",f);return;} while(v){b[--i]='0'+(int)(v%10);v/=10;} fputs(b+i,f);}
static u128 parse128(const char*s){ // accepts digits or 1eNN
  const char*e=strchr(s,'e'); if(e){ u128 m=0; for(const char*q=s;q<e;q++) m=m*10+(*q-'0'); int ex=atoi(e+1); while(ex--) m*=10; return m;}
  u128 v=0; for(;*s;s++) v=v*10+(*s-'0'); return v;}

// segment state
static u64 dead[4][ND][WORDS]; static u64 sqf[ND][WORDS]; static u32 sqp1[ND][SEG], sqp2[ND][SEG];
static inline void mark_sq(int di,u32 l,u32 p){ u64 m=1ull<<(l&63); u64*w=&sqf[di][l>>6];
  if(!(*w&m)){*w|=m; sqp1[di][l]=p; sqp2[di][l]=0;} else if(!sqp2[di][l]) sqp2[di][l]=p; else sqp2[di][l]=0xFFFFFFFFu; }

typedef struct { u64 cand[8], rp[8], hits, pairs, errs, anchors; } stats_t;
static stats_t ST; static FILE* OUT;

static u128 INV[4], LIM[4];
static void init_inv(void){ static const u32 sp[4]={2,3,5,7}; for(int q=1;q<4;q++){ u128 x=1; for(int i=0;i<7;i++) x*=2-(u128)sp[q]*x; INV[q]=x; LIM[q]=(~(u128)0)/sp[q]; if((u128)sp[q]*x!=1){fprintf(stderr,"inv\n");exit(1);} } }
// exact check of one non-anchor term. returns 1 if its rough part (primes>=k, and all of 3,5,7>=k) is OK.
static int check_term(u128 N,int k,int di,u32 l,int e[4]){
  static const u32 sp[4]={2,3,5,7};
  { int z= (u64)N? __builtin_ctzll((u64)N) : 64+__builtin_ctzll((u64)(N>>64)); N>>=z; e[0]=z; }
  for(int q=1;q<4;q++){ e[q]=0; u128 iv=INV[q], lim=LIM[q]; for(;;){ u128 t=N*iv; if(t>lim) break; N=t; e[q]++; } if((int)sp[q]>=k && e[q]==1) return 0; }
  if(sqf[di][l>>6]>>(l&63)&1){
    u32 a=sqp1[di][l], b=sqp2[di][l];
    if(b==0xFFFFFFFFu){ for(int t=3;t<np;t++){ u32 p=pr[t]; if(N%p==0){int ee=0; while(N%p==0){N/=p;ee++;} if(ee==1) {ST.errs++; return 0;}}}}
    else { u32 ps[2]={a,b}; for(int t=0;t<2;t++){ u32 p=ps[t]; if(p<=7) continue; int ee=0; while(N%p==0){N/=p;ee++;} if(ee<2){ST.errs++; return 0;} } }
  }
  if(N==1) return 1;
  u64 r=isqrt128(N); if((u128)r*r==N) return 1;
  u64 c=icbrt128(N); if((u128)c*c*c==N) return 1;
  return 0;
}

static void sieve_roots(u64 b,u64 s,u64 L){
  for(int t=0;t<np;t++){
    u32 p=pr[t]; u64 bm=b%p; if(!bm) continue; int D=Dp(p); int cls=dclass(p);
    int qb=legendre(bm,p); u64 sb= qb==1? tonelli(bm,p) : tonelli(bm*gnq[t]%p,p);
    u64 binv=modinv(bm,p), binv2=binv*binv%p; u64 p2=(u64)p*p; u64 bm2=b%p2, b3=bm2*bm2%p2*bm2%p2;
    for(int d=-D; d<=D; d++){ if(!d) continue; int di=d+DMAX;
      int ld=legd[t*ND+di]; if(ld*qb!=1) continue;
      u64 sq=(u64)ssd[t*ND+di]*sb%p; if(qb==-1) sq=sq*ginv[t]%p;
      u64 r1=sq*binv2%p;
      for(int z=0;z<2;z++){
        u64 r= z? (p-r1)%p : r1;
        // Hensel lift to p^2
        u64 dm = d>0? (u64)d : p2-(u64)(-d);
        u64 fr=( (u128)b3*((u128)r*r%p2) + dm )%p2; u64 m=fr/p; // f(r)=p*m
        u64 fp=2*(b3%p)%p*r%p; u64 tt=(p - m%p*modinv(fp,p)%p)%p; u64 R=(r+tt*p)%p2;
        u64 i0=(r+p-1)%p*inv2p[t]%p; // i = (a-1)/2
        u64 inv2q=(p2+1)/2; u64 iR=(R+p2-1)%p2*inv2q%p2; u64 k0=(iR-i0)/p; // iR = i0 + k0*p
        // first j with i0+j*p >= s
        u64 j= s>i0? (s-i0+p-1)/p : 0; u64 i=i0+j*p; u64 c=(j%p+p-k0)%p;
        for(; i<s+L; i+=p){ u32 l=(u32)(i-s); if(c==0) mark_sq(di,l,p); else dead[cls][di][l>>6]|=1ull<<(l&63); if(++c==p) c=0; }
      }
    }
  }
}
static void sieve_direct(u64 b,u64 s,u64 L){
  for(int t=0;t<np;t++){
    u32 p=pr[t]; u64 bm=b%p; if(!bm) continue; int D=Dp(p); int cls=dclass(p);
    u64 bb=bm*bm%p*bm%p; u64 p2=(u64)p*p;
    for(u64 l=0;l<L;l++){ u64 a=2*(s+l)+1; u64 am=a%p; u64 tt=bb*am%p*am%p; if(!tt) continue;
      for(int z=0;z<2;z++){ int d; u64 u= z? p-tt : tt; if(u>(u64)D) continue; d= z? (int)u : -(int)u; int di=d+DMAX;
        u128 T=(u128)a*a*b*b*b; u128 N=T+(u128)(__int128)d; if(d<0) N=T-(u128)(-d);
        if(N%p2==0) mark_sq(di,(u32)l,p); else dead[cls][di][l>>6]|=1ull<<(l&63); }
    }
  }
}

static const int KS[7]={3,4,5,6,7,10,11};
static void evaluate(u64 b,u64 s,u64 L){
  int nw=(int)((L+63)/64); static u64 Dk[4][ND][WORDS]; static u64 valid[4][WORDS];
  for(int di=0;di<ND;di++) for(int w=0;w<nw;w++){ u64 d11=dead[3][di][w], d7=dead[2][di][w]|d11, d5=dead[1][di][w]|d7, d3=dead[0][di][w]|d5;
    Dk[3][di][w]=d11; Dk[2][di][w]=d7; Dk[1][di][w]=d5; Dk[0][di][w]=d3; }
  // anchor validity: class0 (k=3) all odd T; class1 3∤T; class2 also 5∤T; class3 also 7∤T
  memset(valid,0,sizeof(u64)*4*WORDS);
  for(u64 l=0;l<L;l++){ u64 a=2*(s+l)+1; u64 bit=1ull<<(l&63); int w=(int)(l>>6);
    valid[0][w]|=bit; if((a*b)%3==0) continue; valid[1][w]|=bit; if((a%5)*(b%5)%5==0) continue; valid[2][w]|=bit; if((a%7)*(b%7)%7==0) continue; valid[3][w]|=bit; }
  u128 b3=(u128)b*b*b;
  // self-check: consecutive powerful pairs (T, T+-1)
  for(int sgn=-1;sgn<=1;sgn+=2){ int di=sgn+DMAX; for(int w=0;w<nw;w++){ u64 m=~Dk[0][di][w]; if(w==nw-1 && (L&63)) m&=(1ull<<(L&63))-1;
    while(m){ int bt=__builtin_ctzll(m); m&=m-1; u32 l=(u32)(w*64+bt); u64 a=2*(s+l)+1; u128 T=b3*a*a; u128 N= sgn>0? T+1 : T-1; if(N==0) continue;
      int e[4]; // pair check: N powerful <=> 2-exponent != 1 and 3,5,7 exps != 1 and rough part ok (k=3 -> sieve primes all >=3)
      if(check_term(N,3,di,l,e) && e[0]!=1){ ST.pairs++; fprintf(OUT,"PAIR "); print128(OUT, sgn>0?T:N); fprintf(OUT," b=%llu a=%llu\n",(unsigned long long)b,(unsigned long long)a);} } } }
  if(dumpmode==3){ for(u64 l=0;l<L;l++){ u64 a=2*(s+l)+1; if(a%37!=1 && b<50) continue; u128 T=b3*a*a;
      for(int d=-DMAX; d<=DMAX; d++){ if(!d) continue; int di=d+DMAX; int c=0; for(int q=0;q<4;q++) if(dead[q][di][l>>6]>>(l&63)&1) c|=1<<q;
        int sqb=(int)(sqf[di][l>>6]>>(l&63)&1); fprintf(OUT,"S "); print128(OUT,T); fprintf(OUT," %d %d %d\n",d,c,sqb);} } }
  if(dumpmode==2){ // validation: length-3 windows containing odd powerful T, neighbours with no prime >=11 exactly once
    for(int j=0;j<3;j++) for(int w=0;w<nw;w++){ u64 m=~0ull; for(int d=-j; d<=2-j; d++) if(d) m&=~Dk[3][d+DMAX][w];
      if(w==nw-1 && (L&63)) m&=(1ull<<(L&63))-1;
      while(m){ int bt=__builtin_ctzll(m); m&=m-1; u32 l=(u32)(w*64+bt); u64 a=2*(s+l)+1; u128 T=b3*a*a; if(T<(u128)(j+1)) continue; int ok=1;
        for(int d=-j; d<=2-j; d++){ if(!d) continue; int e[4]; u128 N= d>0? T+(u128)d : T-(u128)(-d); if(!check_term(N,11,d+DMAX,l,e)){ok=0;break;} }
        if(ok){ fprintf(OUT,"NM "); print128(OUT,T-(u128)j); fprintf(OUT,"\n"); } } }
  }
  for(int ki=0;ki<7;ki++){ int k=KS[ki]; int c= k==3?0: k<=5?1: k<=7?2:3;
    for(int j=0;j<k;j++){ // anchor at position j: deltas -j..k-1-j
      for(int w=0;w<nw;w++){ u64 m=valid[c][w]; for(int d=-j; d<=k-1-j && m; d++) if(d) m&=~Dk[c][d+DMAX][w];
        if(w==nw-1 && (L&63)) m&=(1ull<<(L&63))-1;
        while(m){ int bt=__builtin_ctzll(m); m&=m-1; u32 l=(u32)(w*64+bt); u64 a=2*(s+l)+1; u128 T=b3*a*a;
          if(T<(u128)(j+1)) continue; // n = T-j >= 1
          ST.cand[ki]++;
          int tot[4]={0,0,0,0}, ok=1;
          for(int d=-j; d<=k-1-j; d++){ if(!d) continue; int e[4]; u128 N= d>0? T+(u128)d : T-(u128)(-d);
            if(!check_term(N,k,d+DMAX,l,e)){ok=0;break;} for(int q=0;q<4;q++) tot[q]+=e[q]; }
          if(!ok) continue;
          ST.rp[ki]++;
          u128 n=T-(u128)j;
          if(dumpmode){ fprintf(OUT,"RP "); print128(OUT,n); fprintf(OUT," %d\n",k); }
          static const int sp[4]={2,3,5,7}; int good=1; for(int q=0;q<4;q++) if(sp[q]<k && tot[q]==1) good=0;
          if(good){ ST.hits++; fprintf(OUT,"HIT n="); print128(OUT,n); fprintf(OUT," k=%d b=%llu a=%llu j=%d\n",k,(unsigned long long)b,(unsigned long long)a,j); fflush(OUT);} }
      }
    }
  }
}

static void do_task(u64 b,u64 lo,u64 hi){
  for(u64 s=lo;s<hi;s+=SEG){ u64 L= hi-s<SEG? hi-s : SEG;
    memset(dead,0,sizeof dead); memset(sqf,0,sizeof sqf);
    double t0=now(); if(hi-lo < DIRECT_T) sieve_direct(b,s,L); else sieve_roots(b,s,L);
    double t1=now(); evaluate(b,s,L); TS+=t1-t0; TE+=now()-t1; ST.anchors+=L; }
}

int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: X workers [dump] [outdir]\n");return 1;}
  X=parse128(argv[1]); int W=atoi(argv[2]); if(argc>3) dumpmode=atoi(argv[3]); const char*od= argc>4? argv[4] : ".";
  // Y: smallest with Y^5 > X+10
  init_inv();
  Y=2; while(1){ u128 y5=(u128)Y*Y*Y*Y*Y; if(y5>X+10) break; Y++; }
  { char*isp=calloc(Y+1,1); pr=malloc(sizeof(u32)*(Y+1)); np=0; for(u64 i=2;i<=Y;i++) if(!isp[i]){ pr[np++]=(u32)i; for(u64 j=i*i;j<=Y;j+=i) isp[j]=1;} free(isp); }
  // drop p=2 (sieve uses odd primes); keep pr[0]=2 position? simplest: shift
  memmove(pr,pr+1,sizeof(u32)*(np-1)); np--;
  inv2p=malloc(4*np); gnq=malloc(4*np); ginv=malloc(4*np); fm=malloc(8*np); legd=malloc(np*ND); ssd=malloc(4*np*ND);
  for(int t=0;t<np;t++){ u32 p=pr[t]; inv2p[t]=(p+1)/2; u32 g=2; while(legendre(g,p)!=-1) g++; gnq[t]=g; ginv[t]=(u32)modinv(g,p); fm[t]=UINT64_C(0xFFFFFFFFFFFFFFFF)/p+1;
    for(int d=-DMAX; d<=DMAX; d++){ int di=d+DMAX; u64 x= ((long long)(-d)%(long long)p+p)%p; int l= legendre(x,p); legd[t*ND+di]=(int8_t)l; ssd[t*ND+di]= l==1? (u32)tonelli(x,p) : l==-1? (u32)tonelli(x*g%p,p) : 0; } }
  // sanity: t=0 is p=3 so 3,5,7 indices 0,1,2 -> check_term's fallback starts at t=3 (p=11)
  if(pr[0]!=3||pr[1]!=5||pr[2]!=7||pr[3]!=11){fprintf(stderr,"prime table\n");return 1;}
  u64 B=icbrt128(X); char*sqfree=malloc(B+1); memset(sqfree,1,B+1);
  { char*isp=calloc((u64)sqrt((double)B)+2,1); u64 r=(u64)sqrt((double)B)+1; for(u64 i=2;i<=r;i++) if(!isp[i]){ for(u64 j=i*i;j<=r;j+=i) isp[j]=1; for(u64 j=i*i;j<=B;j+=i*i) sqfree[j]=0; } free(isp);}
  fprintf(stderr,"X="); print128(stderr,X); fprintf(stderr," Y=%llu primes(odd)=%d bmax=%llu workers=%d\n",(unsigned long long)Y,np,(unsigned long long)B,W);
  volatile u64* ctr=mmap(NULL,4096,PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANON,-1,0); ctr[0]=0;
  for(int w=0;w<W;w++){ if(fork()==0){
      char fn[512]; snprintf(fn,sizeof fn,"%s/w%02d.txt",od,w); OUT=fopen(fn,"w");
      // task stream: b ascending, chunks of CHUNK; claim by global counter
      u64 myt=__atomic_fetch_add(&ctr[0],1,__ATOMIC_SEQ_CST), tid=0;
      for(u64 b=1;b<=B;b+=2){ if(!sqfree[b]) continue; u128 q=X/((u128)b*b*b); u64 A=isqrt128(q); if(A==0) break; u64 ni=(A+1)/2;
        for(u64 lo=0;lo<ni;lo+=CHUNK,tid++){ if(tid!=myt) continue; u64 hi= ni-lo<CHUNK? ni : lo+CHUNK; do_task(b,lo,hi); myt=__atomic_fetch_add(&ctr[0],1,__ATOMIC_SEQ_CST);}
      }
      // small-b tasks are 1 per b: fine. print stats
      fprintf(OUT,"TIME sieve=%.2f eval=%.2f\n",TS,TE); fprintf(OUT,"STATS anchors=%llu pairs=%llu hits=%llu errs=%llu",(unsigned long long)ST.anchors,(unsigned long long)ST.pairs,(unsigned long long)ST.hits,(unsigned long long)ST.errs);
      for(int i=0;i<7;i++) fprintf(OUT," k%d:cand=%llu,rp=%llu",KS[i],(unsigned long long)ST.cand[i],(unsigned long long)ST.rp[i]); fprintf(OUT,"\n"); fclose(OUT); _exit(0);} }
  for(int w=0;w<W;w++) wait(NULL);
  return 0;
}
