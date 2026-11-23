#!/bin/sh
# Reproduce all computations for WRITEUP.md (run from any directory).
set -e
D=$(cd "$(dirname "$0")" && pwd); O="$D/../out"; mkdir -p "$O"
cc -O2 -o "$D/lemma_cover" "$D/lemma_cover.c"
cc -O2 -o "$D/duality" "$D/duality.c"
(for N in 3 4 5 6 7; do "$D/lemma_cover" exhaustive $N; done) > "$O/lemma_cover_exh3to7.txt"
"$D/lemma_cover" exhaustive 8 > "$O/lemma_cover_exh8.txt"            # ~3 min
(for N in 6 7 9 10 11 12 13 14 16 18; do "$D/lemma_cover" random $N 200000 $((N*7919)); done
 "$D/lemma_cover" random 20 20000 158380) > "$O/lemma_cover_random.txt"   # ~10 min
"$D/duality" full > "$O/duality_full_r3n6.txt"
(for r in 3 4 5 6; do "$D/duality" random $r 200000 $((r*104729)); done) > "$O/duality_random.txt"
cat "$O"/*.txt
