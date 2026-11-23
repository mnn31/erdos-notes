import sys
def inE_small(m):
    # direct: m = x^2+y^2 ?
    x=0
    while x*x<=m:
        y2=m-x*x; y=int(y2**0.5)
        while y*y>y2: y-=1
        while (y+1)*(y+1)<=y2: y+=1
        if y*y==y2: return True
        x+=1
    return False
def S(n): return [a for a in range(1,n+1) if inE_small(a)]
def v(m,q):
    c=0
    while m%q==0: m//=q; c+=1
    return c
def allowed(n,q,k):
    M=q**k; Sn=S(n); out=[]
    for r in range(M):
        ok=True
        for a in Sn:
            m=(r+a)%M
            if m==0: continue
            e=v(m,q)
            if q==2:
                if e<=k-2 and ((m>>e)&3)!=1: ok=False;break
            else:
                if e%2==1: ok=False;break
        if ok: out.append(r)
    return M,out
if __name__=="__main__":
    n=int(sys.argv[1])
    print(len(S(n)), S(n))
    for q,k in [(2,9),(2,10),(2,11),(3,5),(3,6),(7,3),(11,2),(11,3),(19,2),(23,2),(31,2),(43,2)]:
        M,o=allowed(n,q,k); print(q,k,M,len(o),len(o)/M)
