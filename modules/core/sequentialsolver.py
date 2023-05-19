from modules.core.solver import Solver
from modules.utility.point import Point
from archive.interval import IntervalData


class SequentialSolver(Solver):
    def solve(self):
        self.FirstIteration()
        mindelta: float = float('inf')
        niter: int = 0
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            intervalt: IntervalData = self.Q.get()
            mindelta = intervalt.delta
            trial: Point = self.method.NextPoint(intervalt)
            newIntervals = self.method.SplitIntervals(intervalt, trial)
            newM = map(self.method.CalculateM, newIntervals)
            self.UpdateM(max(newM))
            self.UpdateOptimum(trial)
            self.ReCalculate()

            for interval in newIntervals:
                interval.R = self.method.CalculateR(interval)
                self.Q.put(interval)

            niter += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = niter
