from typing import List
from dataclasses import dataclass


@dataclass
class Production:
    name: str
    inputs: List[str]
    outputs: List[str]

    @property
    def all(self):
        return self.inputs + self.outputs

    def __str__(self):
        return (
            f"({self.name}) "
            + ", ".join(self.outputs)
            + " <- "
            + ", ".join(self.inputs)
        )


@dataclass
class FNF:
    classes: List[List[str]]

    def __str__(self) -> str:
        return "FNF([w]) = " + "".join(["(" + "".join(c) + ")" for c in self.classes])


class Relation:
    def __init__(self, productions: List[Production], alphabet: List[str]) -> None:
        self.transactions = productions
        self.D = set()
        self.I = set()

        for x in productions:
            for y in productions:
                if any(symbol in y.all for symbol in x.outputs) or any(
                    symbol in x.all for symbol in y.outputs
                ):
                    self.D.add((x.name, y.name))
                else:
                    self.I.add((x.name, y.name))

        for symbol in alphabet:
            self.D.add((symbol, symbol))

    def is_dependent(self, a: str, b: str):
        return (a, b) in self.D

    def get_dependencies_str(self):
        d = [f"({a},{b})" for a, b in sorted(list(self.D))]
        return "D = {" + ",".join(d) + "}"

    def get_independencies_str(self):
        i = [f"({a},{b})" for a, b in sorted(list(self.I))]
        return "I = {" + ",".join(i) + "}"


class Graph:
    def __init__(self, relation: Relation, word: str) -> None:
        self.word = word
        self.relation = relation
        self.g = [[False for _ in word] for _ in word]
        n = len(word)
        visited = {id: {id} for id in range(n)}

        for j in range(1, n):
            for i in range(j - 1, -1, -1):
                if relation.is_dependent(word[i], word[j]):
                    if not visited[i].issubset(visited[j]):
                        self.g[i][j] = True
                        visited[j].update(visited[i])

    def FNF(self):
        n = len(self.word)
        colors = [-1 for _ in range(n)]
        for i in range(n):
            self._color(colors, i, 0)
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

        labels = [f"{i+1}[label={s}]" for i, s in enumerate(self.word)]

        return "digraph g{\n" + "\n".join(edges + labels) + "\n}"
