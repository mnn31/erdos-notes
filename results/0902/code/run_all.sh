#!/bin/bash
# Reproduce everything. Run from the prove/ directory:  bash code/run_all.sh
set -e
cd "$(dirname "$0")/.."
clang -O2 -march=native -o code/search code/search.c -lpthread
clang -O2 -march=native -o code/check2 code/check2.c -lpthread
clang -O2 -march=native -DFOUNDCAP=100000000 -o code/search_val code/search.c -lpthread
python3 -I code/groupinfo.py > out/groupinfo.txt
mkdir -p out/main out/small out/check2 out/validate
# main search, all groups of odd order 49..65 (+ Z67 control)
(cd out/main; for g in Z49 Z7xZ7 Z51 Z53 Z55 Z11:Z5 Z57 Z19:Z3 Z59 Z61 Z63 Z3xZ21 Z7:Z9 "Z3x(Z7:Z3)" Z65 Z67; do ../../code/search "$g" 4 10; done) > out/main/run_all.log 2>&1
# all groups of odd order 31..47
(cd out/small; for g in C:31,1,1,1 C:33,1,1,1 C:35,1,1,1 C:37,1,1,1 C:39,1,1,1 Z13:Z3 C:41,1,1,1 C:43,1,1,1 Z45 Z3xZ15 Z47; do ../../code/search "$g" 4 10; done) > out/small/run_small.log 2>&1
# independent second implementation, no halving
(cd out/check2; for g in Z49 Z7xZ7 Z51 Z53 Z55 Z11:Z5 Z57 Z19:Z3 Z59 Z61 Z63 Z3xZ21 Z7:Z9 "Z3x(Z7:Z3)" Z65; do ../../code/check2 "$g" 10; done) > out/check2/run_check2.log 2>&1
(cd out/check2; for g in C:31,1,1,1 C:33,1,1,1 C:35,1,1,1 C:37,1,1,1 C:39,1,1,1 Z13:Z3 C:41,1,1,1 C:43,1,1,1 Z45 Z3xZ15 Z47; do ../../code/check2 "$g" 10; done) > out/check2/run_check2_small.log 2>&1
# positive control for check2: parts 7 and 8 of 16 of the Z67 index space contain NQR67 and QR67
(cd out/check2; for p in 7 8; do ../../code/check2 Z67 10 $p 16; done) > out/check2/run_check2_Z67_parts.log 2>&1
python3 -I code/verify_sets.py 67 1 1 1 4 out/main/found_Z67_k4.txt > out/main/verify_Z67.txt
# brute-force comparison (small cases), see out/validate/validate_k23.log
(cd out/validate; for spec in "7 1 1 1 2" "19 1 1 1 3" "23 1 1 1 3" "7 3 2 1 2" "7 3 2 1 3" "3 1 1 3 2" "11 1 1 1 2" "13 1 1 1 2" "9 1 1 1 2" "3 1 1 3 3" "19 1 1 1 2" "3 1 1 5 2" "5 1 1 5 2" "15 1 1 1 2" "21 1 1 1 3"; do set -- $spec; ../../code/search_val "C:$1,$2,$3,$4" $5 2 nohalve >/dev/null; sort "found_C_$1_$2_$3_$4_k$5.txt" > c.txt; python3 -I ../../code/brute.py $spec 2>/dev/null | sort > p.txt; echo "$spec C=$(wc -l <c.txt) py=$(wc -l <p.txt) $(cmp -s c.txt p.txt && echo MATCH || echo DIFF)"; done) > out/validate/validate_rerun.log
