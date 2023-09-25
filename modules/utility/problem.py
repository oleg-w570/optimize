from abc import ABC, abstractmethod

from modules.utility.point import Point


class Problem(ABC):
    def __init__(self) -> None:
        self.name: str
        self.dim: int
        self.lower_bound: list[float]
        self.upper_bound: list[float]
        self.optimum: Point

    @abstractmethod
    def calculate(self, point: list[float]) -> float:
        pass

    def __repr__(self):
        return (f'{self.name}\n'
                f'Known optimum point: {self.optimum.y}\n'
                f'Known optimum value: {self.optimum.z}')
