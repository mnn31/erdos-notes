# Independent check (sympy factorint, Fermat characterisation) of every record t found by lshift/brute:
# prints L(t) = largest n such that t is an n-shift, i.e. a in E <=> a+t in E for 1<=a<=n.
# run: python3 -I code/verify_shifts.py
from sympy import factorint
def inE(m):
    return m >= 1 and all(e % 2 == 0 for p, e in factorint(m).items() if p % 4 == 3)
def L(t, cap=80):
    for a in range(1, cap + 1):
        if inE(a) != inE(a + t): return a - 1
    return cap
records = [1,3,16,48,96,2304,40320,173376,1761984,10269504,755048448,87196919040,159488372736,
           3993737134464,34647247514880,2312113913214336,7504125968199168,8830680626275200]
for t in records:
    l = L(t); a = l + 1
    print(f"t = {t:>20d}  L(t) = {l:2d}   fails at a = {a}: a in E = {inE(a)}, a+t in E = {inE(a+t)}; "
          f"t = {factorint(t)}")
