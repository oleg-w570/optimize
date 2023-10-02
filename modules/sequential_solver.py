from time import perf_counter

from modules.core.solver_base import SolverBase
from modules.utility.interval import Interval
from modules.utility.point import Point


class SequentialSolver(SolverBase):
    def solve(self):
        self.first_iteration()
        mindelta: float = float("inf")
        niter: int = 0
        start_time = perf_counter()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            old_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()

            point: Point = self.method.next_point(old_intrvl)
            point.z = self.problem.calculate(point.y)
            new_intrvls = self.method.split_interval(old_intrvl, point)

            new_m = map(self.method.holder_const, new_intrvls)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            self.recalc_characteristics()

            new_r = map(self.method.characteristic, new_intrvls)
            for trial in zip(new_r, new_intrvls):
                self.trial_data.insert(*trial)

            mindelta = old_intrvl.delta
            niter += 1
        self._solution.time = perf_counter() - start_time
        self._solution.accuracy = mindelta
        self._solution.niter = niter
