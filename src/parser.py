from typing import List
import numpy as np


class Parser:
    def __init__(self, input_path, output_path) -> None:
        self.input_path = input_path
        self.output_path = output_path

    def load(self) -> np.ndarray:
        matrix: List[List[float]] = []

        with open(self.input_path) as file:
            size = int(next(file))
            for _ in range(size):
                matrix.append(list(map(float, next(file).split())))

            for i, v in enumerate(map(float, next(file).split())):
                matrix[i].append(v)

        return np.asfarray(matrix)

    def dump(self, matrix: np.ndarray):
        with open(self.output_path, "w") as file:
            file.write(f"{matrix.shape[0]}\n")
            file.write("\n".join([" ".join(map(str, row)) for row in matrix[:, :-1]]) + '\n')
            file.write(" ".join(map(str, matrix[:, -1].flatten())) + '\n')
