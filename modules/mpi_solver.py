from itertools import chain
from time import perf_counter

from mpi4py import MPI

from modules.core.solver_base import SolverBase
from modules.utility.interval import Interval
from modules.utility.parameters import Parameters
from modules.utility.point import Point
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition


class MPISolver(SolverBase):
    def __init__(
        self, problem: Problem, stopcondition: StopCondition, parameters: Parameters
    ):
        super().__init__(problem, stopcondition, parameters)
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.num_proc = self.comm.Get_size()

    def solve(self):
        self.first_iteration()
        mindelta: float = float("inf")
        niter: int = 1
        start_time = perf_counter()
        self.iterations_to_begin()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            all_old_intrvls = self.trial_data.get_n_intrvls_with_max_r(self.num_proc)
            old_intrvl: Interval = all_old_intrvls[self.rank]
            mindelta = self.comm.allreduce(old_intrvl.delta, MPI.MIN)
            point: Point = self.method.next_point(old_intrvl)
            point.z = self.problem.calculate(point.y)
            min_point = self.comm.allreduce(point, MPI.MIN)
            self.recalc |= self.method.update_optimum(min_point)
            new_intrvls = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvls)
            max_m = self.comm.allreduce(max(new_m), MPI.MAX)
            self.recalc |= self.method.update_holder_const(max_m)
            self.recalc_characteristics()
            new_r = map(self.method.characteristic, new_intrvls)
            all_new_r = self.comm.allgather(new_r)
            all_new_r = list(chain.from_iterable(all_new_r))
            all_new_intrvls = self.comm.allgather(new_intrvls)
            all_new_intrvls = list(chain.from_iterable(all_new_intrvls))
            for trial in zip(all_new_r, all_new_intrvls):
                self.trial_data.insert(*trial)
            niter += 1
        self._solution.time = perf_counter() - start_time
        self._solution.accuracy = mindelta
        self._solution.niter = niter

    def iterations_to_begin(self):
        points = self.method.evenly_points(self.num_proc)
        for point in points:
            point.z = self.problem.calculate(point.y)
        self.method.update_optimum(min(points))
        intrvls: list[Interval] = []
        right_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()
        for point in points:
            left_intrvl, right_intrvl = self.method.split_interval(right_intrvl, point)
            intrvls.append(left_intrvl)
        intrvls.append(right_intrvl)
        m = map(self.method.holder_const, intrvls)
        self.method.update_holder_const(max(m))
        r = map(self.method.characteristic, intrvls)
        for trial in zip(r, intrvls):
            self.trial_data.insert(*trial)
