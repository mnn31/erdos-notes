"""Exact arithmetic used by prove20.py.  Only Python's fractions.Fraction is trusted.

QW  : Q(w), w = e^{i pi/3}, element a + b w, with w^2 = w - 1.
QS  : Q(s), s = sqrt(-3), element a + b s, s^2 = -3.
F   : Q(s, r), r = sqrt(D) (D a positive squarefree integer, or D = 1 meaning r = 1 is
      never used: then the r-part is kept 0), element P + Q r with P, Q in QS.
"""
from fractions import Fraction as Fr


class QW:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fr(a)
        self.b = Fr(b)

    def __add__(self, o):
        return QW(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return QW(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return QW(-self.a, -self.b)

    def __mul__(self, o):
        # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2,  w^2 = w - 1
        a, b, c, d = self.a, self.b, o.a, o.b
        return QW(a * c - b * d, a * d + b * c + b * d)

    def conj(self):
        # conj(w) = 1 - w
        return QW(self.a + self.b, -self.b)

    def norm(self):
        # (a + b w)(a + b - b w) = a^2 + a b + b^2   (rational)
        return self.a * self.a + self.a * self.b + self.b * self.b

    def inv(self):
        n = self.norm()
        assert n != 0
        c = self.conj()
        return QW(c.a / n, c.b / n)

    def __truediv__(self, o):
        return self * o.inv()

    def iszero(self):
        return self.a == 0 and self.b == 0

    def __eq__(self, o):
        return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def to_qs(self):
        # w = (1 + s)/2
        return QS(self.a + self.b / 2, self.b / 2)

    def __repr__(self):
        return f"({self.a}+{self.b}w)"


ZERO = QW(0, 0)
ONE = QW(1, 0)
W = QW(0, 1)
WBAR = QW(1, -1)  # = w^{-1}


class QS:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fr(a)
        self.b = Fr(b)

    def __add__(self, o):
        return QS(self.a + o.a, self.b + o.b)

    def __sub__(self, o):
        return QS(self.a - o.a, self.b - o.b)

    def __neg__(self):
        return QS(-self.a, -self.b)

    def __mul__(self, o):
        return QS(self.a * o.a - 3 * self.b * o.b, self.a * o.b + self.b * o.a)

    def conj(self):
        return QS(self.a, -self.b)

    def iszero(self):
        return self.a == 0 and self.b == 0

    def __eq__(self, o):
        return self.a == o.a and self.b == o.b


class F:
    """P + Q r with r = sqrt(D), D > 1 squarefree integer (r real)."""
    __slots__ = ("P", "Q", "D")

    def __init__(self, P, Q, D):
        self.P, self.Q, self.D = P, Q, D

    def __add__(self, o):
        assert self.D == o.D
        return F(self.P + o.P, self.Q + o.Q, self.D)

    def __sub__(self, o):
        assert self.D == o.D
        return F(self.P - o.P, self.Q - o.Q, self.D)

    def __mul__(self, o):
        assert self.D == o.D
        D = QS(self.D, 0)
        return F(self.P * o.P + D * self.Q * o.Q, self.P * o.Q + self.Q * o.P, self.D)

    def conj(self):  # complex conjugation: s -> -s, r -> r
        return F(self.P.conj(), self.Q.conj(), self.D)

    def abs2(self):
        """|x|^2 as a real element (x0, x1) meaning x0 + x1 sqrt(D)."""
        m = self * self.conj()
        assert m.P.b == 0 and m.Q.b == 0, "abs2 not real"
        return RealQ(m.P.a, m.Q.a, self.D)

    @staticmethod
    def from_qw(q, D):
        return F(q.to_qs(), QS(0, 0), D)

    def to_complex(self):
        import math
        r = math.sqrt(self.D)
        s = math.sqrt(3)
        return complex(float(self.P.a) + float(self.Q.a) * r,
                       float(self.P.b) * s + float(self.Q.b) * s * r)

    def to_mp(self, dps=40):
        import mpmath as mp
        mp.mp.dps = dps
        r = mp.sqrt(self.D)
        s = mp.sqrt(3)
        return (mp.mpf(self.P.a.numerator) / self.P.a.denominator + mp.mpf(self.Q.a.numerator) / self.Q.a.denominator * r,
                (mp.mpf(self.P.b.numerator) / self.P.b.denominator + mp.mpf(self.Q.b.numerator) / self.Q.b.denominator * r) * s)


class RealQ:
    """x0 + x1 sqrt(D), D > 1 squarefree; canonical when x1 == 0 (D ignored)."""
    __slots__ = ("x0", "x1", "D")

    def __init__(self, x0, x1, D):
        self.x0, self.x1, self.D = Fr(x0), Fr(x1), D

    def key(self):
        return (self.x0, self.x1, self.D if self.x1 != 0 else 0)

    def sign(self):
        # exact sign of x0 + x1 sqrt(D)
        a, b, D = self.x0, self.x1, self.D
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if (a > 0) == (b > 0):
            return 1 if a > 0 else -1
        # opposite signs: compare a^2 with D b^2
        if a * a > D * b * b:
            return 1 if a > 0 else -1
        if a * a < D * b * b:
            return 1 if b > 0 else -1
        return 0  # impossible for D non-square, kept for completeness

    def __sub__(self, o):
        if self.x1 != 0 and o.x1 != 0:
            assert self.D == o.D
        D = self.D if self.x1 != 0 else o.D
        return RealQ(self.x0 - o.x0, self.x1 - o.x1, D)

    def __eq__(self, o):
        return (self - o).sign() == 0

    def __repr__(self):
        if self.x1 == 0:
            return f"{self.x0}"
        return f"{self.x0} + ({self.x1})*sqrt({self.D})"

    def __float__(self):
        import math
        return float(self.x0) + float(self.x1) * math.sqrt(self.D)


def squarefree_split(E):
    """E positive rational -> (q, D) with E = q^2 D, q rational > 0, D squarefree positive int."""
    E = Fr(E)
    assert E > 0
    num, den = E.numerator * E.denominator, E.denominator  # E = num / den^2
    # factor num = sq^2 * D
    n = num
    sq = 1
    D = 1
    p = 2
    while p * p <= n:
        while n % (p * p) == 0:
            n //= p * p
            sq *= p
        if n % p == 0:
            n //= p
            D *= p
        p += 1
    D *= n
    return Fr(sq, den), D
