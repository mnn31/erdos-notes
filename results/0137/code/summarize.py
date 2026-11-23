# Summarize worker outputs: totals, HIT lines, PAIR list vs A060355 b-file (terms below X).
import sys, glob
d=sys.argv[1]; X=int(float(sys.argv[2])) if 'e' in sys.argv[2] else int(sys.argv[2]); bfile=sys.argv[3]
tot={}; pairs=[]; hits=[]
for f in sorted(glob.glob(d+'/w*.txt')):
    for line in open(f):
        if line.startswith('STATS'):
            for tok in line.split()[1:]:
                if ':' in tok:
                    k,rest=tok.split(':')
                    for kv in rest.split(','):
                        a,b=kv.split('='); tot[k+'_'+a]=tot.get(k+'_'+a,0)+int(b)
                else:
                    a,b=tok.split('='); tot[a]=tot.get(a,0)+int(b)
        elif line.startswith('PAIR'): pairs.append(int(line.split()[1]))
        elif line.startswith('HIT'): hits.append(line.strip())
pairs=sorted(set(pairs))
bf=[int(l.split()[1]) for l in open(bfile) if l.strip() and not l.startswith('#')]
# a pair (m,m+1) is found iff its odd member <= X
exp=sorted(m for m in bf if (m if m%2 else m+1)<=X)
print("totals",tot); print("hits",hits)
print("pairs found",len(pairs),"b-file pairs with odd member <= X:",len(exp),"identical:",pairs==exp)
print("extra (not in b-file):",sorted(set(pairs)-set(exp)),"missing:",sorted(set(exp)-set(pairs)))
