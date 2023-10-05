from multiprocessing import Process, Queue
from time import perf_counter

from modules.core.solver_base import SolverBase
from modules.utility.interval import Interval
from modules.utility.parameters import Parameters
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition


class Worker(Process):
    def __init__(self, problem: Problem, task_queue: Queue, done_queue: Queue):
        super().__init__()
        self.problem = problem
        self.task_queue = task_queue
        self.done_queue = done_queue

    def run(self) -> None:
        for point in iter(self.task_queue.get, "STOP"):
            point.z = self.problem.calculate(point.y)
            self.done_queue.put_nowait(point)


class AsyncSolver(SolverBase):
    def __init__(
            self, problem: Problem, stopcondition: StopCondition, parameters: Parameters
    ):
        super().__init__(problem, stopcondition, parameters)
        self.task_queue: Queue = Queue()
        self.done_queue: Queue = Queue()
        self.workers: list[Worker] = [
            Worker(self.problem, self.task_queue, self.done_queue)
            for _ in range(self.num_proc)
        ]

    def solve(self):
        self.first_iteration()
        self.start_workers()
        waiting_workers = self.num_proc
        waiting_intrvls: dict[float, Interval] = dict()
        mindelta: float = float("inf")
        niter: int = self.num_proc
        start_time = perf_counter()
        self.iterations_to_begin()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            old_intrvls = self.trial_data.get_n_intrvls_with_max_r(waiting_workers)
            mindelta = min([item.delta for item in old_intrvls])
            for old_intrvl in old_intrvls:
                point = self.method.next_point(old_intrvl)
                waiting_intrvls[point.x] = old_intrvl
                self.task_queue.put_nowait(point)
            point = self.done_queue.get()
            old_intrvl = waiting_intrvls[point.x]
            new_intrvls = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvls)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            new_r = map(self.method.characteristic, new_intrvls)
            for trial in zip(new_r, new_intrvls):
                self.trial_data.insert(*trial)
            waiting_workers = 1
            while not self.done_queue.empty():
                point = self.done_queue.get()
                old_intrvl = waiting_intrvls[point.x]
                new_intrvls = self.method.split_interval(old_intrvl, point)
                new_m = map(self.method.holder_const, new_intrvls)
                self.recalc |= self.method.update_holder_const(max(new_m))
                self.recalc |= self.method.update_optimum(point)
                new_r = map(self.method.characteristic, new_intrvls)
                for trial in zip(new_r, new_intrvls):
                    self.trial_data.insert(*trial)
                waiting_workers += 1
            self.recalc_characteristics()
            niter += 1
        self._solution.time = perf_counter() - start_time
        self.stop_workers(waiting_intrvls)
        self._solution.accuracy = mindelta
        self._solution.niter = niter

    def start_workers(self) -> None:
        for w in self.workers:
            w.start()

    def stop_workers(self, waiting_intrvls: dict[float, Interval]) -> None:
        for _ in range(self.num_proc):
            self.task_queue.put_nowait("STOP")
        for w in self.workers:
            w.join()
        while not self.done_queue.empty():
            point = self.done_queue.get()
            old_intrvl = waiting_intrvls[point.x]
            new_intrvls = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvls)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            new_r = map(self.method.characteristic, new_intrvls)
            for trial in zip(new_r, new_intrvls):
                self.trial_data.insert(*trial)

    def iterations_to_begin(self):
        points = self.method.evenly_points(self.num_proc)
        for point in points:
            self.task_queue.put_nowait(point)
        points = []
        for _ in range(self.num_proc - 1):
            point = self.done_queue.get()
            points.append(point)
        points.sort(key=lambda p: p.x)
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
