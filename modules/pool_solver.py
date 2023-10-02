from itertools import chain
from time import perf_counter

from pathos.pools import ProcessPool

from modules.core.calculator import Calculator
from modules.core.solver_base import SolverBase
from modules.utility.interval import Interval
from modules.utility.parameters import Parameters
from modules.utility.point import Point
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition


class PoolSolver(SolverBase):
    def __init__(
        self, problem: Problem, stopcondition: StopCondition, parameters: Parameters
    ):
        super().__init__(problem, stopcondition, parameters)
        self.pool = ProcessPool(
            self.num_proc, initializer=Calculator.worker_init, initargs=(self.problem,)
        )

    def iterations_to_begin(self):
        points = self.method.evenly_points(self.num_proc)
        self.func_value_for_points(points)
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

    def func_value_for_points(self, points: list[Point]):
        ys = list(map(lambda p: p.y, points))
        zs: list[float] = self.pool.map(Calculator.work, ys)
        for point, z in zip(points, zs):
            point.z = z

    def solve(self):
        self.first_iteration()
        mindelta: float = float("inf")
        niter: int = self.num_proc
        start_time = perf_counter()
        self.iterations_to_begin()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            old_intrvls = self.trial_data.get_n_intrvls_with_max_r(self.num_proc)

            points: list[Point] = list(map(self.method.next_point, old_intrvls))
            self.func_value_for_points(points)

            new_intrvls = list(map(self.method.split_interval, old_intrvls, points))
            new_intrvls = list(chain.from_iterable(new_intrvls))

            new_m = map(self.method.holder_const, new_intrvls)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(min(points))
            self.recalc_characteristics()

            new_r = map(self.method.characteristic, new_intrvls)
            for trial in zip(new_r, new_intrvls):
                self.trial_data.insert(*trial)

            mindelta = min(map(lambda i: i.delta, old_intrvls))
            niter += 1
        self._solution.time = perf_counter() - start_time
        self._solution.accuracy = mindelta
        self._solution.niter = niter
