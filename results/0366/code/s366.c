// Erdos #366 search: for every 3-full u = B^4 C^5 t^3 <= U (B,C squarefree coprime, u>1),
// decide exactly whether u+d is 2-full, for each shift d in a list (production: d=-1,+1).
// Polynomial sieve over t of f(t) = c t^3 + d, c = B^4 C^5, with all primes p <= P,
// (P+1)^5 > U + max|d|.  Primes 2,3 and primes dividing some d: residue classes mod q^2
// (exact), plus full stripping at test time.  Other primes p (p !| c d): roots of
// c t^3 = -d mod p via discrete-log tables, unique Hensel lift to p^2.  A position with
// t = root mod p is rejected unless t = lifted root mod p^2 (then p^2 | f, p recorded in rad).
// Survivor: strip brute primes (reject if exponent 1), strip rad primes; cofactor m has all
// prime factors > P and m <= U+max|d| < (P+1)^5, so m 2-full <=> m in {1, square, cube}.
// Usage: s366 U nthreads d1 d2 ... [-check]   (-check: compare every position against
// an independent trial-division 2-full test; only for small U)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
#include <stdatomic.h>
typedef unsigned __int128 u128;
typedef __int128 i128;
typedef uint64_t u64; typedef uint32_t u32; typedef int64_t i64;

#define MAXD 16
static u128 U; static int ND; static i64 Dv[MAXD]; static i64 maxabsd;
static int NT; static int CHECK = 0;
static u64 P;
static u32 *primes; static int nprimes;            // all primes <= P
static int *isbrute;                                // per prime index
static u64 *toff; static u32 *LOGT, *EXPT;          // tables for hensel primes
static u32 *inv3; // per prime: 3^{-1} mod (p-1) if p%3==2
static u32 *lognegd; // per prime*MAXD: log(-d mod p), or UINT32_MAX if p|d
// families
static u32 *FB, *FC; static u128 *Fc; static u64 *FT; static u64 nfam;
// segments
typedef struct { u64 fam; u64 tlo, thi; u64 off; } seg_t;
static seg_t *segs; static u64 nsegs, segcap;
static u64 *chunkstart; static u64 nchunks, chunkcap;
static u64 M = 1u << 20; static int MAXSEG = 2048;
static atomic_ulong nextchunk;
static atomic_ulong tot_pos, tot_surv, tot_hits, tot_checked, tot_mismatch;
static pthread_mutex_t outmx = PTHREAD_MUTEX_INITIALIZER;

static u128 parse128(const char *s) {
  // accepts integer or 1eNN
  const char *e = strchr(s, 'e');
  if (e) { u128 m = strtoull(s, 0, 10); int k = atoi(e + 1); while (k--) m *= 10; return m; }
  u128 v = 0; for (; *s; s++) v = v * 10 + (*s - '0'); return v;
}
static void print128(FILE *f, u128 v) {
  char buf[64]; int i = 63; buf[i] = 0;
  if (v == 0) buf[--i] = '0';
  while (v) { buf[--i] = '0' + (int)(v % 10); v /= 10; }
  fputs(buf + i, f);
}
static u128 isqrt128(u128 n) {
  if (n == 0) return 0;
  u128 r = (u128)sqrt((double)n);
  while (r * r > n) r--;
  while ((r + 1) * (r + 1) <= n) r++;
  return r;
}
static u128 icbrt128(u128 n) {
  if (n == 0) return 0;
  u128 r = (u128)cbrt((double)n);
  while (r > 0 && r * r * r > n) r--;
  while ((r + 1) * (r + 1) * (r + 1) <= n) r++;
  return r;
}
static u64 iroot5(u128 n) { u64 r = (u64)pow((double)n, 0.2); while ((u128)r*r*r*r*r > n) r--; while ((u128)(r+1)*(r+1)*(r+1)*(r+1)*(r+1) <= n) r++; return r; }
static u64 iroot4(u128 n) { u64 r = (u64)sqrt(sqrt((double)n)); while (r>0 && (u128)r*r*r*r > n) r--; while ((u128)(r+1)*(r+1)*(r+1)*(r+1) <= n) r++; return r; }
static u64 gcd64(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }
static u64 powmod(u64 a, u64 e, u64 m) { u64 r = 1 % m; a %= m; while (e) { if (e & 1) r = (u128)r * a % m; a = (u128)a * a % m; e >>= 1; } return r; }

