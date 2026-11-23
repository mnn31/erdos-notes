# Factoring helpers: gmpy2 Pollard rho, p-1, ECM (Montgomery, stage 1 + bsgs stage 2).
import gmpy2, random, time, math
from gmpy2 import mpz, gcd, is_prime, invert

def small_primes(B):
    s = bytearray([1])*(B+1); s[0]=s[1]=0
    for i in range(2,int(B**0.5)+1):
        if s[i]: s[i*i::i] = bytearray(len(s[i*i::i]))
    return [i for i in range(B+1) if s[i]]
PR = small_primes(5_000_000)

def ladder(k, X, Z, N, a24):
    # Montgomery ladder, returns k*(X:Z)
    if k == 1: return X, Z
    X1, Z1 = X, Z
    # 2P
    t1=(X+Z)**2 % N; t2=(X-Z)**2 % N; t3=t1-t2
    X2=t1*t2 % N; Z2=t3*(t2+a24*t3) % N
    for bit in bin(k)[3:]:
        # R0=(X1,Z1), R1=(X2,Z2), diff = P
        u=(X1-Z1)*(X2+Z2) % N; v=(X1+Z1)*(X2-Z2) % N
        Xa=Z*((u+v)**2) % N; Za=X*((u-v)**2) % N
        if bit == '1':
            t1=(X2+Z2)**2 % N; t2=(X2-Z2)**2 % N; t3=t1-t2
            X2=t1*t2 % N; Z2=t3*(t2+a24*t3) % N
            X1,Z1=Xa,Za
        else:
            t1=(X1+Z1)**2 % N; t2=(X1-Z1)**2 % N; t3=t1-t2
            X1=t1*t2 % N; Z1=t3*(t2+a24*t3) % N
            X2,Z2=Xa,Za
    return X1, Z1

def xadd(X1,Z1,X2,Z2,Xd,Zd,N):
    u=(X1-Z1)*(X2+Z2) % N; v=(X1+Z1)*(X2-Z2) % N
    return Zd*((u+v)**2) % N, Xd*((u-v)**2) % N
def xdbl(X,Z,N,a24):
    t1=(X+Z)**2 % N; t2=(X-Z)**2 % N; t3=t1-t2
    return t1*t2 % N, t3*(t2+a24*t3) % N

def ecm_curve(N, B1, B2, sigma):
    N = mpz(N); s = mpz(sigma)
    u=(s*s-5) % N; v=4*s % N
    X=pow(u,3,N); Z=pow(v,3,N)
    den = 16*pow(u,3,N)*v % N
    g = gcd(den, N)
    if g != 1: return g
    a24 = pow(v-u,3,N)*(3*u+v) % N * invert(den, N) % N
    for p in PR:
        if p > B1: break
        pk = p
        while pk*p <= B1: pk *= p
        X, Z = ladder(pk, X, Z, N, a24)
    g = gcd(Z, N)
    if g != 1: return g
    # stage 2: bsgs with w=2310
    w = 2310
    bs = [b for b in range(1, w//2, 2) if math.gcd(b, w) == 1]
    # baby steps b*P for odd b
    X2,Z2 = xdbl(X,Z,N,a24)
    baby = {1:(X,Z)}
    pX,pZ = X,Z; qX,qZ = xadd(X,Z,X2,Z2,X,Z,N)  # 3P  (diff P)
    baby[3]=(qX,qZ); prev=(X,Z); cur=(qX,qZ)
    for b in range(5, w//2, 2):
        nx = xadd(cur[0],cur[1],X2,Z2,prev[0],prev[1],N)
        prev, cur = cur, nx
        baby[b] = nx
    BB = [(baby[b][0], baby[b][1]) for b in bs]
    GX,GZ = ladder(w, X, Z, N, a24)
    m0 = max(1, B1 // w)
    cX,cZ = ladder(m0*w, X, Z, N, a24)
    pXg,pZg = ladder((m0-1)*w, X, Z, N, a24) if m0 > 1 else (GX, GZ)  # unused when m0==1 handled below
    acc = mpz(1)
    m = m0
    prevX, prevZ = (ladder((m0-1)*w, X, Z, N, a24) if m0>1 else (None,None))
    while m*w - w//2 <= B2:
        for (bx,bz) in BB:
            acc = acc * (cX*bz - bx*cZ) % N
        # next giant
        if prevX is None:
            nX,nZ = xdbl(cX,cZ,N,a24)  # m0==1: 2wP
        else:
            nX,nZ = xadd(cX,cZ,GX,GZ,prevX,prevZ,N)
        prevX,prevZ = cX,cZ; cX,cZ = nX,nZ; m += 1
    g = gcd(acc, N)
    return g

def pm1(N, B1, extra=1):
    N = mpz(N); a = mpz(3)
    a = pow(a, extra, N)
    for p in PR:
        if p > B1: break
        pk = p
        while pk*p <= B1: pk *= p
        a = pow(a, pk, N)
    return gcd(a-1, N)

def rho(N, iters):
    N = mpz(N)
    for c in (1, 3, 5):
        y = mpz(2); x = y; g = mpz(1); q = mpz(1); r = 1; it = 0
        while g == 1 and it < iters:
            x = y
            for _ in range(r): y = (y*y + c) % N
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(128, r-k)):
                    y = (y*y + c) % N; q = q*abs(x-y) % N
                g = gcd(q, N); k += 128
            r *= 2; it += r
        if g == N:
            g = mpz(1)
            while g == 1:
                ys = (ys*ys + c) % N; g = gcd(abs(x-ys), N)
        if 1 < g < N: return g
    return mpz(1)

def factor_full(N, budget, extra=1, log=None):
    """Returns (primes:list[int] with multiplicity, composites:list[int]). primes are BPSW/MR probable primes."""
    t0 = time.time()
    N = mpz(N); primes = []
    for p in PR[:20000]:   # trial up to ~2.2e5
        while N % p == 0: primes.append(p); N //= p
        if p*p > N: break
    todo = [N] if N > 1 else []; comps = []
    stages = [('pm1', 10**6), ('rho', 200000)] + [('ecm', B1, c) for B1, c in
              [(2000,25),(11000,90),(50000,300),(250000,700),(1000000,1800),(3000000,5000)]]
    while todo:
        n = todo.pop()
        if n == 1: continue
        if is_prime(n, 40): primes.append(int(n)); continue
        r = gmpy2.iroot(n, 2)
        if r[1]: todo += [r[0], r[0]]; continue
        f = None
        for st in stages:
            if time.time() - t0 > budget: break
            if st[0] == 'pm1':
                g = pm1(n, st[1], extra)
                if 1 < g < n: f = g; break
            elif st[0] == 'rho':
                g = rho(n, st[1])
                if 1 < g < n: f = g; break
            else:
                B1, nc = st[1], st[2]
                rnd = random.Random(int(n % 1000003) + B1)
                for _ in range(nc):
                    if time.time() - t0 > budget: break
                    g = ecm_curve(n, B1, 50*B1, rnd.randrange(6, 1 << 62))
                    if 1 < g < n: f = g; break
                if f: break
        if f is None: comps.append(int(n))
        else: todo += [f, n // f]
    return sorted(int(p) for p in primes), comps
