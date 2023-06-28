from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver
from itertools import chain
from mpi4py import MPI
import multiprocessing


class MpiPoolSolver(Solver):
    def solve(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()

        self.FirstIteration()
        self.SequentialIterationsForBegin(size-1)

        mindelta = float('inf')
        niter = 0

        with multiprocessing.Pool(self.num_proc) as pool:
            while mindelta > self.stop.eps and niter < self.stop.maxiter:
                if rank == 0:
                    all_intervalt = []
                    for _ in range(size * self.num_proc):
                        if not self.Q.empty():
                            all_intervalt.append(self.Q.get())
                    step = len(all_intervalt) // size
                    all_intervalt = [all_intervalt[i:i+step] for i in range(0, len(all_intervalt), step)]
                else:
                    all_intervalt = None
                loc_intervalt: list[IntervalData] = comm.scatter(all_intervalt, 0)

                loc_mindelta: float = min(loc_intervalt, key=(lambda x: x.delta)).delta
                mindelta = comm.allreduce(loc_mindelta, MPI.MIN)

                loc_trials: list[Point] = pool.map(self.method.NextPoint, loc_intervalt)
                loc_mintrial: Point = min(loc_trials)
                mintrial: Point = comm.allreduce(loc_mintrial, MPI.MIN)
                self.UpdateOptimum(mintrial)

                loc_new_intervals = pool.starmap(self.method.SplitIntervals, zip(loc_intervalt, loc_trials))
                loc_new_intervals = list(chain.from_iterable(loc_new_intervals))
                all_new_intervals = comm.gather(loc_new_intervals, 0)

                loc_new_m: list[float] = pool.map(self.method.CalculateM, loc_new_intervals)
                loc_max_m: float = max(loc_new_m)
                maxm: float = comm.allreduce(loc_max_m, MPI.MAX)
                self.UpdateM(maxm)

                loc_new_r: list[float] = pool.map(self.method.CalculateR, loc_new_intervals)
                all_new_r: list[list[float]] = comm.gather(loc_new_r, 0)
                if rank == 0:
                    self.ReCalculate()
                    all_new_intervals = list(chain.from_iterable(all_new_intervals))
                    all_new_r = list(chain.from_iterable(all_new_r))

                    for interval, R in zip(all_new_intervals, all_new_r):
                        interval.R = R
                        self.Q.put(interval)
                niter += 1
            self._solution.accuracy = mindelta
            self._solution.iterationCount = niter

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
