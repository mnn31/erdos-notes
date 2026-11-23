#!/bin/bash
# Reproduce every load-bearing computation. Run from this code/ directory:  bash run_all.sh
set -e
cd "$(dirname "$0")"
python3 -I six_lower.py      > ../out/six_lower.txt      # phi(6) >= 6 : 1-factorizations of K6 + exact identity
python3 -I six_upper.py      > ../out/six_upper.txt      # phi(6) <= 6 : explicit 6 points, exact integer check
python3 -I nf7.py            > ../out/nf7.txt            # near-1-factorizations of K7: 6240 labelled, 7 orbits
python3 -I rep0_comb.py      > ../out/rep0_comb.txt      # combinatorial facts for orbit 0 (hand proof, Lemma 8)
python3 -I check_reps.py > ../out/check_reps.txt
for k in 1 2 3 4 5 6; do python3 -I verify_cert.py ../out/cert_nf7_rep$k.json; done > ../out/verify_certs.txt   # orbits 1..6
python3 -I seven_upper8.py   > ../out/seven_upper8.txt   # phi(7) <= 8 : explicit 7 integer points, exact check
python3 -I five_upper.py     > ../out/five_upper.txt     # phi(5) <= 5 : Krawczyk-certified 5 points (side result)
# certificates for orbits 1..6 were produced by (optional, slow):
#   python3 -I lift.py ../out/nf7_reps.pkl <k> "<target>" 3 ../out/cert_nf7_rep<k>.json
# targets: 1 "d3*(d0-d6)*(d1-d2)"; 2 "d0**2*(d3-d4)"; 3 "d0*d4*d6"; 4,5,6 "d0**3"
