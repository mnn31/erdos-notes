#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static u64 mm(u64 a,u64 b,u64 m){return (u64)((u128)a*b%m);}
static u64 pw(u64 a,u64 e,u64 m){u64 r=1%m;a%=m;while(e){if(e&1)r=mm(r,a,m);a=mm(a,a,m);e>>=1;}return r;}
static int mr(u64 n){ if(n<2)return 0; u64 sp[]={2,3,5,7,11,13,17,19,23,29,31,37,41};
  for(int i=0;i<13;i++){ if(n==sp[i])return 1; if(n%sp[i]==0)return 0; }
  u64 d=n-1;int s=0; while(!(d&1)){d>>=1;s++;}
  for(int i=0;i<13;i++){ u64 x=pw(sp[i],d,n); if(x==1||x==n-1)continue; int c=0;
    for(int r=1;r<s;r++){ x=mm(x,x,n); if(x==n-1){c=1;break;} } if(!c)return 0; } return 1; }
static u64 g(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
/* Brent's rho */
static u64 brent(u64 n){ if(n%2==0)return 2; for(u64 c=1;;c++){ u64 y=2,x,q=1,gg=1,ys=2; u64 r=1,m=64;
    do{ x=y; for(u64 i=0;i<r;i++) y=(mm(y,y,n)+c)%n; u64 k=0;
      do{ ys=y; for(u64 i=0;i<m && i<r-k;i++){ y=(mm(y,y,n)+c)%n; q=mm(q, x>y?x-y:y-x, n);} gg=g(q,n); k+=m; }while(k<r && gg==1);
      r*=2; }while(gg==1);
    if(gg==n){ do{ ys=(mm(ys,ys,n)+c)%n; gg=g(x>ys?x-ys:ys-x,n);}while(gg==1); }
    if(gg!=n) return gg; } }
/* returns 1 iff every prime q=3 mod 4 divides m to an even power (m>=1) */
static int okfact(u64 m){ /* m odd, no small factors handled by caller */
  if(m==1) return 1;
  if(mr(m)) return (m&3)==1 ? 1 : 0; /* single prime to power 1 */
  /* composite: factor fully and count exponents */
  u64 st[128]; int ns=0; u64 pr[128]; int np=0; st[ns++]=m;
  while(ns){ u64 x=st[--ns]; if(x==1)continue; if(mr(x)){pr[np++]=x;continue;} u64 d=brent(x); st[ns++]=d; st[ns++]=x/d; }
  for(int i=0;i<np;i++) if((pr[i]&3)==3){ int c=0; for(int j=0;j<np;j++) if(pr[j]==pr[i]) c++; if(c&1) return 0; }
  return 1; }
static int inE(u64 m){ if(m==0) return 0; while(!(m&1)) m>>=1;
  for(u64 p=3;p<1000;p+=2){ if(p*p>m) break; if(m%p==0){ int e=0; while(m%p==0){m/=p;e++;} if((p&3)==3 && (e&1)) return 0; } }
  /* remaining m has all prime factors >= ~1000 or m is prime/1 */
  return okfact(m); }
