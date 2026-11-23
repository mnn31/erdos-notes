import math
def Fh(x1,x2,x3):
    A2=4*x3**2-(x1-x2)**2; B2=4*x1**2-(x2-x3)**2; AB2=4*x2**2-(x1-x3)**2
    C=AB2-A2-B2
    return 4*A2*B2-C**2, A2,B2,AB2
B=80; sols=[]
for x1 in range(-B,B+1):
  for x2 in range(-B,B+1):
    for x3 in range(1,B+1):
      if math.gcd(math.gcd(x1,x2),x3)!=1: continue
      f,A2,B2,AB2=Fh(x1,x2,x3)
      if f==0 and A2>0 and B2>0 and AB2>0 and x1!=0 and x2!=0:
        sols.append((x1,x2,x3))
print(len(sols)); print(sols[:40])
