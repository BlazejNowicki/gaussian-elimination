# %%
from utils import *
from dataclasses import dataclass
import os

M = lambda k, i: f'M{k},{i}'
m = lambda k, i: f'm{k},{i}'
n = lambda k, i, j: f'n{i},{j},{k}'

@dataclass
class A:
    i: int
    k: int

    def __str__(self):
        return f'A{self.i}{self.k}'

    def to_production(self):
        i,k = self.i, self.k
        return Production(str(self), [M(k,i), M(i,i)], [m(k,i)])

@dataclass
class B:
    i: int
    j: int
    k: int

    def __str__(self):
        return f'B{self.i}{self.j}{self.k}'

    def to_production(self):
        i,j,k = self.i, self.j, self.k
        return Production(str(self), [M(i, j), m(k,i)], [n(k,i, j)])

@dataclass
class C:
    i: int
    j: int
    k: int

    def __str__(self):
        return f'C{self.i}{self.j}{self.k}'

    def to_production(self):
        i,j,k = self.i, self.j, self.k
        return Production(str(self), [M(k, j), n(k,i, j)], [M(k,j)])
    

alphabet = []
productions = []
word = []

def add(x):
    alphabet.append(str(x))
    productions.append(x.to_production())
    word.append(str(x))

s = 3
for i in range(1,s):
    for k in range(i+1, s+1):
        add(A(i,k))
        for j in range(i, s+2):
            add(B(i,j,k))
            add(C(i,j,k))

# print(alphabet)
# print(productions)

# Define both dependency and independency relations
relation = Relation(productions, alphabet)
print(relation.get_dependencies_str())
# print(relation.get_independencies_str())

# Create graph for given word and calculate Foata Normal Form
# word = parser.get_word()
graph = Graph(relation, word)
print(graph.FNF())
print(graph)

# Draw dependency graph from dot format and save it as png file
# To run this part installation of graphviz module is required
# `pip install graphviz`

# %%
import graphviz
viz = graphviz.Source(str(graph), filename="graph", format="png")
viz.view()

