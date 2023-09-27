from time import perf_counter
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
        start_time = perf_counter()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            all_old_intrvls: list[Interval] = []
            for _ in range(size):
                all_old_intrvls.append(self.trial_data.get_intrvl_with_max_r())
            old_intrvl: Interval = all_old_intrvls[rank]
            mindelta = comm.allreduce(old_intrvl.delta, MPI.MIN)
            point: Point = self.method.next_point(old_intrvl)
            minpoint = comm.allreduce(point, MPI.MIN)
            self.recalc |= self.method.update_optimum(minpoint)
            new_intrvl = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvl)
            max_m = comm.allreduce(max(new_m), MPI.MAX)
            self.recalc |= self.method.update_holder_const(max_m)
            self.recalculate()
            new_r = map(self.method.characteristic, new_intrvl)
            all_new_r = comm.allgather(new_r)
            all_new_r = list(chain.from_iterable(all_new_r))
            all_new_intrvls = comm.allgather(new_intrvl)
            all_new_intrvls = list(chain.from_iterable(all_new_intrvls))
            for trial in zip(all_new_r, all_new_intrvls):
                self.trial_data.insert(*trial)
            niter += 1
        self._solution.time = perf_counter() - start_time
        self._solution.accuracy = mindelta
        self._solution.niter = niter

    def sequential_iterations_for_begin(self):
        for _ in range(MPI.COMM_WORLD.size - 1):
            old_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()
            point: Point = self.method.next_point(old_intrvl)
            new_intrvl = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvl)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            self.recalculate()
            new_r = map(self.method.characteristic, new_intrvl)
            for trial in zip(new_r, new_intrvl):
                self.trial_data.insert(*trial)

