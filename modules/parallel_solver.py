import pathos.multiprocessing as mp
from itertools import chain

from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver


class ParallelSolver(Solver):
    def get_intervals_with_max_r(self) -> list[IntervalData]:
        intervals: list[IntervalData] = []
        for _ in range(self.num_proc):
            if not self.intrvls_queue.empty():
                intervals.append(self.intrvls_queue.get_nowait())
        return intervals

    def solve(self):
        self.first_iteration()
        mindelta: float = float('inf')
        niter: int = 0
        with mp.ProcessingPool(self.num_proc) as pool:
            while mindelta > self.stop.eps and niter < self.stop.maxiter:
                old_intrvls = self.get_intervals_with_max_r()
                mindelta = min(old_intrvls, key=(lambda x: x.delta)).delta

                trials: list[Point] = pool.map(self.method.next_point, old_intrvls)
                new_intervals = pool.map(self.method.split_interval, old_intrvls, trials)
                new_intervals = list(chain.from_iterable(new_intervals))

                new_m: list[float] = pool.map(self.method.calculate_m, new_intervals)
                self.recalc |= self.method.update_m(max(new_m))
                self.recalc |= self.method.update_optimum(min(trials))
                self.recalculate()

                new_r: list[float] = pool.map(self.method.calculate_r, new_intervals)
                for interval, r in zip(new_intervals, new_r):
                    interval.r = r
                    self.intrvls_queue.put_nowait(interval)
                niter += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = niter