// independent exact 2-full test by trial division (for -check only; n small)
static int twofull_trial(u128 n) {
  if (n == 0) return 0;
  if (n == 1) return 1;
  for (u64 p = 2; (u128)p * p * p <= n; p += (p == 2 ? 1 : 2)) {
    if (n % p == 0) { int e = 0; while (n % p == 0) { n /= p; e++; } if (e == 1) return 0; }
  }
  // remaining n has all prime factors > cube root of the remaining value: 1, q, q^2, or q*r
  if (n == 1) return 1;
  u128 s = isqrt128(n); return s * s == n;
}

static void add_seg(u64 fam, u64 tlo, u64 thi, u64 *cur, int *curseg) {
  if (nsegs == segcap) { segcap = segcap ? 2 * segcap : 1 << 16; segs = realloc(segs, segcap * sizeof(seg_t)); }
  u64 len = thi - tlo + 1;
  if (*curseg > 0 && (*cur + len > M || *curseg >= MAXSEG)) { // close chunk
    if (nchunks + 1 >= chunkcap) { chunkcap = chunkcap ? 2 * chunkcap : 1 << 12; chunkstart = realloc(chunkstart, chunkcap * sizeof(u64)); }
    chunkstart[++nchunks] = nsegs; *cur = 0; *curseg = 0;
  }
  segs[nsegs].fam = fam; segs[nsegs].tlo = tlo; segs[nsegs].thi = thi; segs[nsegs].off = *cur;
  nsegs++; *cur += len; (*curseg)++;
}

typedef struct { uint8_t *rej[MAXD]; u64 *rad[MAXD]; } tbuf_t;

