# Toy runs of the same branch enumeration on the other single-graph cases n=5,7,9,10,12,20 (AMP25 Table 3 codes).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graphs import dec
from branch_enum import run
codes={5:'DR{',7:'FoSvw',9:'H{dQXgj',10:'IISpZATaw',12:'KwC[KLQIibDJ',20:'S?E@cQHWB?_Q?bDPAcYWKM_BC?OAiW@T['}
for n,c in codes.items():
    _,E=dec(c); T,C4,M0,st,pl=run(n,E)
    print('n=%d |E|=%d triangles=%d 4-cycles=%d nodes=%d pruned=%d leaves=%d kernel dims=%s'%(n,len(E),len(T),len(C4),st['nodes'],st['pruned'],len(st['leaves']),[n-len(M.rows) for s,M in st['leaves']]))
    sys.stdout.flush()
