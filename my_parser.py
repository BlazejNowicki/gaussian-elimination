from typing import List
import numpy as np


class Parser:
    def __init__(self, filename) -> None:
        self.filename = filename

    def load(self) -> np.ndarray:
        matrix: List[List[float]] = []

        with open(self.filename) as file:
            size = int(next(file))
            for _ in range(size):
                matrix.append(list(map(float, next(file).split())))
        
            for i, v in enumerate(map(float, next(file).split())):
                matrix[i].append(v)
        
        return np.asfarray(matrix)