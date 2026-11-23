from sympy import factorint, symbols, expand
import math
def inE(m):
    return m>=1 and all(e%2==0 for p,e in factorint(m).items() if p%4==3)
def L(t,cap=80):
    for a in range(1,cap+1):
        if inE(a)!=inE(a+t): return a-1
    return cap
tab={1:1,3:3,16:4,48:7,96:8,2304:12,40320:16,173376:17,1761984:24,10269504:31,755048448:36,87196919040:39,159488372736:40,
3993737134464:44,34647247514880:48,2312113913214336:51,7504125968199168:52}
for t,l in tab.items():
    Lt=L(t); a=Lt+1
    print(t, Lt, Lt==l, "fail a=",a, inE(a), inE(a+t), factorint(t))
for n,t in [(52,7504125968199168),(49,2312113913214336),(40,159488372736)]:
    print(n, math.log(t), math.log(t)/n)
v=symbols('v'); t=4*v**2*(v**2-1)
print(expand(t+1-(2*v**2-1)**2), expand(t+2-(2*v**2-1)**2-1), expand(t+4-(2-2*v**2)**2-(2*v)**2), expand(t+5-(2*v**2-1)**2-4))
from collections import Counter
c=Counter()
for k in range(1,301):
    vv=21*k; T=4*vv*vv*(vv*vv-1); c[L(T,40)]+=1
print(sorted(c.items()))
# Lemma G boundary: is 21|v needed? try v=3*7 multiples vs failures for v not multiple
print([ (vv, L(4*vv*vv*(vv*vv-1),20)) for vv in range(2,30)])
