# %%
from utils import *
import os

# Read configuration file
path = "sample_inputs"
file = "sample1.txt"
with open(os.path.join(path, file)) as f:
    input = f.read()

# Extract alphabet and productions from text 
parser = Parser(input)
alphabet = parser.get_alphabet()
productions = parser.get_productions()
for p in productions:
    print(p)

# Define both dependency and independency relations
relation = Relation(productions, alphabet)
print(relation.get_dependencies_str())
print(relation.get_independencies_str())

# Create graph for given word and calculate Foata Normal Form
word = parser.get_word()
graph = Graph(relation, word)
print(graph.FNF())
print(graph)

# Draw dependency graph from dot format and save it as png file
# To run this part installation of graphviz module is required
# `pip install graphviz`

# import graphviz
# filename = file.split(".")[0]
# viz = graphviz.Source(str(graph), filename="graph", format="png")
# viz.view()
