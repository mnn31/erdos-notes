#!/bin/sh
# Reproduce everything for the delta = 4 computation, 2 <= r <= 40.
# Run from attack/776/t1-retry/prove :   sh code/run_all.sh
set -e
cc -O2 -Wall -o code/check code/check.c
cc -O2 -Wall -fsanitize=undefined -o code/check_ubsan code/check.c

# 1. exhaustive search (Python, exact integers): N(r), certificates, colex witnesses, base cores
python3 -I code/search.py 2 40 out > out/search_stdout.txt

# 2. direct check of every witness block (W) and base core (K)
for r in $(seq 2 40); do ./code/check_ubsan w out/witnesses/wit_r$r.txt; done > out/check_witness.txt 2>&1
echo "witness blocks OK: $(grep -c '^OK W' out/check_witness.txt)  cores OK: $(grep -c '^OK K' out/check_witness.txt)  failures: $(grep -c 'FAIL' out/check_witness.txt || true)"

# 3. independent recomputation of every infeasibility certificate (C, own Kruskal-Katona)
for r in $(seq 7 40); do
  N=$(awk -v r=$r '$1==r{print $2}' out/summary_2_40.txt)
  ./code/check_ubsan i $r $N out/certs/cert_r${r}_n${N}.txt
done > out/check_infeas.txt 2>&1
echo "certificates OK: $(grep -c '^OK INFEAS' out/check_infeas.txt)  failures: $(grep -c 'FAIL' out/check_infeas.txt || true)"

# 4. independent full scan (C): all failing n in [5, 2r+5]
for r in $(seq 2 40); do ./code/check_ubsan s $r $((2*r+5)); done > out/scan_c.txt 2>&1
echo "scan written to out/scan_c.txt"

# 5. Lemma 7/8 sanity demo: explicit tail antichains for n = 2r+6..2r+17
python3 -I code/tail_demo.py out 2 40 12 > out/tail_demo.txt
./code/check_ubsan w out/tail_demo.txt > out/check_tail_demo.txt 2>&1
echo "tail demo: $(tail -1 out/check_tail_demo.txt)"
gzip -f out/tail_demo.txt

# 6. sanity tests (KK brute force, colex, Python-vs-C KK, n=6 brute force)
python3 -I -u code/sanity.py > out/sanity.txt 2>&1
tail -1 out/sanity.txt
