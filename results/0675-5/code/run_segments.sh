#!/bin/sh
# usage: run_segments.sh NSTART LO HI NSEG OUTDIR
# Runs lshift on NSEG disjoint t-ranges of [LO,HI] in parallel (NMAX=80, Q0=3000).
NS=$1; LO=$2; HI=$3; K=$4; OD=$5; D=$(dirname "$0")
STEP=$(python3 -I -c "print(($HI-$LO)//$K+1)")
i=0
while [ $i -lt $K ]; do
  a=$(python3 -I -c "print($LO+$i*$STEP)"); b=$(python3 -I -c "print(min($HI,$LO+($i+1)*$STEP-1))")
  "$D/lshift" 80 $b 3000 $NS $a > "$OD/seg_${NS}_$a.out" 2> "$OD/seg_${NS}_$a.err" &
  i=$((i+1))
done
wait
