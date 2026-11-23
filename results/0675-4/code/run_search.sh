#!/bin/sh
# usage: run_search.sh TMAX NMAX NPROC OUTPREFIX ; splits [1,TMAX] into NPROC chunks, runs in parallel
TMAX=$1; NMAX=$2; NP=$3; OUT=$4
DIR=$(cd "$(dirname "$0")" && pwd)
CH=$(( (TMAX + NP - 1) / NP ))
i=0
while [ $i -lt $NP ]; do
  LO=$(( 1 + i*CH )); HI=$(( 1 + (i+1)*CH )); if [ $HI -gt $((TMAX+1)) ]; then HI=$((TMAX+1)); fi
  "$DIR/shiftsearch" $LO $HI $NMAX > "$OUT.chunk$i" &
  i=$((i+1))
done
wait
