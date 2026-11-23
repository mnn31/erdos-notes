"""Checks each constructed group is a group of the stated order, and prints invariants
(abelian?, element-order histogram) showing groups of equal order are non-isomorphic."""
import sys, collections
SPECS=[("Z31",31,1,1,1),("Z33",33,1,1,1),("Z35",35,1,1,1),("Z37",37,1,1,1),("Z39",39,1,1,1),
 ("Z13:Z3",13,3,3,1),("Z41",41,1,1,1),("Z43",43,1,1,1),("Z45",45,1,1,1),("Z3xZ15",15,1,1,3),("Z47",47,1,1,1),
 ("Z49",49,1,1,1),("Z7xZ7",7,1,1,7),("Z51",51,1,1,1),("Z53",53,1,1,1),("Z55",55,1,1,1),("Z11:Z5",11,5,3,1),
 ("Z57",57,1,1,1),("Z19:Z3",19,3,7,1),("Z59",59,1,1,1),("Z61",61,1,1,1),("Z63",63,1,1,1),("Z3xZ21",21,1,1,3),
 ("Z7:Z9",7,9,2,1),("Z3x(Z7:Z3)",7,3,2,3),("Z65",65,1,1,1),("Z67",67,1,1,1)]
for name,m,k,r,d in SPECS:
    assert pow(r,k,m)==1%m
    els=[(x,y,w) for x in range(m) for y in range(k) for w in range(d)]
    mul=lambda a,b:((a[0]+pow(r,a[1],m)*b[0])%m,(a[1]+b[1])%k,(a[2]+b[2])%d)
    e=(0,0,0)
    S=set(els)
    for a in els:
        for b in els:
            assert mul(a,b) in S
    import random; rnd=random.Random(1)
    for _ in range(20000):
        a,b,c=(rnd.choice(els) for _ in range(3)); assert mul(mul(a,b),c)==mul(a,mul(b,c))
    def order(a):
        x,o=a,1
        while x!=e: x=mul(x,a); o+=1
        return o
    ab=all(mul(a,b)==mul(b,a) for a in els for b in els)
    h=collections.Counter(order(a) for a in els)
    print(f"{name:12s} n={len(els):3d} abelian={ab!s:5s} orders={dict(sorted(h.items()))}")
