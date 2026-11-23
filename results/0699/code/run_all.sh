#!/bin/sh
# Merge factor files and run both family searches.
cd "$(dirname "$0")/../out"
cat fac_small.jsonl factors_pass1_large.jsonl factors_pass2.jsonl $EXTRA > factors_merged.jsonl
THREADS=${THREADS:-11} python3 -I ../code/search.py 3 40 150 factors_merged.jsonl fam3_m40_150.jsonl
THREADS=${THREADS:-11} python3 -I ../code/search.py 2 63 300 factors_merged.jsonl fam2_k63_300.jsonl
