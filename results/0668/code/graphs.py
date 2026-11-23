# graph6 decoding + the three AMP25 graphs (codes copied from task brief / AMP25 Table 3)
def dec(s):
    d=[ord(c)-63 for c in s]
    n=d[0]; bits=[]
    for x in d[1:]:
        for k in range(5,-1,-1): bits.append((x>>k)&1)
    E=[];i=0
    for j in range(1,n):
        for a in range(j):
            if bits[i]: E.append((a,j))
            i+=1
    return n,E
CODES={13:'L@rLaDBIOidEDJ',15:'NGECKA@WW{igRHKpDSW',16:'O@iib@`cC_iOAsAi_ioHZ'}
U={13:30,15:37,16:41}
def adjacency(n,E):
    adj=[set() for _ in range(n)]
    for a,b in E: adj[a].add(b); adj[b].add(a)
    return adj
def triangles(n,E):
    adj=adjacency(n,E)
    return sorted({tuple(sorted((a,b,c))) for a,b in E for c in adj[a]&adj[b]})
def four_cycles(n,E):
    # 4-cycles a-b-c-d-a returned as (a,b,c,d) with a<c, b<d, a=min
    adj=adjacency(n,E); out=set()
    for a in range(n):
        for c in range(a+1,n):
            com=sorted(adj[a]&adj[c])
            for i in range(len(com)):
                for j in range(i+1,len(com)):
                    b,d=com[i],com[j]
                    cyc=(a,b,c,d)
                    # canonical: rotate so min first
                    out.add(frozenset([(a,c),(b,d)]))
    res=[]
    for fs in out:
        (a,c),(b,d)=sorted(fs)
        res.append((a,b,c,d))
    return sorted(res)
