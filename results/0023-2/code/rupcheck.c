/* Forward DRUP checker (RUP lemmas only; no RAT).
 *
 * Usage: rupcheck formula.cnf proof.drup
 *
 * Every added lemma L is checked to be RUP w.r.t. the current clause database:
 * assigning all literals of L false and running unit propagation must give a conflict.
 * The proof is accepted only if the empty clause is derived (either as a lemma, or
 * because unit propagation at top level reaches a conflict after some lemma is added).
 *
 * Deletions: a deleted clause is removed from the database. Deleting clauses only
 * weakens the database, so it can never make an invalid lemma pass. (Unit clauses
 * are never deleted, as in drat-trim; keeping a clause is always sound.)
 *
 * Soundness argument: each lemma accepted is implied by the clauses present at that
 * moment (RUP => implied), and those clauses are original or previously accepted lemmas,
 * so by induction every clause in the database is implied by the original formula.
 * Deriving the empty clause therefore proves the original formula unsatisfiable.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int nvars;
static int **cls; static int *clen; static char *cdel; static int ncls, capcls;
static int **wl; static int *wlen, *wcap;   /* watch lists indexed by literal code */
static signed char *val;                    /* value of variable: 0 unassigned, 1 true, -1 false */
static int *trail; static int tlen;

static inline int code(int lit) { return lit > 0 ? 2 * lit : -2 * lit + 1; }
static inline int litval(int lit) { int v = val[abs(lit)]; return lit > 0 ? v : -v; }
static void assign(int lit) { val[abs(lit)] = lit > 0 ? 1 : -1; trail[tlen++] = lit; }
static void watch(int lit, int c) {
    int k = code(lit);
    if (wlen[k] == wcap[k]) { wcap[k] = wcap[k] ? 2 * wcap[k] : 4; wl[k] = realloc(wl[k], sizeof(int) * wcap[k]); }
    wl[k][wlen[k]++] = c;
}

/* propagate from trail position qhead; return 1 on conflict */
static int propagate(int qhead) {
    while (qhead < tlen) {
        int lit = trail[qhead++];
        int fl = -lit;                       /* literal that became false */
        int k = code(fl);
        int i = 0, j = 0;
        while (i < wlen[k]) {
            int c = wl[k][i++];
            if (cdel[c]) continue;           /* drop deleted clause from this list */
            int *C = cls[c];
            if (C[0] == fl) { C[0] = C[1]; C[1] = fl; }
            /* now C[1] == fl */
            if (litval(C[0]) == 1) { wl[k][j++] = c; continue; }
            int found = 0;
            for (int t = 2; t < clen[c]; t++) {
                if (litval(C[t]) != -1) {
                    C[1] = C[t]; C[t] = fl; watch(C[1], c); found = 1; break;
                }
            }
            if (found) continue;
            wl[k][j++] = c;
            if (litval(C[0]) == -1) {        /* conflict */
                while (i < wlen[k]) wl[k][j++] = wl[k][i++];
                wlen[k] = j;
                return 1;
            }
            if (litval(C[0]) == 0) assign(C[0]);
        }
        wlen[k] = j;
    }
    return 0;
}

/* hash table of clauses for deletion lookup (key: sorted literal multiset) */
#define HBITS 22
static int *hhead, *hnext;
static unsigned long long hkey(int *C, int n) {
    unsigned long long s = 0, x = 1469598103934665603ULL, sum = 0, prod = 1;
    for (int i = 0; i < n; i++) { unsigned long long l = (unsigned long long)(long long)C[i];
        sum += l * 0x9E3779B97F4A7C15ULL; prod *= (l * 2 + 1); x ^= l * 0xBF58476D1CE4E5B9ULL; }
    s = sum ^ (prod * 31) ^ (unsigned long long)n;
    (void)x; return s;
}
static int same_set(int *A, int na, int *B, int nb) {
    if (na != nb) return 0;
    for (int i = 0; i < na; i++) { int f = 0; for (int j = 0; j < nb; j++) if (A[i] == B[j]) { f = 1; break; } if (!f) return 0; }
    return 1;
}

static int status_conflict = 0;   /* top-level conflict reached */

/* add clause to database (assumes current assignment = top level). */
static void add_clause(int *lits, int n) {
    if (ncls == capcls) {
        capcls = capcls ? 2 * capcls : 1024;
        cls = realloc(cls, sizeof(int *) * capcls); clen = realloc(clen, sizeof(int) * capcls);
        cdel = realloc(cdel, capcls); hnext = realloc(hnext, sizeof(int) * capcls);
    }
    int c = ncls++;
    cls[c] = malloc(sizeof(int) * (n ? n : 1)); memcpy(cls[c], lits, sizeof(int) * n);
    clen[c] = n; cdel[c] = 0;
    unsigned long long h = hkey(lits, n) & ((1u << HBITS) - 1);
    hnext[c] = hhead[h]; hhead[h] = c;
    if (status_conflict) return;
    if (n == 0) { status_conflict = 1; return; }
    int *C = cls[c];
    /* move non-false literals to the front */
    int nf = 0;
    for (int i = 0; i < n; i++) if (litval(C[i]) != -1) { int t = C[nf]; C[nf] = C[i]; C[i] = t; nf++; }
    for (int i = 0; i < n; i++) if (litval(C[i]) == 1) { int t = C[0]; C[0] = C[i]; C[i] = t; break; }
    if (n == 1) {
        cdel[c] = 0;
        if (litval(C[0]) == -1) { status_conflict = 1; return; }
        if (litval(C[0]) == 0) { int q = tlen; assign(C[0]); if (propagate(q)) status_conflict = 1; }
        return;
    }
    watch(C[0], c); watch(C[1], c);
    if (litval(C[0]) == 1) return;
    if (nf == 0) { status_conflict = 1; return; }
    if (nf == 1) { int q = tlen; assign(C[0]); if (propagate(q)) status_conflict = 1; }
}

