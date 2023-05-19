import multiprocessing
from itertools import chain
from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver

class ParallelSolver(Solver):
    def solve(self):
        self.FirstIteration()
        mindelta: float = float('inf')
        iterationCount: int = 0
        with multiprocessing.Pool(self.numberOfProcess) as pool:
            while mindelta > self.stop.eps and iterationCount < self.stop.maxiter:
                intervalt: list[IntervalData] = []
                for _ in range(self.numberOfProcess):
                    if not self.Q.empty():
                        intervalt.append(self.Q.get())
                mindelta = self.min_delta(intervalt)

                trial: list[Point] = pool.map(self.method.NextPoint, intervalt)
                newIntervals = pool.starmap(self.method.SplitIntervals, zip(intervalt, trial))
                newIntervals = list(chain.from_iterable(newIntervals))
                newm: list[float] = pool.map(self.method.CalculateM, newIntervals)
                self.UpdateM(max(newm))
                self.UpdateOptimum(min(trial))
                self.ReCalculate()
                newR: list[float] = pool.map(self.method.CalculateR, newIntervals)
                for interval, R in zip(newIntervals, newR):
                    interval.R = R
                    self.Q.put(interval)
                iterationCount += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = iterationCount

    @staticmethod
    def min_delta(intervals: list[IntervalData]):
        deltas = []
        for interval in intervals:
            deltas.append(interval.delta)
        return min(deltas)
