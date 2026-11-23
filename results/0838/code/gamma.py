# gamma(rho) = [Phi(rho) + rho^2 Phi(1/rho)] / phi(rho)^2 : the ES-family constant for i/j -> rho.
import math
LN2 = math.log(2)
def phi(x):  # (1+x)log2(1+x) - x log2 x
    return (1+x)*math.log2(1+x) - (x*math.log2(x) if x > 0 else 0.0)
def Phi(y):  # int_0^y phi
    a = (1+y)**2/2*math.log2(1+y) - (1+y)**2/(4*LN2) + 1/(4*LN2)
    b = (y**2/2*math.log2(y) - y**2/(4*LN2)) if y > 0 else 0.0
    return a - b
def gamma(r): return (Phi(r) + r*r*Phi(1/r))/phi(r)**2
# sanity: Phi via numeric quadrature
def Phi_num(y, N=200000):
    h = y/N; return sum(phi((k+0.5)*h) for k in range(N))*h
for y in (0.3, 1.0, 2.5):
    print(f"Phi({y}) closed={Phi(y):.10f} numeric={Phi_num(y):.10f}")
print("I = Phi(1) =", Phi(1), " 2-1/(2ln2) =", 2-1/(2*LN2))
print("gamma(1) =", gamma(1), " 1-1/(4ln2) =", 1-1/(4*LN2))
best = min((gamma(math.exp(t/10000)), math.exp(t/10000)) for t in range(-40000, 40001))
print("min over rho in [e^-4,e^4] (grid step 1e-4 in log rho): gamma=%.10f at rho=%.6f" % best)
for r in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 2, 5, 20):
    print(f"rho={r:6}: gamma={gamma(r):.6f}")
