# Exact verification: 6 points in R^2, no isosceles triangle (incl. degenerate), exactly 6 distinct distances.
# Points (x, c) mean (x, c*sqrt(7)); squared distance = dx^2 + 7*dc^2 is an integer.
import itertools, json
P=[(34,0),(-11,-25),(40,-8),(-34,0),(11,-25),(-40,-8)]
assert len(set(P))==6
sq=lambda p,q:(p[0]-q[0])**2+7*(p[1]-q[1])**2
D={(i,j):sq(P[i],P[j]) for i,j in itertools.combinations(range(6),2)}
vals=sorted(set(D.values()))
print('points (x, y/sqrt7):',P)
print('distinct squared distances:',vals,'count',len(vals))
for v in vals: print(' ',v,[e for e in D if D[e]==v])
iso=[(a,b,c) for a,b,c in itertools.combinations(range(6),3) if len({D[(a,b)],D[(a,c)],D[(b,c)]})<3]
print('isosceles (incl. degenerate) triples:',iso)
assert not iso and len(vals)==6 and min(vals)>0
json.dump({'points_x_and_y_over_sqrt7':P,'squared_distances':{f'{i}-{j}':v for (i,j),v in D.items()}},open('../out/six_points.json','w'),indent=1)
print('OK')
