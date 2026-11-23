import numpy as np
def vals(x1,x2,x3):
    A2=4*x3**2-(x1-x2)**2; B2=4*x1**2-(x2-x3)**2; AB2=4*x2**2-(x1-x3)**2
    C=AB2-A2-B2
    return A2,B2,AB2,C
res=[]
rng=np.random.default_rng(0)
for x1 in np.linspace(-3,3,241):
  for x2 in np.linspace(-3,3,241):
    x3=1.0
    A2,B2,AB2,C=vals(x1,x2,x3)
    if A2>0 and B2>0 and AB2>0:
        F=4*A2*B2-C**2
        res.append((x1,x2,F))
res=np.array(res); print(len(res))
# look for sign changes of F on the grid -> curve passes through feasible region
s=np.sign(res[:,2]); print('pos',np.sum(s>0),'neg',np.sum(s<0))
