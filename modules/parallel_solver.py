import pathos.multiprocessing as mp
from itertools import chain

from modules.utility.interval import Interval
from modules.utility.point import Point
from modules.core.solver import Solver


class ParallelSolver(Solver):
    # def sequential_iterations_for_begin(self):
    #     for _ in range(self.num_proc - 1):
    #         old_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()
    #         trial: Point = self.method.next_point(old_intrvl)
    #         new_intrvl = self.method.split_interval(old_intrvl, trial)
    #         new_m = map(self.method.lipschitz_const, new_intrvl)
    #         self.recalc |= self.method.update_m(max(new_m))
    #         self.recalc |= self.method.update_optimum(trial)
    #         self.recalculate()
    #         new_r = map(self.method.characteristic, new_intrvl)
    #         for r, intrvl in zip(new_r, new_intrvl):
    #             self.trial_data.insert(r, intrvl)
                
    def get_intrvls_with_max_r(self) -> list[Interval]:
        intervals: list[Interval] = []
        for _ in range(min(self.num_proc, self.trial_data.size())):
            intervals.append(self.trial_data.get_intrvl_with_max_r())
        return intervals

    def solve(self):
        self.first_iteration()
        # self.sequential_iterations_for_begin()
        mindelta: float = float('inf')
        niter: int = 0
        with mp.ProcessingPool(self.num_proc) as pool:
            while mindelta > self.stop.eps and niter < self.stop.maxiter:
                old_intrvls = self.get_intrvls_with_max_r()
                mindelta = min(old_intrvls, key=(lambda x: x.delta)).delta

                points: list[Point] = pool.map(self.method.next_point, old_intrvls)
                new_intrvls = pool.map(self.method.split_interval, old_intrvls, points)
                new_intrvls = list(chain.from_iterable(new_intrvls))

                new_m: list[float] = pool.map(self.method.lipschitz_const, new_intrvls)
                self.recalc |= self.method.update_m(max(new_m))
                self.recalc |= self.method.update_optimum(min(points))
                self.recalculate()

                new_r: list[float] = pool.map(self.method.characteristic, new_intrvls)
                for trial in zip(new_r, new_intrvls):
                    self.trial_data.insert(*trial)
                niter += 1
        self._solution.accuracy = mindelta
        self._solution.niter = niter
