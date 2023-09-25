from modules.utility.point import Point
from modules.utility.problem import Problem
from problems.shekel.shekel_function import ShekelFunction


class Shekel(Problem):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Shekel"
        self.function = ShekelFunction()
        self.dim = 1
        self.lower_bound = [0.]
        self.upper_bound = [10.]
        self.optimum = Point(0, [0], 0)

    def calculate(self, point: list[float]) -> float:
        value = self.function(point[0])
        return value
    