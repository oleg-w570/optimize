from modules.utility.point import Point
from modules.utility.problem import Problem
from modules.utility.parameters import Parameters
from modules.utility.interval import Interval

from modules.evolvent.evolvent import Evolvent


# from modules.evolvent.ctypes.evolvent import Evolvent
# from evolvent_c import Evolvent


class Method:
    def __init__(self,
                 problem: Problem,
                 parameters: Parameters):
        self.problem: Problem = problem
        self.evolvent: Evolvent = Evolvent(problem.lower_bound, problem.upper_bound,
                                           problem.dim,
                                           parameters.evolvent_density)
        self.r: float = parameters.r
        self.m: float = 1
        self.optimum: float = float('inf')

    def update_m(self, m: float) -> bool:
        is_update = m > self.m
        self.m = m if is_update else self.m
        return is_update        

    def update_optimum(self, point: Point) -> bool:
        is_update = point.z < self.optimum
        self.optimum = point.z if is_update else self.optimum
        return is_update

    def delta(self, interval: Interval) -> float:
        rx = interval.right.x
        lx = interval.left.x
        n = self.problem.dim
        return (rx - lx) ** (1 / n)

    @staticmethod
    def lipschitz_const(interval: Interval) -> float:
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

    def first_points(self) -> tuple[Point, Point]:
        lx = 0.0
        ly = self.evolvent.get_image(lx)
        lz = self.problem.f(ly)
        lpoint = Point(lx, ly, lz)

        rx = 1.0
        ry = self.evolvent.get_image(rx)
        rz = self.problem.f(ry)
        rpoint = Point(rx, ry, rz)

        return lpoint, rpoint

    def next_point_coordinate(self, interval: Interval) -> float:
        rx = interval.right.x
        lx = interval.left.x
        m = self.m
        r = self.r
        n = self.problem.dim
        dif = interval.right.z - interval.left.z
        dg = 1.0 if dif > 0 else -1.0
        return 0.5 * (rx + lx) - 0.5 * dg * (abs(dif) / m) ** n / r

    def next_point(self, interval: Interval) -> Point:
        x: float = self.next_point_coordinate(interval)
        y = self.evolvent.get_image(x)
        z: float = self.problem.f(y)
        return Point(x, y, z)

    def split_interval(self,
                       interval: Interval,
                       point: Point
                       ) -> tuple[Interval, Interval]:

        left_interval = Interval(point)
        left_interval.left = interval.left
        # right_interval = Interval(interval.right)
        # right_interval.left = left_interval.right
        interval.left = left_interval.right
            
        left_interval.delta = self.delta(left_interval)
        interval.delta = self.delta(interval)

        return left_interval, interval
