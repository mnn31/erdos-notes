# Exact arithmetic in Q(w), w = e^{i pi/3}, w^2 = w - 1.  Element = (x, y) meaning x + y*w, x,y Fractions.
from fractions import Fraction as Fr
Z=(Fr(0),Fr(0)); ONE=(Fr(1),Fr(0)); W=(Fr(0),Fr(1)); WB=(Fr(1),Fr(-1))  # WB = conj(w) = 1 - w
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def neg(a): return (-a[0],-a[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]+a[1]*b[1])
def conj(a): return (a[0]+a[1],-a[1])
def norm(a): return a[0]*a[0]+a[0]*a[1]+a[1]*a[1]          # |a|^2, a rational
def inv(a):
    N=norm(a); c=conj(a); return (c[0]/N,c[1]/N)
def iszero(a): return a[0]==0 and a[1]==0
def re(a): return a[0]+a[1]/2            # real part (rational)
def im_over_r3(a): return a[1]/2         # imaginary part divided by sqrt(3)
def tocomplex(a):
    import math
    return complex(float(a[0])+float(a[1])/2, float(a[1])*math.sqrt(3)/2)
