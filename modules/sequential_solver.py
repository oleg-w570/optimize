from modules.core.solver import Solver
from modules.utility.point import Point
from modules.utility.intervaldata import IntervalData


class SequentialSolver(Solver):
    def solve(self):
        self.first_iteration()
        mindelta: float = float('inf')
        niter: int = 0
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            intervalt: IntervalData = self.intrvls_queue.get_nowait()
            mindelta = intervalt.delta
            point: Point = self.method.next_point(intervalt)
            new_intervals = self.method.split_interval(intervalt, point)
            new_m = map(self.method.lipschitz_constant, new_intervals)
            self.recalc |= self.method.update_m(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            self.recalculate()

            new_r = map(self.method.characteristic, new_intervals)
            new_intervals = list(map(self.change_r, new_intervals, new_r))
            for interval in new_intervals:
                self.intrvls_queue.put_nowait(interval)
            niter += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = niter
