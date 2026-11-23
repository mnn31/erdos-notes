# driver: build levels n=5..NMAX of ALL 4-regular graphs (canonical, binary uint32 rows)
import sys, os, subprocess, numpy as np
from concurrent.futures import ThreadPoolExecutor
CODE=os.path.dirname(os.path.abspath(__file__)); G4=os.path.join(CODE,'g4')
OUT=sys.argv[1]; NMAX=int(sys.argv[2]); NW=int(sys.argv[3]); START=int(sys.argv[4]) if len(sys.argv)>4 else 6
def fn(n): return os.path.join(OUT,f'all{n}.bin')
def load(n): return np.fromfile(fn(n),dtype=np.uint32).reshape(-1,n)
def conn(rows):
    n=len(rows); seen={0}; st=[0]
    while st:
        v=st.pop()
        for j in range(n):
            if rows[v]>>j&1 and j not in seen: seen.add(j); st.append(j)
    return len(seen)==n
if START==6:
    k5=np.array([0b11111 & ~(1<<i) for i in range(5)],dtype=np.uint32); k5.tofile(fn(5))
for n in range(START,NMAX+1):
    def work(w):
        return subprocess.run([G4,'expand',fn(n-1),str(n-1),os.path.join(OUT,f'tmp{n}_{w}.bin'),str(w),str(NW)],capture_output=True,text=True).stderr
    def work2(args):
        op,w=args; src=n-1-op if op<3 else n-5
        return subprocess.run([G4,'expand',fn(src),str(src),os.path.join(OUT,f'tmp{n}_{op}_{w}.bin'),str(w),str(NW)],env=dict(os.environ,OP=str(op)),capture_output=True,text=True).stderr
    jobs=[(op,w) for op in (0,1,2,4) if (n-1-op if op<3 else n-5)>=5 for w in range(NW)]
    with ThreadPoolExecutor(NW) as ex: list(ex.map(work2,jobs))
    ins=[os.path.join(OUT,f'tmp{n}_{op}_{w}.bin') for op,w in jobs]
    # disjoint unions: connected comp of size a (5..n-5) + any 4-reg graph on n-a
    U=[]
    for a in range(5,n-4):
        A=[r for r in load(a) if conn(list(map(int,r)))]
        B=load(n-a)
        for ra in A:
            for rb in B:
                rows=[int(x) for x in ra]+[int(x)<<a for x in rb]
                U.append(rows)
    if U:
        uf=os.path.join(OUT,f'union{n}.bin'); np.array(U,dtype=np.uint32).tofile(uf)
        ucf=os.path.join(OUT,f'unionc{n}.bin')
        subprocess.run([G4,'merge',str(n),ucf,uf],env=dict(os.environ,RECANON='1'),capture_output=True)
        ins.append(ucf)
    r=subprocess.run([G4,'merge',str(n),fn(n)]+ins,capture_output=True,text=True)
    print(r.stdout.strip(),flush=True)
    for f in ins: os.remove(f)
    if U: os.remove(uf)
