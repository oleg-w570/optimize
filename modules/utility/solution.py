from modules.utility.point import Point


class Solution:
    def __init__(self):
        self.trials: list[Point] = []
        self.optimum: Point = Point(float('inf'), float('inf'), float('inf'))
        self.accuracy: float = float('inf')
        self.iterationCount: int = 0


