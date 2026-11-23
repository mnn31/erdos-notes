import itertools, math
from fractions import Fraction as F
def det(a1,a2,a3):
    e1=a1+a2+a3; e2=a1*a2+a1*a3+a2*a3; e3=a1*a2*a3
    return -5*e1**3+20*e1*e2-49*e3
sols=[]
B=60
for a1 in range(-B,B+1):
  for a2 in range(a1,B+1):
    for a3 in range(a2,B+1):
      if (a1,a2,a3)!=(0,0,0) and det(a1,a2,a3)==0 and math.gcd(math.gcd(a1,a2),a3)==1:
        sols.append((a1,a2,a3))
print(sols[:50], len(sols))
