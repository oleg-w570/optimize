from multiprocessing import Process, Queue
from time import perf_counter

from modules.core.method import Method
from modules.utility.intervaldata import IntervalData
from modules.utility.parameters import Parameters
from modules.core.solver import Solver
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition


class Worker(Process):
    def __init__(self,
                 method: Method,
                 tasks: Queue,
                 done: Queue):
        super().__init__()
        self.method: Method = method
        self.tasks = tasks
        self.done = done

    def run(self) -> None:
        for intrvl, m, optimum in iter(self.tasks.get, 'STOP'):
            self.method.m = m
            self.method.optimum = optimum
            point = self.method.next_point(intrvl)
            new_intrvls = self.method.split_interval(intrvl, point)
            for new_intrvl in new_intrvls:
                new_intrvl.r = self.method.characteristic(new_intrvl)
                new_intrvl.m = self.method.lipschitz_const(new_intrvl)
            self.done.put(new_intrvls)


class AsyncSolver(Solver):
    def __init__(self,
                 problem: Problem,
                 stopcondition: StopCondition = ...,
                 parameters: Parameters = ...):
        super().__init__(problem, stopcondition, parameters)
        self.tasks: Queue = Queue()
        self.done: Queue = Queue()
        self.workers: list[Worker] = []
        for _ in range(self.num_proc):
            w = Worker(self.method, self.tasks, self.done)
            self.workers.append(w)

    def start_workers(self) -> None:
        for w in self.workers:
            w.start()
        self.tasks.put_nowait((self.intrvls_queue.get_nowait(),
                               self.method.m, self.method.optimum))

    def stop_workers(self) -> None:
        for _ in range(self.num_proc):
            self.tasks.put_nowait('STOP')
        for w in self.workers:
            w.join()
            w.close()
        while not self.done.empty:
            self.intrvls_queue.put_nowait(self.done.get())

    def solve(self):
        self.first_iteration()
        self.start_workers()
        mindelta: float = float('inf')
        niter: int = 0
        start_time = perf_counter()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            new_intrvls: tuple[IntervalData, IntervalData] = self.done.get()
            for new_intrvl in new_intrvls:
                self.intrvls_queue.put_nowait(new_intrvl)

            m = max(new_intrvls[0].m, new_intrvls[1].m)
            point = new_intrvls[0].right
            self.recalc |= self.method.update_m(m)
            self.recalc |= self.method.update_optimum(point)
            self.recalculate()

            old_intrvl: IntervalData = self.intrvls_queue.get_nowait()
            self.tasks.put_nowait((old_intrvl, self.method.m, self.method.optimum))

            mindelta = old_intrvl.delta
            niter += 1
        self.solving_time = perf_counter() - start_time
        self.stop_workers()
        self._solution.accuracy = mindelta
        self._solution.niter = niter
