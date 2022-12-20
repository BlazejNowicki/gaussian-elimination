# %%
from my_parser import Parser
from scheduler import Scheduler
from utils import *
import numpy as np

# TODO restructure
# TODO report
# TODO parser dump


# Variable definitions
M = lambda k, i: f"M{k},{i}"
m = lambda k, i: f"m{k},{i}"
n = lambda k, i, j: f"n{i},{j},{k}"


class A(Task):
    def __init__(self, i: int, k: int) -> None:
        super().__init__(f"A{i}{k}", [M(k, i), M(i, i)], [m(k, i)])
        self.ik = (i, k)

    def run(self, *args, **kwargs):
        M: np.ndarray = kwargs["M"]
        m: np.ndarray = kwargs["m"]
        i, k = self.ik

        m[k - 1, i - 1] = M[k - 1, i - 1] / M[i - 1, i - 1]


class B(Task):
    def __init__(self, i, j, k) -> None:
        super().__init__(f"B{i}{j}{k}", [M(i, j), m(k, i)], [n(k, i, j)])
        self.ijk = (i, j, k)

    def run(self, *args, **kwargs):
        M: np.ndarray = kwargs["M"]
        m: np.ndarray = kwargs["m"]
        n: np.ndarray = kwargs["n"]
        i, j, k = self.ijk

        n[k-1, i-1, j-1] = M[i-1, j-1] * m[k-1, i-1]


class C(Task):
    def __init__(self, i, j, k) -> None:
        super().__init__(f"C{i}{j}{k}", [M(k, j), n(k, i, j)], [M(k, j)])
        self.ijk = (i, j, k)

    def run(self, *args, **kwargs):
        M: np.ndarray = kwargs["M"]
        n: np.ndarray = kwargs["n"]
        i, j, k = self.ijk

        M[k-1, j-1] = M[k-1,j-1] - n[k-1, i-1, j-1]
        print(M, end='\n\n')

# %%

alphabet = []
productions = []
word = []


def add(x):
    alphabet.append(x)
    productions.append(x)
    word.append(x)


size = 3
for i in range(1, size):
    for k in range(i + 1, size + 1):
        add(A(i, k))
        for j in range(i, size + 2):
            add(B(i, j, k))
            add(C(i, j, k))

relation = Relation(productions, alphabet)

# Create graph for given word and calculate Foata Normal Form
graph = Graph(relation, word)
fnf = graph.to_FNF()
print(fnf)


# %% 

M = Parser("in.txt").load()
n = np.zeros((M.shape[0], M.shape[1], M.shape[1]))
m = np.zeros_like(M)

print(M)

Scheduler(fnf).run(M=M, n=n, m=m)

for i in range(M.shape[0]):
    M[i, :] = M[i, :] / M[i, i]

for i in range(M.shape[0]-1, 0, -1):
    for j in range(i):
        M[j, :] = M[j, :] - M[i, :] * (M[j, i] / M[i, i])

print(M)

# %% 
import graphviz
viz = graphviz.Source(str(graph), filename="graph", format="png")
viz.view()
