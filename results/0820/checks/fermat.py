import math
from sympy import isprime, divisors
def H(n):
    l=3
    while True:
        ln=l**n-1
        for k in range(2,l):
            if math.gcd(k**n-1,ln)==1: return l,k
        l+=1
bad=0
for n in range(1,37):
    P=[d+1 for d in divisors(n) if isprime(d+1)]
    prod=math.prod(P)
    l,k=H(n)
    ok=(k*l)%prod==0 and l*l>k*l>=prod
    # also check every coprime pair with l<=H(n)+5 has prod | kl
    for L in range(3,l+6):
        for K in range(2,L):
            if math.gcd(K**n-1,L**n-1)==1 and (K*L)%prod: bad+=1
    print(n,"H=",l,"k=",k,"omega*=",len(P),"prod=",prod,"sqrt=",round(prod**.5,2),ok)
print("violations of prod|kl:",bad)
