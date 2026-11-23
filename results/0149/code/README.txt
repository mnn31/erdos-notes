g4.c      : cc -O2 -march=native -o g4 g4.c   (modes: expand [OP=0|1|2|3|4], merge [RECANON=1], sq [THRESH,NODELIM,REPORT])
g4b       : same source after adding THRESH (built from the current g4.c)
driver.py : python3 -I driver.py <outdir> <nmax> <workers> [start]   builds out/levels/all<n>.bin
satcheck.py, sat_le.py : independent SAT check (networkx + pysat CaDiCaL)
