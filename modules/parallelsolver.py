import multiprocessing
from itertools import chain

from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver


class ParallelSolver(Solver):
    def solve(self):
        self.FirstIteration()
        mindelta: float = float('inf')
        iteration_count: int = 0
        time = []
        with multiprocessing.Pool(self.numberOfProcess) as pool:
            while mindelta > self.stop.eps and iteration_count < self.stop.maxiter:
                intervalt: list[IntervalData] = []
                for _ in range(self.numberOfProcess):
                    if not self.Q.empty():
                        intervalt.append(self.Q.get())
                mindelta = min(intervalt, key=(lambda x: x.delta)).delta

                trial: list[Point] = pool.map(self.method.NextPoint, intervalt)
                new_intervals = pool.starmap(self.method.SplitIntervals, zip(intervalt, trial))
                new_intervals = list(chain.from_iterable(new_intervals))
                newm: list[float] = pool.map(self.method.CalculateM, new_intervals)
                self.UpdateM(max(newm))
                self.UpdateOptimum(min(trial))
                self.ReCalculate()
                new_r: list[float] = pool.map(self.method.CalculateR, new_intervals)
                for interval, R in zip(new_intervals, new_r):
                    interval.R = R
                    self.Q.put(interval)
                iteration_count += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = iteration_count
