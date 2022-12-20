from typing import List
from dataclasses import dataclass
from src.task import Task


class Relation:
    """
    Class that defines relations of dependency and independency given productions and the alphabet.
    """

    def __init__(self, productions: List[Task], alphabet: List[Task]) -> None:
        # pairs of symbols from the alphabet that define relations
        self.D = set()

        # determine dependency relation from definition
        # for every combination of productions check if any output from
        # the first production is used as an input or output in the second production
        for x in productions:
            for y in productions:
                if any(symbol in y.all for symbol in x.outputs) or any(
                    symbol in x.all for symbol in y.outputs
                ):
                    self.D.add((x, y))

        # if any symbol is in the alphabet but is not used in any productions
        # it is dependent on itself and independent on every other task
        for symbol in alphabet:
            self.D.add((symbol, symbol))

        self.I = {(x, y) for x in productions for y in productions} - self.D

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