static void delete_clause(int *lits, int n) {
    unsigned long long h = hkey(lits, n) & ((1u << HBITS) - 1);
    for (int c = hhead[h]; c != -1; c = hnext[c]) {
        if (!cdel[c] && same_set(cls[c], clen[c], lits, n)) {
            if (clen[c] <= 1) return;        /* never delete units */
            /* do not delete a clause that is currently the reason of a top-level unit:
               we simply keep any clause whose literal set is unit/satisfied-propagating; keeping
               clauses is always sound, so only delete when no literal is assigned at top level */
            for (int i = 0; i < clen[c]; i++) if (litval(cls[c][i]) != 0) return;
            cdel[c] = 1; return;
        }
    }
}

/* RUP check of lemma at top level; returns 1 if RUP */
static int rup(int *lits, int n) {
    int save = tlen, ok = 0;
    for (int i = 0; i < n; i++) {
        int v = litval(lits[i]);
        if (v == 1) { ok = 1; goto undo; }    /* lemma satisfied at top level: implied */
        if (v == 0) assign(-lits[i]);
    }
    ok = propagate(save);
undo:
    while (tlen > save) { val[abs(trail[--tlen])] = 0; }
    return ok;
}

static int *buf; static int bcap;
static int readclause(FILE *f, int *isdel, int *n) {
    int x, k = 0; *isdel = 0;
    int ch;
    while ((ch = fgetc(f)) != EOF) {
        if (ch == ' ' || ch == '\n' || ch == '\t' || ch == '\r') continue;
        if (ch == 'c') { while ((ch = fgetc(f)) != EOF && ch != '\n'); continue; }
        if (ch == 'p') { while ((ch = fgetc(f)) != EOF && ch != '\n'); continue; }
        if (ch == 'd') { *isdel = 1; continue; }
        ungetc(ch, f); break;
    }
    if (ch == EOF) return 0;
    while (fscanf(f, "%d", &x) == 1) {
        if (x == 0) { *n = k; return 1; }
        if (abs(x) > nvars) { fprintf(stderr, "variable %d exceeds header\n", x); exit(2); }
        if (k == bcap) { bcap = bcap ? 2 * bcap : 1024; buf = realloc(buf, sizeof(int) * bcap); }
        buf[k++] = x;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage\n"); return 2; }
    FILE *f = fopen(argv[1], "r"); char line[4096];
    int ncl = 0;
    while (fgets(line, sizeof line, f)) if (line[0] == 'p') { sscanf(line, "p cnf %d %d", &nvars, &ncl); break; }
    rewind(f);
    nvars += 1;  /* allow proof to mention no new variables beyond header (RUP-only proofs) */
    val = calloc(nvars + 1, 1); trail = malloc(sizeof(int) * (nvars + 2));
    wl = calloc(2 * nvars + 4, sizeof(int *)); wlen = calloc(2 * nvars + 4, sizeof(int)); wcap = calloc(2 * nvars + 4, sizeof(int));
    hhead = malloc(sizeof(int) << HBITS); for (int i = 0; i < (1 << HBITS); i++) hhead[i] = -1;
    int isdel, n, read = 0;
    while (readclause(f, &isdel, &n)) { add_clause(buf, n); read++; }
    fclose(f);
    if (read != ncl) { fprintf(stderr, "clause count mismatch %d vs %d\n", read, ncl); return 2; }
    printf("formula: %d vars, %d clauses; top-level conflict already: %d\n", nvars - 1, ncl, status_conflict);
    FILE *p = fopen(argv[2], "r");
    long added = 0, deleted = 0, lineno = 0;
    while (!status_conflict && readclause(p, &isdel, &n)) {
        lineno++;
        if (isdel) { delete_clause(buf, n); deleted++; continue; }
        if (!rup(buf, n)) { printf("FAIL: lemma %ld (proof clause #%ld) is not RUP\n", added + 1, lineno); return 1; }
        add_clause(buf, n); added++;
        if (n == 0) break;
    }
    fclose(p);
    printf("lemmas checked: %ld, deletions: %ld\n", added, deleted);
    if (status_conflict) { printf("VERIFIED: empty clause derived, formula UNSAT\n"); return 0; }
    printf("NOT VERIFIED: proof ended without empty clause\n"); return 1;
}
