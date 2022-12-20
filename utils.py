from typing import List
from dataclasses import dataclass
import re
from task import Task


@dataclass
class FNF:
    """
    Class that represents Foata Normal Form.

    classes - list of classes that compose Foata Normal Form
    """

    classes: List[List[Task]]

    def __str__(self) -> str:
        return "FNF([w]) = " + "".join(
            ["(" + ",".join(map(str, c)) + ")" for c in self.classes]
        )


class Relation:
    """
    Class that defines relations of dependency and independency given productions and the alphabet.
    """

    def __init__(self, productions: List[Task], alphabet: List[Task]) -> None:
        # pairs of symbols from the alphabet that define relations
        self.D = set()
        self.I = set()

        # determine dependency relation from definition
        # for every combination of productions check if any output from
        # the first production is used as an input or output in the second production
        for x in productions:
            for y in productions:
                if any(symbol in y.all for symbol in x.outputs) or any(
                    symbol in x.all for symbol in y.outputs
                ):
                    self.D.add((x, y))
                else:
                    self.I.add((x, y))

        # if any symbol is in the alphabet but is not used in productions
        # it is still dependent on itself
        for symbol in alphabet:
            self.D.add((symbol, symbol))
            # TODO add independencies

    def dependent(self, a: Task, b: Task):
        """Check if two symbols are in the dependency relation"""
        return (a, b) in self.D

    def to_dependency_str(self):
        """Return string representation of dependency relation"""
        d = [f"({a},{b})" for a, b in sorted(list(self.D))]
        return "D = {" + ",".join(d) + "}"

    def to_independency_str(self):
        """Return string representation of independency relation"""
        i = [f"({a},{b})" for a, b in sorted(list(self.I))]
        return "I = {" + ",".join(i) + "}"


class Graph:
    """Dependency graph calculated from dependency relation for a given word"""

    def __init__(self, relation: Relation, word: List[Task]) -> None:
        self.word = word
        self.relation = relation

        # directed graph represented as two dimensional array
        self.g = [[False for _ in word] for _ in word]

        n = len(word)

        # helper dictionary that stores information which other nodes
        # are already connected with the given node
        visited = {id: {id} for id in range(n)}

        # The word defines the order of tasks that are to be executed.
        # Any task can not be dependent on the task that comes after it
        # in that order. To construct the minimal dependency graph for
        # every node dependency is checked with all the previous nodes in
        # the order of smallest jumps.
        # ex. for nodes 0,1,2,3 the order is: (0,1),(1,2),(0,2),(2,3),(1,3),(0,3), ...
        # This way is if an edge is not redundant it can not become redundant after
        # adding other edges
        # Redundancy is determined by checking if adding an edge would increase the
        # number of available nodes
        for j in range(1, n):
            for i in range(j - 1, -1, -1):
                if relation.dependent(word[i], word[j]):
                    if not visited[i].issubset(visited[j]):
                        self.g[i][j] = True
                        visited[j].update(visited[i])

    def to_FNF(self):
        """
        Determine Foata Normal Form from the dependency graph.
        Performs recursive graph coloring algorithm.
        """
        n = len(self.word)

        # perform graph coloring
        colors = [-1 for _ in range(n)]
        for i in range(n):
            self._color(colors, i, 0)

        # assign symbols to corresponding classes in FNF
        fnf = [[] for _ in range(max(colors) + 1)]
        for i, symbol in enumerate(self.word):
            fnf[colors[i]].append(symbol)

        return FNF(fnf)

    def _color(self, colors, i, color):
        if colors[i] == -1:
            colors[i] = color
            for j in range(i + 1, len(self.word)):
                if self.g[i][j]:
                    self._color(colors, j, color + 1)

    def __str__(self) -> str:
        n = len(self.word)
        edges = []
        for j in range(1, n):
            for i in range(j):
                if self.g[i][j]:
                    edges.append(f"{i+1} -> {j+1}")

        labels = [f"{i+1}[label={str(s)}]" for i, s in enumerate(self.word)]

        return "digraph g{\n" + "\n".join(edges + labels) + "\n}"
