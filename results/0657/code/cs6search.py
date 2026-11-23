import sympy as sp
a1,a2,a3=sp.symbols('a1 a2 a3')
g=lambda ai,aj,ak:(ai+aj-4*ak)/2
G=sp.Matrix([[a1,g(a1,a2,a3),g(a1,a3,a2)],[g(a1,a2,a3),a2,g(a2,a3,a1)],[g(a1,a3,a2),g(a2,a3,a1),a3]])
D=sp.factor(G.det()); print('det =',D)
