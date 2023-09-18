from modules.core.solver import Solver
from modules.utility.point import Point
from modules.utility.interval import Interval


class SequentialSolver(Solver):
    def solve(self):
        self.first_iteration()
        mindelta: float = float('inf')
        niter: int = 0
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            old_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()
            mindelta = old_intrvl.delta

            point: Point = self.method.next_point(old_intrvl)
            new_intrvls = self.method.split_interval(old_intrvl, point)

            new_m = map(self.method.lipschitz_const, new_intrvls)
            self.recalc |= self.method.update_m(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            self.recalculate()

            new_r = map(self.method.characteristic, new_intrvls)
            for r, intrvl in zip(new_r, new_intrvls):
                self.trial_data.insert(r, intrvl)

            niter += 1
        self._solution.accuracy = mindelta
        self._solution.niter = niter
