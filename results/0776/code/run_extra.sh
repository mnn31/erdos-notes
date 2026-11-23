#!/bin/sh
# Optional: same pipeline for 41 <= r <= 61 (largest r with 2r+5 <= 127, the bitmask limit).
# Run from attack/776/t1-retry/prove :   sh code/run_extra.sh      (about 10-15 min)
set -e
E=out/extra_41_61
cc -O2 -Wall -o code/check code/check.c
python3 -I code/search.py 41 61 $E > $E/search_stdout.txt
for r in $(seq 41 61); do ./code/check w $E/witnesses/wit_r$r.txt; done > $E/check_witness.txt 2>&1
for r in $(seq 41 61); do
  N=$(awk -v r=$r '$1==r{print $2}' $E/summary_41_61.txt)
  ./code/check i $r $N $E/certs/cert_r${r}_n${N}.txt
done > $E/check_infeas.txt 2>&1
echo "W ok $(grep -c '^OK W' $E/check_witness.txt)  K ok $(grep -c '^OK K' $E/check_witness.txt)  W/K fail $(grep -c FAIL $E/check_witness.txt || true)  certs ok $(grep -c '^OK INFEAS' $E/check_infeas.txt)"
gzip -f $E/witnesses/*.txt
