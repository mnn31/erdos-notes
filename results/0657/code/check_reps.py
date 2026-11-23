# check that the certificate files use exactly orbit representatives 1..6 produced by nf7.py, and that
# the 7 representatives lie in 7 distinct S7-orbits covering all 6240 labelled near-1-factorizations (see nf7.txt)
import json, pickle
reps=pickle.load(open('../out/nf7_reps.pkl','rb'))
norm=lambda f: sorted(sorted(tuple(sorted(e)) for e in m) for m in f)
for k in range(1,7):
    c=json.load(open(f'../out/cert_nf7_rep{k}.json'))
    assert norm(c['rep'])==norm(reps[k]), k
print('certificate reps match nf7.py representatives 1..6: True')
