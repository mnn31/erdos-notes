#!/bin/sh
# Each "neg"/false input below must be REJECTED by code/check; ok_copy must pass.
mkdir -p out/negative
python3 -I code/make_negative.py
for f in out/negative/ok_copy.txt out/negative/core_ok.txt out/negative/neg_*.txt; do echo "== $f"; ./code/check w $f | tail -1; done
echo "== false infeasibility claim r=7 N=11 (must FAIL)"; ./code/check i 7 11 | tail -1
echo "== false infeasibility claim r=11 N=16 (must FAIL)"; ./code/check i 11 16 | tail -1
sed '5s/ [0-9]*$/ 999/' out/certs/cert_r11_n15.txt > out/negative/cert_corrupt.txt
echo "== corrupted certificate value (must FAIL)"; ./code/check i 11 15 out/negative/cert_corrupt.txt | tail -1
sed '$d' out/certs/cert_r11_n15.txt > out/negative/cert_trunc.txt
echo "== truncated certificate (must FAIL)"; ./code/check i 11 15 out/negative/cert_trunc.txt | tail -1
