# count labelled partitions of E(K7) into 8 matchings (classes unordered): canonical order = class containing smallest remaining edge
import itertools, sys
n=7
E=list(itertools.combinations(range(n),2)); eid={e:i for i,e in enumerate(E)}
vm=[ (1<<a)|(1<<b) for a,b in E]
# all matchings as edge bitmasks with vertex masks
M=[]
for k in (1,2,3):
    for c in itertools.combinations(range(21),k):
        vs=0; ok=True
        for i in c:
            if vs & vm[i]: ok=False;break
            vs|=vm[i]
        if ok: M.append((sum(1<<i for i in c), k))
bylow={}
for m,k in M:
    low=(m & -m).bit_length()-1
    bylow.setdefault(low,[]).append((m,k))
cnt={}
def rec(rem, ncls, sizes):
    if rem==0:
        key=tuple(sorted(sizes)); cnt[key]=cnt.get(key,0)+1; return
    if ncls==8: return
    # need remaining edges <= 3*(8-ncls)
    if bin(rem).count('1')>3*(8-ncls): return
    low=(rem & -rem).bit_length()-1
    for m,k in bylow[low]:
        if m & rem == m:
            rec(rem^m, ncls+1, sizes+[k])
rec((1<<21)-1,0,[])
print(cnt)
