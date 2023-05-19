import math
from modules.utility.point import Point
class Solution:
    def __init__(self):
        self.trials: list[Point] = []
        self.optimum: Point = Point(math.inf, math.inf, math.inf)
        self.accuracy: float = math.inf
        self.iterationCount: int = 0


