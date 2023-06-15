from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver
from itertools import chain
from mpi4py import MPI


class MPISolver(Solver):
    def solve(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        self.FirstIteration()
        self.SequentialIterationsForBegin(size - 1)
        mindelta = float('inf')
        itercount = 1
        while mindelta > self.stop.eps and itercount < self.stop.maxiter:
            all_intervalt: list[IntervalData] = []
            for _ in range(size):
                all_intervalt.append(self.Q.get_nowait())
            intervalt: IntervalData = all_intervalt[rank]
            mindelta = comm.allreduce(intervalt.delta, MPI.MIN)
            trial: Point = self.method.NextPoint(intervalt)
            mintrial = comm.allreduce(trial, MPI.MIN)
            self.UpdateOptimum(mintrial)
            new_intervals = self.method.SplitIntervals(intervalt, trial)
            new_m = map(self.method.CalculateM, new_intervals)
            max_m = comm.allreduce(max(new_m), MPI.MAX)
            self.UpdateM(max_m)
            new_r = map(self.method.CalculateR, new_intervals)
            new_intervals = map(self.ChangeR, new_intervals, new_r)
            self.ReCalculate()
            all_new_intervals = comm.allgather(new_intervals)
            all_new_intervals = list(chain.from_iterable(all_new_intervals))
            for interval in all_new_intervals:
                self.Q.put_nowait(interval)
            itercount += 1
        self._solution.accuracy = mindelta
        self._solution.iterationCount = itercount

    def SequentialIterationsForBegin(self, number_iterations: int):
        for _ in range(number_iterations):
            intervalt: IntervalData = self.Q.get()
            trial: Point = self.method.NextPoint(intervalt)
            new_intervals = self.method.SplitIntervals(intervalt, trial)
            new_m = map(self.method.CalculateM, new_intervals)
            self.UpdateM(max(new_m))
            self.UpdateOptimum(trial)
            self.ReCalculate()
            new_r = map(self.method.CalculateR, new_intervals)
            new_intervals = map(self.ChangeR, new_intervals, new_r)
            for interval in new_intervals:
                self.Q.put_nowait(interval)
