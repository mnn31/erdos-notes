#!/bin/sh
# Komlos-Sos sweep: J=ceil(n/2) vertices of degree >= k.
# edge form (LKS, Zhao Conj 1.4): trees with k edges; page form: trees with k vertices (k-1 edges).
cd "$(dirname "$0")/../out"
for n in 2 3 4 5 6 7 8 9 10 11 12; do
  J=$(( (n+1)/2 ))
  for k in $(seq 1 $((n-1))); do
    echo "== n=$n k=$k edge-form (trees with $k edges)"
    ../code/lks $n $J $k $k data/graphs$J.txt data/trees$k.txt 4 3 2>/dev/null
    if [ $k -ge 2 ]; then
      echo "== n=$n k=$k page-form (trees with $k vertices)"
      ../code/lks $n $J $k $((k-1)) data/graphs$J.txt data/trees$((k-1)).txt 4 3 2>/dev/null
    fi
  done
done
