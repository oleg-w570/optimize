import math
from modules.utility.point import Point
from modules.utility.problem import Problem
from archive.parameters import Parameters
from modules.utility.intervaldata import IntervalData
from modules.core.evolvent import Evolvent


class Method:
    def __init__(self,
                 problem: Problem,
                 parameters: Parameters):
        self.problem: Problem = problem
        self.evolvent: Evolvent = Evolvent(problem.lowerBound, problem.upperBound, problem.dimension)
        self.r: float = parameters.r
        self.m: float = 1
        self.optimum: float = math.inf

    def CalculateDelta(self, interval: IntervalData):
        rx = interval.right.x
        lx = interval.left.x
        n = self.problem.dimension
        return pow(rx - lx, 1 / n)

    @staticmethod
    def CalculateM(interval: IntervalData) -> float:
        rz = interval.right.z
        lz = interval.left.z
        delta = interval.delta
        m = abs(rz - lz) / delta
        if m < 1e-16:
            return 1
        return m

    def CalculateR(self, interval: IntervalData) -> float:
        rz = interval.right.z
        lz = interval.left.z
        delta = interval.delta
        z_opt = self.optimum
        m = self.m
        r = self.r
        return delta + (rz - lz) * (rz - lz) / (r * r * m * m * delta) - 2 * (rz + lz - 2 * z_opt) / (r * m)

    def FirstPoints(self) -> tuple[Point, Point]:
        lx = 0.0
        ly = self.evolvent.GetImage(lx)
        lz = self.problem.f(ly)
        lpoint = Point(lx, ly, lz)

        rx = 1.0
        ry = self.evolvent.GetImage(rx)
        rz = self.problem.f(ry)
        rpoint = Point(rx, ry, rz)

        return lpoint, rpoint

    def NextPointCoordinate(self, interval: IntervalData) -> float:
        rx = interval.right.x
        lx = interval.left.x
        m = self.m
        r = self.r
        n = self.problem.dimension
        dif = interval.right.z - interval.left.z
        dg = 1.0 if dif > 0 else -1.0
        return 0.5 * (rx + lx) - 0.5 * dg * (abs(dif) / m) ** n / r

    def NextPoint(self, interval: IntervalData) -> Point:
        x: float = self.NextPointCoordinate(interval)
        y = self.evolvent.GetImage(x)
        z: float = self.problem.f(y)
        point: Point = Point(x, y, z)
        return point

    def SplitIntervals(self, interval: IntervalData, point: Point) -> tuple[IntervalData, IntervalData]:
        left_interval = IntervalData(point)
        left_interval.left = interval.left
        right_interval = IntervalData(interval.right)
        right_interval.left = left_interval.right

        left_interval.delta = self.CalculateDelta(left_interval)
        right_interval.delta = self.CalculateDelta(right_interval)

        return left_interval, right_interval
