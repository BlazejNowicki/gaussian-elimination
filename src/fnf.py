from dataclasses import dataclass
from typing import List

from src.task import Task


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