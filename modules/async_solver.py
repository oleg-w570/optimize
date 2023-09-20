from multiprocessing import Process, Queue
from queue import Empty

from modules.core.method import Method
from modules.utility.interval import Interval
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
            new_r = map(self.method.characteristic, new_intrvls)
            new_m = map(self.method.lipschitz_const, new_intrvls)
            self.done.put_nowait((new_m, new_r, new_intrvls))
            print(f'I am released!')


class AsyncSolver(Solver):
    def __init__(self,
                 problem: Problem,
                 stopcondition: StopCondition = ...,
                 parameters: Parameters = ...):
        super().__init__(problem, stopcondition, parameters)
        self.tasks: Queue = Queue()
        self.done: Queue = Queue()
        self.workers: list[Worker] = [Worker(self.method, self.tasks, self.done)
                                      for _ in range(self.num_proc)]

    def start_workers(self) -> None:
        for w in self.workers:
            w.start()
        self.tasks.put_nowait((self.trial_data.get_intrvl_with_max_r(),
                               self.method.m, self.method.optimum))

    def stop_workers(self) -> None:
        for _ in range(self.num_proc):
            self.tasks.put_nowait('STOP')
        self.done.get()
        for w in self.workers:
            w.join()
            w.close()
            
    def save_remaining_intrvls(self) -> None:
        while True:
            try:
                _, new_r, new_intrvls = self.done.get_nowait()
            except Empty:
                break
            else:
                print('remaining interval')
                for trial in zip(new_r, new_intrvls):
                    self.trial_data.insert(*trial)

    def get_n_intrvls_with_max_r(self, n: int) -> list[Interval]:
        intrvls = []
        for _ in range(n):
            intrvls.append(self.trial_data.get_intrvl_with_max_r())
        return intrvls

    def solve(self):
        self.first_iteration()
        self.start_workers()
        mindelta: float = float('inf')
        niter: int = 0
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            print(f'Iter {niter}')
            new_m, new_r, new_intrvls = self.done.get()
            for trial in zip(new_r, new_intrvls):
                self.trial_data.insert(*trial)
            point = new_intrvls[0].right
            self.recalc |= self.method.update_m(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            released_process = 1
            while not self.done.empty():
                new_m, new_r, new_intrvls = self.done.get()
                for trial in zip(new_r, new_intrvls):
                    self.trial_data.insert(*trial)
                point = new_intrvls[0].right
                self.recalc |= self.method.update_m(max(new_m))
                self.recalc |= self.method.update_optimum(point)
                released_process += 1
            print(f'\treleased process: {released_process}')
            self.recalculate()
            old_intrvls = self.get_n_intrvls_with_max_r(released_process)
            mindelta = min(old_intrvls, key=lambda x: x.delta).delta
            for old_intrvl in old_intrvls:
                self.tasks.put_nowait((old_intrvl, self.method.m, self.method.optimum))
            niter += 1
        self.save_remaining_intrvls()
        self.stop_workers()
        self._solution.accuracy = mindelta
        self._solution.niter = niter
