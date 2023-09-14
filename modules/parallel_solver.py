import multiprocessing
from itertools import chain

from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver


class ParallelSolver(Solver):
    def solve(self):
        self.first_iteration()
        mindelta: float = float('inf')
        iteration_count: int = 0
        with multiprocessing.Pool(self.num_proc) as pool:
            while mindelta > self.stop.eps and iteration_count < self.stop.maxiter:
                intervalt: list[IntervalData] = []
                for _ in range(self.num_proc):
                    if not self.Q.empty():
                        intervalt.append(self.Q.get())
                mindelta = min(intervalt, key=(lambda x: x.delta)).delta

                trial: list[Point] = pool.map(self.method.next_point, intervalt)
                new_intervals = pool.starmap(self.method.split_interval, zip(intervalt, trial))
                new_intervals = list(chain.from_iterable(new_intervals))
                newm: list[float] = pool.map(self.method.calculate_m, new_intervals)
                self.update_m(max(newm))
                self.update_optimum(min(trial))
                self.re_calculate()
                new_r: list[float] = pool.map(self.method.calculate_r, new_intervals)
                for interval, R in zip(new_intervals, new_r):
                    interval.R = R
                    self.Q.put(interval)
                iteration_count += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = iteration_count