static void process_chunk(u64 ch, tbuf_t *tb) {
  u64 s0 = chunkstart[ch], s1 = chunkstart[ch + 1];
  u64 npos = segs[s1 - 1].off + (segs[s1 - 1].thi - segs[s1 - 1].tlo + 1);
  for (int j = 0; j < ND; j++) { memset(tb->rej[j], 0, npos); for (u64 i = 0; i < npos; i++) tb->rad[j][i] = 1; }
  // brute primes: classes mod q^2
  for (int pi = 0; pi < nprimes; pi++) if (isbrute[pi]) {
    u64 q = primes[pi], q2 = q * q;
    for (u64 s = s0; s < s1; s++) {
      seg_t *sg = &segs[s]; u64 cq = (u64)(Fc[sg->fam] % q2);
      for (int j = 0; j < ND; j++) {
        i64 dm = ((Dv[j] % (i64)q2) + (i64)q2) % (i64)q2;
        for (u64 k = 0; k < q2; k++) {
          u64 val = (u64)(((u128)cq * k % q2 * k % q2 * k + (u64)dm) % q2);
          if (val % q == 0 && val != 0) {
            u64 first = sg->tlo + ((k + q2 - sg->tlo % q2) % q2);
            for (u64 t = first; t <= sg->thi; t += q2) tb->rej[j][sg->off + t - sg->tlo] = 1;
          }
        }
      }
    }
  }
  // hensel primes
  for (int pi = 0; pi < nprimes; pi++) if (!isbrute[pi]) {
    u64 p = primes[pi], pm1 = p - 1, p2 = p * p;
    const u32 *LG = LOGT + toff[pi], *EX = EXPT + toff[pi];
    for (u64 s = s0; s < s1; s++) {
      seg_t *sg = &segs[s]; u64 f = sg->fam;
      u32 bm = FB[f] % p, cm = FC[f] % p;
      if (bm == 0 || cm == 0) continue; // p | c: p never divides c t^3 + d (p !| d)
      u64 lc = (4 * (u64)LG[bm] + 5 * (u64)LG[cm]) % pm1;
      u64 cq = 0; int havecq = 0; u64 cmodp = EX[lc];
      for (int j = 0; j < ND; j++) {
        u32 ld = lognegd[(u64)pi * MAXD + j];
        u64 L = (ld + pm1 - lc) % pm1;
        u64 ex[3]; int nr = 0;
        if (p % 3 == 2) { ex[0] = (u64)L * inv3[pi] % pm1; nr = 1; }
        else if (L % 3 == 0) { u64 e0 = L / 3, st = pm1 / 3; ex[0] = e0; ex[1] = e0 + st; ex[2] = e0 + 2 * st; nr = 3; }
        for (int r_ = 0; r_ < nr; r_++) {
          u64 r = EX[ex[r_]];
          u64 first = sg->tlo + ((r + p - sg->tlo % p) % p);
          if (first > sg->thi) continue;
          if (!havecq) { cq = (u64)(Fc[f] % p2); havecq = 1; }
          i64 dm = ((Dv[j] % (i64)p2) + (i64)p2) % (i64)p2;
          u64 fr = (u64)(((u128)cq * r % p2 * r % p2 * r + (u64)dm) % p2);
          if (fr % p != 0) { fprintf(stderr, "BUG root p=%llu\n", (unsigned long long)p); exit(3); }
          u64 a = fr / p;
          u64 fp = 3 * cmodp % p * r % p * r % p;
          u64 inv = EX[(pm1 - LG[fp]) % pm1];
          u64 k0 = (p - a * inv % p) % p;                 // t = r + k p has p^2 | f iff k = k0 mod p
          u64 k = ((first - r) / p) % p;
          uint8_t *RJ = tb->rej[j] + sg->off; u64 *RD = tb->rad[j] + sg->off;
          for (u64 t = first; t <= sg->thi; t += p) {
            if (k == k0) RD[t - sg->tlo] *= p; else RJ[t - sg->tlo] = 1;
            if (++k == p) k = 0;
          }
        }
      }
    }
  }
  // survivors
  u64 surv = 0, hits = 0, checked = 0, mism = 0;
  for (u64 s = s0; s < s1; s++) {
    seg_t *sg = &segs[s]; u64 f = sg->fam; u128 c = Fc[f];
    for (u64 t = sg->tlo; t <= sg->thi; t++) {
      u64 idx = sg->off + t - sg->tlo; u128 u = c * t * t * t;
      for (int j = 0; j < ND; j++) {
        int verdict = 0;
        i128 fv = (i128)u + Dv[j];
        if (fv <= 0) continue;
        if (!tb->rej[j][idx]) {
          surv++;
          u128 m = (u128)fv; int ok = 1;
          for (int pi = 0; pi < nprimes && ok; pi++) if (isbrute[pi]) {
            u64 q = primes[pi]; int e = 0; while (m % q == 0) { m /= q; e++; } if (e == 1) ok = 0;
          }
          if (ok) {
            u64 R = tb->rad[j][idx];
            while (R > 1) { u64 g = gcd64((u64)(m % R), R); if (g == 1) break; m /= g; }
            if (m == 1) verdict = 1;
            else { u128 r2 = isqrt128(m); if (r2 * r2 == m) verdict = 1; else { u128 r3 = icbrt128(m); if (r3 * r3 * r3 == m) verdict = 1; } }
          }
        }
        if (verdict) {
          hits++;
          pthread_mutex_lock(&outmx);
          printf("HIT d=%lld B=%u C=%u t=%llu u=", (long long)Dv[j], FB[f], FC[f], (unsigned long long)t);
          print128(stdout, u); printf(" u+d="); print128(stdout, (u128)fv); printf("\n"); fflush(stdout);
          pthread_mutex_unlock(&outmx);
        }
        if (CHECK) { checked++; if (twofull_trial((u128)fv) != verdict) { mism++;
          pthread_mutex_lock(&outmx); printf("MISMATCH d=%lld u=", (long long)Dv[j]); print128(stdout, u); printf(" sieve=%d\n", verdict); pthread_mutex_unlock(&outmx); } }
      }
    }
  }
  atomic_fetch_add(&tot_pos, npos); atomic_fetch_add(&tot_surv, surv); atomic_fetch_add(&tot_hits, hits);
  atomic_fetch_add(&tot_checked, checked); atomic_fetch_add(&tot_mismatch, mism);
}

