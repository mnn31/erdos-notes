#!/bin/bash
# sweep_one.sh v n m : run run_instance.py for one pair and print a one-line summary.
# Witness files of the sweep are gzip-compressed after verification to save disk.
cd "$(dirname "$0")/.."
v=$1; n=$2; m=$3
[ "$v" -lt 2 ] && exit 0
o=$(python3 -I code/run_instance.py $n $m out/graphs out/sweepw 2>&1)
su=$(echo "$o" | grep 'star union' | awk '{print $NF}')
ar=$(echo "$o" | grep '^e=' | awk '{print $NF}')
wc=$(echo "$o" | grep 'independent' | awk '{print $NF}')
echo "$v $n $m starunion_arrows=$su arrowing_at_v-1=$ar bad_witnesses=$wc"
tag="${n//,/.}_vs_${m//,/.}"
gzip -f out/sweepw/${tag}_e$((v-1))_witnesses.tsv
