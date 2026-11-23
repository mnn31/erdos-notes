# Combinatorial facts about near-1-factorization rep 0 of K7 used in the hand proof (Lemma 7):
# (i) for every class and every pair of its edges {ab},{cd}, the quadruple {a,b,c,d} has all three
#     opposite pairs in common classes ("rectangle quadruple"); (ii) every vertex lies in a rectangle quadruple.
import pickle, itertools
f=pickle.load(open('../out/nf7_reps.pkl','rb'))[0]
print('rep 0 classes:',f)
cls={tuple(e):c for c,m in enumerate(f) for e in m}
C=lambda a,b: cls[(min(a,b),max(a,b))]
def rect(q):
    a,b,c,d=q
    return C(a,b)==C(c,d) and C(a,c)==C(b,d) and C(a,d)==C(b,c)
quads=[q for q in itertools.combinations(range(7),4) if rect(q)]
print('rectangle quadruples:',quads)
ok1=all(rect(tuple(sorted(set(e1)|set(e2)))) for m in f for e1,e2 in itertools.combinations(m,2))
ok2=all(any(v in q for q in quads) for v in range(7))
print('(i) every same-class edge pair spans a rectangle quadruple:',ok1)
print('(ii) every vertex lies in a rectangle quadruple:',ok2)
assert ok1 and ok2