static void *worker(void *arg) {
  tbuf_t tb; (void)arg;
  for (int j = 0; j < ND; j++) { tb.rej[j] = malloc(M + 16); tb.rad[j] = malloc((M + 16) * sizeof(u64)); }
  for (;;) {
    u64 ch = atomic_fetch_add(&nextchunk, 1);
    if (ch >= nchunks) break;
    process_chunk(ch, &tb);
  }
  return 0;
}

static int tbl_next; static pthread_mutex_t tblmx = PTHREAD_MUTEX_INITIALIZER;
static void *tblworker(void *arg) {
  (void)arg;
  for (;;) {
    pthread_mutex_lock(&tblmx); int pi = tbl_next++; pthread_mutex_unlock(&tblmx);
    if (pi >= nprimes) break;
    if (isbrute[pi]) continue;
    u64 p = primes[pi], pm1 = p - 1;
    // primitive root
    u64 fac[32]; int nf = 0; u64 x = pm1;
    for (u64 q = 2; q * q <= x; q++) if (x % q == 0) { fac[nf++] = q; while (x % q == 0) x /= q; }
    if (x > 1) fac[nf++] = x;
    u64 g = 2;
    for (;; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powmod(g, pm1 / fac[i], p) == 1) { ok = 0; break; } if (ok) break; }
    u32 *LG = LOGT + toff[pi], *EX = EXPT + toff[pi];
    u64 v = 1;
    for (u64 k = 0; k < pm1; k++) { EX[k] = (u32)v; LG[v] = (u32)k; v = v * g % p; }
    if (v != 1) { fprintf(stderr, "BUG primroot\n"); exit(3); }
    if (p % 3 == 2) { // inverse of 3 mod p-1
      for (u64 i = 1; i < pm1; i++) if ((3 * i) % pm1 == 1) { inv3[pi] = (u32)i; break; }
    }
    for (int j = 0; j < ND; j++) {
      i64 dm = (((-Dv[j]) % (i64)p) + (i64)p) % (i64)p;
      lognegd[(u64)pi * MAXD + j] = dm == 0 ? UINT32_MAX : LG[dm];
      if (dm == 0) { fprintf(stderr, "BUG p|d for hensel prime\n"); exit(3); }
    }
  }
  return 0;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage\n"); return 1; }
  U = parse128(argv[1]); NT = atoi(argv[2]); ND = 0; maxabsd = 0;
  for (int i = 3; i < argc; i++) {
    if (!strcmp(argv[i], "-check")) { CHECK = 1; continue; }
    if (!strncmp(argv[i], "-M", 2)) { M = strtoull(argv[i] + 2, 0, 10); continue; }
    Dv[ND] = atoll(argv[i]); if (llabs(Dv[ND]) > maxabsd) maxabsd = llabs(Dv[ND]); ND++;
  }
  u128 Fmax = U + maxabsd;
  P = iroot5(Fmax); while ((u128)(P + 1) * (P + 1) * (P + 1) * (P + 1) * (P + 1) <= Fmax) P++;
  // need (P+1)^5 > Fmax: iroot5 gives largest r with r^5 <= Fmax, so (r+1)^5 > Fmax. ok.
  if (P < 3) P = 3;
  printf("# U="); print128(stdout, U); printf(" P=%llu ND=%d d:", (unsigned long long)P, ND);
  for (int j = 0; j < ND; j++) printf(" %lld", (long long)Dv[j]); printf(" check=%d\n", CHECK);
  // primes
  char *comp = calloc(P + 1, 1); nprimes = 0; primes = malloc(sizeof(u32) * (P + 1));
  for (u64 i = 2; i <= P; i++) if (!comp[i]) { primes[nprimes++] = (u32)i; for (u64 k = i * i; k <= P; k += i) comp[k] = 1; }
  free(comp);
  isbrute = calloc(nprimes, sizeof(int)); toff = malloc(sizeof(u64) * nprimes);
  inv3 = calloc(nprimes, sizeof(u32)); lognegd = calloc((u64)nprimes * MAXD, sizeof(u32));
  u64 tot = 0;
  for (int i = 0; i < nprimes; i++) {
    u64 p = primes[i]; int b = (p == 2 || p == 3);
    for (int j = 0; j < ND; j++) if (Dv[j] % (i64)p == 0) b = 1;
    isbrute[i] = b; toff[i] = tot; if (!b) tot += p;
  }
  LOGT = malloc(sizeof(u32) * (tot + 1)); EXPT = malloc(sizeof(u32) * (tot + 1));
  printf("# nprimes=%d table entries=%llu (%.2f GB)\n", nprimes, (unsigned long long)tot, 8.0 * tot / 1e9); fflush(stdout);
  { pthread_t th[64]; tbl_next = 0; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, tblworker, 0); for (int i = 0; i < NT; i++) pthread_join(th[i], 0); }
  printf("# tables built\n"); fflush(stdout);
  // squarefree flags up to U^(1/4)
  u64 Bmax = iroot4(U);
  char *sqf = malloc(Bmax + 2); memset(sqf, 1, Bmax + 2);
  for (u64 i = 2; i * i <= Bmax; i++) for (u64 k = i * i; k <= Bmax; k += i * i) sqf[k] = 0;
  // families
  u64 cap = 1 << 20; FB = malloc(cap * 4); FC = malloc(cap * 4); Fc = malloc(cap * 16); FT = malloc(cap * 8); nfam = 0;
  u128 totpos = 0;
  for (u64 C = 1; (u128)C * C * C * C * C <= U; C++) {
    if (!sqf[C]) continue;
    u128 C5 = (u128)C * C * C * C * C;
    for (u64 B = 1; (u128)B * B * B * B * C5 <= U; B++) {
      if (!sqf[B] || gcd64(B, C) != 1) continue;
      u128 c = (u128)B * B * B * B * C5;
      u64 T = (u64)icbrt128(U / c);
      if (c == 1 && T < 2) continue;
      if (nfam == cap) { cap *= 2; FB = realloc(FB, cap * 4); FC = realloc(FC, cap * 4); Fc = realloc(Fc, cap * 16); FT = realloc(FT, cap * 8); }
      FB[nfam] = (u32)B; FC[nfam] = (u32)C; Fc[nfam] = c; FT[nfam] = T; nfam++;
      totpos += (c == 1) ? T - 1 : T;
    }
  }
  printf("# families=%llu positions(3-full u in (1,U])=", (unsigned long long)nfam); print128(stdout, totpos); printf("\n"); fflush(stdout);
  // chunks
  chunkcap = 1 << 12; chunkstart = malloc(chunkcap * sizeof(u64)); nchunks = 0; chunkstart[0] = 0;
  u64 cur = 0; int curseg = 0;
  for (u64 f = 0; f < nfam; f++) {
    u64 tlo = (Fc[f] == 1) ? 2 : 1, T = FT[f];
    for (u64 a = tlo; a <= T; a += M) { u64 b = a + M - 1; if (b > T) b = T; add_seg(f, a, b, &cur, &curseg); }
  }
  if (nchunks + 1 >= chunkcap) { chunkcap *= 2; chunkstart = realloc(chunkstart, chunkcap * sizeof(u64)); }
  chunkstart[++nchunks] = nsegs;
  printf("# chunks=%llu segs=%llu\n", (unsigned long long)nchunks, (unsigned long long)nsegs); fflush(stdout);
  pthread_t th[64]; atomic_store(&nextchunk, 0);
  for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, worker, 0);
  for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
  printf("# DONE positions=%lu (expect ", (unsigned long)atomic_load(&tot_pos)); print128(stdout, totpos);
  printf(") survivors=%lu hits=%lu checked=%lu mismatches=%lu\n", (unsigned long)atomic_load(&tot_surv), (unsigned long)atomic_load(&tot_hits),
         (unsigned long)atomic_load(&tot_checked), (unsigned long)atomic_load(&tot_mismatch));
  return 0;
}
