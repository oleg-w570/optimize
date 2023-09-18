from modules.utility.interval import Interval
from modules.utility.point import Point
from modules.core.solver import Solver
from itertools import chain
from mpi4py import MPI


class MPISolver(Solver):
    def solve(self):
        comm = MPI.COMM_WORLD
        size = comm.Get_size()
        rank = comm.Get_rank()
        self.first_iteration()
        self.sequential_iterations_for_begin()
        mindelta: float = float('inf')
        niter: int = 1
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            all_intervalt: list[Interval] = []
            for _ in range(size):
                all_intervalt.append(self.intrvls_queue.get_nowait())
            intervalt: Interval = all_intervalt[rank]
            mindelta = comm.allreduce(intervalt.delta, MPI.MIN)
            trial: Point = self.method.next_point(intervalt)
            mintrial = comm.allreduce(trial, MPI.MIN)
            self.recalc |= self.method.update_optimum(mintrial)
            new_intervals = self.method.split_interval(intervalt, trial)
            new_m = map(self.method.lipschitz_const, new_intervals)
            max_m = comm.allreduce(max(new_m), MPI.MAX)
            self.recalc |= self.method.update_m(max_m)
            self.recalculate()
            new_r = map(self.method.characteristic, new_intervals)
            new_intervals = map(self.change_r, new_intervals, new_r)
            all_new_intervals = comm.allgather(new_intervals)
            all_new_intervals = list(chain.from_iterable(all_new_intervals))
            for interval in all_new_intervals:
                self.intrvls_queue.put_nowait(interval)
            niter += 1
        self._solution.accuracy = mindelta
        self._solution.niter = niter

    def sequential_iterations_for_begin(self):
        for _ in range(MPI.COMM_WORLD.size - 1):
            intervalt: Interval = self.intrvls_queue.get_nowait()
            trial: Point = self.method.next_point(intervalt)
            new_intervals = self.method.split_interval(intervalt, trial)
            new_m = map(self.method.lipschitz_const, new_intervals)
            self.recalc |= self.method.update_m(max(new_m))
            self.recalc |= self.method.update_optimum(trial)
            self.recalculate()
            new_r = map(self.method.characteristic, new_intervals)
            new_intervals = map(self.change_r, new_intervals, new_r)
            for interval in new_intervals:
                self.intrvls_queue.put_nowait(interval)
