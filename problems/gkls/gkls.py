from modules.utility.point import Point
from modules.utility.problem import Problem
from problems.gkls.gkls_function import GKLSClass, GKLSFunction


class GKLS(Problem):
    def __init__(self, 
                 function_number: int,
                 dimension: int = 3):
        super().__init__()
        self.name = f"GKLS {function_number}"
        self.function = GKLSFunction()
        self.function.SetDimension(dimension)
        self.function.SetFunctionClass(GKLSClass.Simple, dimension)
        self.function.SetFunctionNumber(function_number)
        self.dim = dimension
        self.lower_bound = [-1.0] * dimension
        self.upper_bound = [1.0] * dimension
        self.optimum = Point(0.,
                             self.function.GetOptimumPoint(),
                             self.function.GetOptimumValue()
                             )

    def calculate(self, point: list[float]) -> float:
        value = self.function.Calculate(point)
        return value
    