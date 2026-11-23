#!/bin/bash
# Full reproduction. Needs refs/b000664.txt (OEIS A000664 b-file) and, for the cross-check,
# the scout's checker ../../code/arrow.py.   Run:  bash code/reproduce.sh
set -u
cd "$(dirname "$0")/.."
cc -O2 -o code/arrow code/arrow.c
mkdir -p out/graphs out/runs out/sweepw
# 1. graph lists g1..g12 (gen.py) and g13 (gen_next.py); count check against OEIS A000664
[ -f out/graphs/g12.txt ] || python3 -I code/gen.py 12 out/graphs > out/gen_log.txt 2>&1
[ -f out/graphs/g13.txt ] || python3 -I code/gen_next.py out/graphs 13 "${TMPDIR:-/tmp}/shards13_$$" > out/gen13_log.txt 2>&1
python3 -I code/check_graph_files.py out/graphs refs/b000664.txt 13 > out/graph_files_check.txt
# 2. validation: refereed values, positive controls, cross-check against the scout's checker
bash code/validate_small.sh > out/validation_small.txt 2>&1
{ code/arrow 2 2 out/graphs/g3.txt; code/arrow 2 2,2 out/graphs/g6.txt; } > out/positive_controls.txt
python3 -I code/crosscheck_scout.py ../../code out/graphs > out/crosscheck_scout.txt 2>&1
# 3. the six target instances (witness files kept uncompressed in out/runs)
python3 -I code/run_instance.py 2,2,1 2,1,1 out/graphs out/runs > out/main_221_vs_211.txt 2>&1
for p in "2,2,1 2,2,1" "2,1,1 2,2,1,1"; do python3 -I code/run_instance.py $p out/graphs out/runs; done > out/main_value12.txt 2>&1
for p in "3,2,1 2,1,1" "2,2,2 2,1,1" "2,2,1 2,1,1,1"; do python3 -I code/run_instance.py $p out/graphs out/runs; done > out/main_value13.txt 2>&1
code/arrow 2,2,1 2,1,1 out/graphs/g11.txt > out/extremal_2.2.1_vs_2.1.1_e11.txt
code/arrow 2,2,1 2,2,1 out/graphs/g12.txt > out/extremal_2.2.1_vs_2.2.1_e12.txt
code/arrow 2,1,1 2,2,1,1 out/graphs/g12.txt > out/extremal_2.1.1_vs_2.2.1.1_e12.txt
echo MAIN_DONE
# 4. sweep over every pair (up to swapping colours) with value <= 13, and frontier pairs at 14
python3 -I code/all_pairs.py 14 > out/all_pairs_le14.txt
awk '$1<=12' out/all_pairs_le14.txt | xargs -P 8 -L 1 bash code/sweep_one.sh > out/sweep_le12.txt 2>&1
awk '$1==13' out/all_pairs_le14.txt | xargs -P 8 -L 1 bash code/sweep_one.sh > out/sweep_13.txt 2>&1
# value 14: only the 11 'frontier' pairs (both sides >= 3 stars, neither a matching); the full
# 309-pair value-14 sweep was estimated at ~6 h and not run.
python3 -I code/filter14.py out/all_pairs_le14.txt > out/pairs14_frontier.txt
xargs -P 6 -L 1 bash code/sweep_one.sh < out/pairs14_frontier.txt > out/sweep_14_frontier.txt 2>&1
echo DONE
