from modules.utility.point import Point
from modules.utility.problem import Problem
from problems.grishagin.grishagin_function import GrishaginFunction


class Grishagin(Problem):
    def __init__(self, function_number: int) -> None:
        super().__init__()
        self.name = f"Grishagin {function_number}"
        self.function = GrishaginFunction(function_number)
        self.dim = 2
        self.lower_bound = [0., 0.]
        self.upper_bound = [1., 1.]
        self.optimum = Point(0.,
                             self.function.GetOptimumPoint(),
                             self.function.Calculate(self.function.GetOptimumPoint())
                             )

    def calculate(self, point: list[float]) -> float:
        value = self.function.Calculate(point)
        return value
