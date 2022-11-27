# %%
from parser import Parser
from utils import *

path = "input2.txt"
with open(path) as f:
    input = f.read()

parser = Parser(input)

alphabet = parser.get_alphabet()
productions = parser.get_productions()
for p in productions:
    print(p)

relation = Relation(productions, alphabet)
word = parser.get_word()
print(relation.get_dependencies_str())
print(relation.get_independencies_str())

graph = Graph(relation, word)
print(graph.FNF())
print(graph)

# import graphviz
# viz = graphviz.Source(str(graph), filename="graph", format="png")
# viz.view()
