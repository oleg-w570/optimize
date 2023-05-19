import sys

from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver
from itertools import chain
from mpi4py import MPI
import multiprocessing

sys.setrecursionlimit(10000)


class MpiSolver(Solver):
    def solve(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        self.FirstIteration()
        self.SequentialIterationsForBegin(size-1)

        mindelta = float('inf')
        niter = 0

        with multiprocessing.Pool(self.numberOfProcess) as pool:
            while mindelta > self.stop.eps and niter < self.stop.maxiter:
                if rank == 0:
                    allIntervalt = []
                    for _ in range(size * self.numberOfProcess):
                        if not self.Q.empty():
                            allIntervalt.append(self.Q.get())
                    step = len(allIntervalt) // size
                    allIntervalt = [allIntervalt[i:i+step] for i in range(0, len(allIntervalt), step)]
                else:
                    allIntervalt = None
                locIntervalt: list[IntervalData] = comm.scatter(allIntervalt, 0)

                locMinDelta: float = self.min_delta(locIntervalt)
                mindelta = comm.allreduce(locMinDelta, MPI.MIN)

                locTrials: list[Point] = pool.map(self.method.NextPoint, locIntervalt)
                locMinTrial: Point = min(locTrials)
                mintrial: Point = comm.allreduce(locMinTrial, MPI.MIN)
                self.UpdateOptimum(mintrial)

                locNewIntervals = pool.starmap(self.method.SplitIntervals, zip(locIntervalt, locTrials))
                locNewIntervals = list(chain.from_iterable(locNewIntervals))
                allNewIntervals = comm.gather(locNewIntervals, 0)

                locNewM: list[float] = pool.map(self.method.CalculateM, locNewIntervals)
                locMaxM: float = max(locNewM)
                maxm: float = comm.allreduce(locMaxM, MPI.MAX)
                self.UpdateM(maxm)

                locNewR: list[float] = pool.map(self.method.CalculateR, locNewIntervals)
                allNewR: list[list[float]] = comm.gather(locNewR, 0)
                if rank == 0:
                    self.ReCalculate()
                    allNewIntervals = list(chain.from_iterable(allNewIntervals))
                    allNewR = list(chain.from_iterable(allNewR))

                    for interval, R in zip(allNewIntervals, allNewR):
                        interval.R = R
                        self.Q.put(interval)
                niter += 1
            self._solution.accuracy = mindelta
            self._solution.iterationCount = niter

    def SequentialIterationsForBegin(self, numberOfIteration: int):
        for _ in range(numberOfIteration):
            intervalt: IntervalData = self.Q.get()
            trial: Point = self.method.NextPoint(intervalt)
            newIntervals = self.method.SplitIntervals(intervalt, trial)
            newM = map(self.method.CalculateM, newIntervals)
            self.UpdateM(max(newM))
            self.UpdateOptimum(trial)
            self.ReCalculate()
            for interval in newIntervals:
                interval.R = self.method.CalculateR(interval)
                self.Q.put(interval)

    @staticmethod
    def min_delta(intervals: list[IntervalData]):
        deltas = []
        for interval in intervals:
            deltas.append(interval.delta)
        return min(deltas)

