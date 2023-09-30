from modules.evolvent.evolvent import Evolvent
from modules.utility.parameters import Parameters
from modules.utility.point import Point
from modules.utility.interval import Interval
from modules.utility.problem import Problem


class Method:
    def __init__(self,
                 problem: Problem,
                 parameters: Parameters):
        self.problem: Problem = problem
        self.evolvent: Evolvent = Evolvent(problem.lower_bound, problem.upper_bound,
                                           problem.dim,
                                           parameters.evolvent_density)
        self.r = parameters.r
        self.m: float = 1
        self.optimum: float = float('inf')

    def update_holder_const(self, m: float) -> bool:
        is_update = m > self.m
        self.m = m if is_update else self.m
        return is_update        

    def update_optimum(self, point: Point) -> bool:
        is_update = point.z < self.optimum
        self.optimum = point.z if is_update else self.optimum
        return is_update

    @staticmethod
    def holder_const(interval: Interval) -> float:
        rz = interval.right.z
        lz = interval.left.z
        delta = interval.delta
        m = abs(rz - lz) / delta
        if m < 1e-16:
            return 1
        return m

    def characteristic(self, interval: Interval) -> float:
        rz = interval.right.z
        lz = interval.left.z
        delta = interval.delta
        z_opt = self.optimum
        m = self.m
        r = self.r
        return (delta + (rz - lz) * (rz - lz) / (r * r * m * m * delta) -
                2 * (rz + lz - 2 * z_opt) / (r * m))

    def next_point_coordinate(self, interval: Interval) -> float:
        n = self.problem.dim
        rx = interval.right.x
        lx = interval.left.x
        dif = interval.right.z - interval.left.z
        dg = 1.0 if dif > 0 else -1.0
        return 0.5 * (rx + lx) - 0.5 * dg * (abs(dif) / self.m) ** n / self.r

    def next_point(self, interval: Interval) -> Point:
        x = self.next_point_coordinate(interval)
        y = self.evolvent.get_image(x)
        return Point(x, y)

    def delta(self, interval: Interval) -> float:
        rx = interval.right.x
        lx = interval.left.x
        n = self.problem.dim
        return (rx - lx) ** (1 / n)

    def split_interval(self,
                       interval: Interval,
                       point: Point
                       ) -> tuple[Interval, Interval]:

        left_interval = Interval(point)
        left_interval.left = interval.left
        interval.left = left_interval.right

        left_interval.delta = self.delta(left_interval)
        interval.delta = self.delta(interval)

        return left_interval, interval

    def boundary_points(self) -> tuple[Point, Point]:
        lx = 0.0
        ly = self.evolvent.get_image(lx)
        lz = self.problem.calculate(ly)
        lpoint = Point(lx, ly, lz)

        rx = 1.0
        ry = self.evolvent.get_image(rx)
        rz = self.problem.calculate(ry)
        rpoint = Point(rx, ry, rz)

        return lpoint, rpoint

    def evenly_points(self, number: int) -> list[Point]:
        points: list[Point] = []
        step = 1.0 / number
        for i in range(1, number):
            x = step * i
            y = self.evolvent.get_image(x)
            points.append(Point(x, y))
        return points


