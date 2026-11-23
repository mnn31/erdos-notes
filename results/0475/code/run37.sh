#!/bin/sh
cd compute/475/code
./g475 37 21 33 0 11 ../out/hard_m0.txt > ../out/p37_t21-33_m0.txt
./g475 37 13 20 0 11 ../out/hard_m0.txt > ../out/p37_t13-20_m0.txt
./g475 37 1 12 0 11 ../out/hard_m0.txt > ../out/p37_t1-12_m0.txt
./g475 37 34 36 0 11 ../out/hard_m0.txt > ../out/p37_t34-36_m0.txt
echo DONE > ../out/p37.done
