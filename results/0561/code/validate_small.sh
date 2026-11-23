#!/bin/bash
# Validation on instances whose value is known from refereed sources (see WRITEUP.md, Section 3).
cd "$(dirname "$0")/.."
while read a b; do python3 -I code/run_instance.py $a $b out/graphs out/runs; done <<'L'
2 2
1,1 1,1
3 3
2 2,2
2,2 2,2
3,1 3,1
2,2 3,2
2,2,2 2
L
