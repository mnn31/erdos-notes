# Exact integer verification: 7 points in Z^2, no isosceles triangle (degenerate included), exactly 8 distinct distances.
import itertools, json
P=[(97241,0),(-97241,0),(-53240,43759),(53240,-43759),(-441,97240),(44000,-53041),(-44000,53041)]
assert len(set(P))==7
D={(i,j):(P[i][0]-P[j][0])**2+(P[i][1]-P[j][1])**2 for i,j in itertools.combinations(range(7),2)}
vals=sorted(set(D.values()))
print('points:',P)
print('number of distinct distances:',len(vals))
for v in vals: print(' ',v,[e for e in D if D[e]==v])
iso=[(a,b,c) for a,b,c in itertools.combinations(range(7),3) if len({D[(a,b)],D[(a,c)],D[(b,c)]})<3]
print('isosceles (incl. degenerate) triples:',iso)
assert not iso and len(vals)==8 and min(vals)>0
rel=min(abs(x-y) for x,y in itertools.combinations(vals,2))/max(vals)
print('min relative gap between distinct squared distances:',rel)
json.dump({'points':P,'squared_distances':{f'{i}-{j}':v for (i,j),v in D.items()}},open('../out/seven_points_8.json','w'),indent=1)
print('OK')
