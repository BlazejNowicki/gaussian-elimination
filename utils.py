from typing import List
from dataclasses import dataclass


@dataclass
class Transaction:
    name: str
    inputs: List[str]
    outputs: List[str]

    @property
    def all(self):
        return self.inputs + self.outputs


@dataclass
class FNF:
    classes: List[List[str]]

    def __str__(self) -> str:
        return "FNF([w]) = " + "".join(["(" + "".join(c) + ")" for c in self.classes])


class Relation:
    def __init__(self, transactions: List[Transaction]) -> None:
        self.transactions = transactions
        self.D = []
        self.I = []

        for x in transactions:
            for y in transactions:
                if any(symbol in y.all for symbol in x.outputs) or any(
                    symbol in x.all for symbol in x.outputs
                ):
                    self.D.append((x.name, y.name))
                else:
                    self.I.append((x.name, y.name))

    def get_alphabet(self):
        return list(map(lambda x: x.name, self.transactions))

    def get_dependencies(self):
        return self.D.copy()

    def get_independencies(self):
        return self.I.copy()


class Graph:
    def __init__(self, relation: Relation, word: str) -> None:
        alphabet = relation.get_alphabet()
        self.g = [[False for _ in alphabet] for _ in alphabet]
        n = len(alphabet)

        # zle
        # for x, y in relation.get_dependencies():
        #     self.g[x][y] = True

        visited = {id: set(id) for id in range(n)}
        for j in range(1, n):
            for i in range(j):
                # jeśli jest krawędź to sprawdzamy czy ma być
                # if visited[]
                pass
