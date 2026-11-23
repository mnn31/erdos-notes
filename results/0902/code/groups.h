/* Group constructions for odd orders; elements 0..n-1, identity 0.
   Each group is Z_m x| Z_k with action x -> r^y x, optionally times Z_d (direct).
   Element encoding: ((x * k) + y) * d + w, x in Z_m, y in Z_k, w in Z_d.
   (x1,y1,w1)(x2,y2,w2) = (x1 + r^{y1} x2 mod m, y1+y2 mod k, w1+w2 mod d). */
#ifndef GROUPS_H
#define GROUPS_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 72
typedef struct { const char *name; int m, k, r, d; } gspec;
static int gn, gmul[MAXN][MAXN], ginv[MAXN];
static void build_group(gspec g) {
  int m=g.m,k=g.k,r=g.r,d=g.d; gn=m*k*d;
  if (gn>MAXN) { fprintf(stderr,"too big\n"); exit(1); }
  int rp[64]; rp[0]=1 % m; for(int i=1;i<k;i++) rp[i]=(rp[i-1]*r)%m;
  if ((rp[k-1]*r)%m != 1%m) { fprintf(stderr,"bad r: r^k != 1 mod m\n"); exit(1); }
  for(int a=0;a<gn;a++) for(int b=0;b<gn;b++){
    int x1=a/(k*d), y1=(a/d)%k, w1=a%d, x2=b/(k*d), y2=(b/d)%k, w2=b%d;
    int x=(x1+rp[y1]*x2)%m, y=(y1+y2)%k, w=(w1+w2)%d;
    gmul[a][b]=(x*k+y)*d+w; }
  /* verify group axioms */
  for(int a=0;a<gn;a++){ if(gmul[0][a]!=a||gmul[a][0]!=a){fprintf(stderr,"identity fail\n");exit(1);} }
  for(int a=0;a<gn;a++) for(int b=0;b<gn;b++) for(int c=0;c<gn;c++)
    if (gmul[gmul[a][b]][c]!=gmul[a][gmul[b][c]]) { fprintf(stderr,"assoc fail\n"); exit(1); }
  for(int a=0;a<gn;a++){ ginv[a]=-1; for(int b=0;b<gn;b++) if(gmul[a][b]==0){ ginv[a]=b; break;}
    if(ginv[a]<0||gmul[ginv[a]][a]!=0){fprintf(stderr,"inverse fail\n");exit(1);} }
}
static int is_abelian(void){ for(int a=0;a<gn;a++)for(int b=0;b<gn;b++) if(gmul[a][b]!=gmul[b][a]) return 0; return 1; }
static int elt_order(int a){ int o=1,x=a; while(x!=0){x=gmul[x][a];o++;} return o; }
static gspec GROUPS[] = {
  {"Z49",49,1,1,1}, {"Z7xZ7",7,1,1,7}, {"Z51",51,1,1,1}, {"Z53",53,1,1,1},
  {"Z55",55,1,1,1}, {"Z11:Z5",11,5,3,1}, {"Z57",57,1,1,1}, {"Z19:Z3",19,3,7,1},
  {"Z59",59,1,1,1}, {"Z61",61,1,1,1}, {"Z63",63,1,1,1}, {"Z3xZ21",21,1,1,3},
  {"Z7:Z9",7,9,2,1}, {"Z3x(Z7:Z3)",7,3,2,3}, {"Z65",65,1,1,1},
  /* controls / toy */
  {"Z67",67,1,1,1}, {"Z47",47,1,1,1}, {"Z45",45,1,1,1}, {"Z3xZ15",15,1,1,3},
  {"Z7",7,1,1,1}, {"Z19",19,1,1,1}, {"Z7:Z3",7,3,2,1},{"Z27",27,1,1,1},
  {"Z3xZ9",9,1,1,3},{"Z13:Z3",13,3,3,1},{"Z25",25,1,1,1},{"Z5xZ5",5,1,1,5},
  {"Z9xZ3",9,1,1,3}, /* dup name check */
};
static gspec CUSTOM; static char CNAME[64];
static int find_group(const char *nm){ if(!strncmp(nm,"C:",2)){ snprintf(CNAME,sizeof CNAME,"C_%s",nm+2); for(char*q=CNAME;*q;q++) if(*q==',') *q='_'; CUSTOM.name=CNAME; if(sscanf(nm+2,"%d,%d,%d,%d",&CUSTOM.m,&CUSTOM.k,&CUSTOM.r,&CUSTOM.d)!=4) return -1; return 999; } for(size_t i=0;i<sizeof(GROUPS)/sizeof(GROUPS[0]);i++) if(!strcmp(GROUPS[i].name,nm)) return (int)i; return -1; }
#endif
