from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class Task(ABC):
    """
    Class that represents a task.

    name - name of this task
    inputs - variables that production takes as an input
    outputs - variables that are affected by this production
    """

    def __init__(self, name: str, inputs: List[str], outputs: List[str]) -> None:
        super().__init__()

        self._name = name
        self._inputs = inputs
        self._outputs = outputs

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @property
    def inputs(self) -> List[str]:
        return self._inputs

    @property
    def outputs(self) -> List[str]:
        return self._outputs

    @property
    def all(self) -> List[str]:
        return self._inputs + self._outputs

    def __str__(self) -> str:
        return self._name
    
    def __lt__(self, other: object):
        if isinstance(other, Task):
            return self._name < other._name
        raise TypeError(f"Incomparable types: Task and {type(other)}")

