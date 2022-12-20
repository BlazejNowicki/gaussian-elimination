from typing import List
from src.task import Task
from src.relation import Relation
from src.fnf import FNF


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