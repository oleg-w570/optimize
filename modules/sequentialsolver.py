from modules.core.solver import Solver
from modules.utility.point import Point
from modules.utility.intervaldata import IntervalData


class SequentialSolver(Solver):
    def solve(self):
        self.FirstIteration()
        mindelta: float = float('inf')
        niter: int = 0
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            intervalt: IntervalData = self.Q.get_nowait()
            mindelta = intervalt.delta
            trial: Point = self.method.NextPoint(intervalt)
            new_intervals = self.method.SplitIntervals(intervalt, trial)
            new_m = map(self.method.CalculateM, new_intervals)
            self.UpdateM(max(new_m))
            self.UpdateOptimum(trial)
            self.ReCalculate()

            new_r = map(self.method.CalculateR, new_intervals)
            new_intervals = list(map(self.ChangeR, new_intervals, new_r))
            for interval in new_intervals:
                self.Q.put_nowait(interval)
            niter += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = niter
