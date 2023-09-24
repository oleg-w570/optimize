from modules.utility.point import Point


class Solution:
    def __init__(self):
        self.points: list[Point] = []
        self.optimum: Point = Point(float('inf'), [float('inf')], float('inf'))
        self.accuracy: float = float('inf')
        self.niter: int = 0
        self.time: float = 0


