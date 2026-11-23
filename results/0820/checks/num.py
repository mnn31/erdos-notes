import math
phi=(1+5**.5)/2
def f(theta,t):
    return (t*math.log(t)-(t-theta)*math.log(t-theta)-theta*math.log(theta))/(t+1-theta) if t>theta else theta*math.log(1/theta)/(1)  # t=theta limit
# 1. maximize f_{1/2} on [1/2, 50] by golden section after grid
for theta in (0.5,0.4736):
    ts=[theta+1e-9+i*1e-4 for i in range(1,200000)]
    best=max(ts,key=lambda t:f(theta,t))
    print("theta",theta,"argmax~",round(best,5),"max",f(theta,best))
u=(3+5**.5)/4
print("u",u,"f_1/2(u)",f(.5,u),"log phi",math.log(phi), "diff",f(.5,u)-math.log(phi))
print("0.6736 log2",0.6736*math.log(2))
# 2. C formula
C=0.5*math.log(2*u)+(u-.5)*math.log(2*u/(2*u-1))
print("C",C,"(u+1/2)log phi",(u+.5)*math.log(phi), "2u=phi^2?",2*u-phi**2,"2u/(2u-1)=phi?",2*u/(2*u-1)-phi)
# entropy form: u*H(1/(2u))
r=1/(2*u); H=-r*math.log(r)-(1-r)*math.log(1-r); print("u*H(1/2u)",u*H)
# 3. f_{1/2}(t) equals t*H(1/(2t))/(t+1/2)? i.e. Section-4 formula consistent with GRH branch C/(u+1/2)
for t in (0.8,1.0,u,2.0):
    r=0.5/t; H=-r*math.log(r)-(1-r)*math.log(1-r); print(t, f(.5,t), t*H/(t+.5))
