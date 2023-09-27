from multiprocessing import Process, Queue
from time import perf_counter

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
            new_m = map(self.method.holder_const, new_intrvls)
            self.done.put_nowait((new_m, new_r, new_intrvls))


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

    def solve(self):
        self.first_iteration()
        self.sequential_iterations_for_begin()  # вычислим нужное количество интервалов, чтобы загрузить работой все процессы
        self.start_workers()  # стартуем все процессы и передаём каждому по интервалу
        mindelta: float = float('inf')
        niter: int = 0
        start_time = perf_counter()
        while mindelta > self.stop.eps and niter < self.stop.maxiter:
            new_m, new_r, new_intrvls = self.done.get()  # обязательно ждём, что один процесс завершит обработку интервала и вернёт результат
            for trial in zip(new_r, new_intrvls):  # здесь и далее идёт обработка полученных данных
                self.trial_data.insert(*trial)
            point = new_intrvls[0].right
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            released_process = 1  # ставим счётчик процессов, завершивших работу на текущей итерации
            while not self.done.empty():  # далее проверяем очередь готовых данных, так же обрабатываем их, и увеличиваем счётчик
                new_m, new_r, new_intrvls = self.done.get()
                for trial in zip(new_r, new_intrvls):
                    self.trial_data.insert(*trial)
                point = new_intrvls[0].right
                self.recalc |= self.method.update_holder_const(max(new_m))
                self.recalc |= self.method.update_optimum(point)
                released_process += 1
            self.recalculate()  # проверяем нужно ли пересчитать характеристики всех интервалов
            old_intrvls = self.get_n_intrvls_with_max_r(released_process)  # выдаём интервалы с макс характеристикой столько, сколько завершило работу процессов на текущей итерации
            mindelta = min(old_intrvls, key=lambda x: x.delta).delta
            for old_intrvl in old_intrvls:
                self.tasks.put_nowait((old_intrvl, self.method.m, self.method.optimum))  # также передаём процессам текущие оценку конст Л. и оптимума
            niter += 1
            # print(released_process)
        self._solution.time = perf_counter() - start_time
        self.stop_workers()
        self._solution.accuracy = mindelta
        self._solution.niter = niter

    def start_workers(self) -> None:
        for w in self.workers:
            w.start()
        for _ in range(self.num_proc):
            self.tasks.put_nowait((self.trial_data.get_intrvl_with_max_r(),
                                   self.method.m, self.method.optimum))

    def stop_workers(self) -> None:
        for _ in range(self.num_proc):
            self.tasks.put_nowait('STOP')
        while not self.done.empty():
            _, new_r, new_intrvls = self.done.get()
            for trial in zip(new_r, new_intrvls):
                self.trial_data.insert(*trial)
        for w in self.workers:
            w.terminate()

    def sequential_iterations_for_begin(self):
        for _ in range(self.num_proc - 1):
            old_intrvl: Interval = self.trial_data.get_intrvl_with_max_r()
            point = self.method.next_point(old_intrvl)
            new_intrvl = self.method.split_interval(old_intrvl, point)
            new_m = map(self.method.holder_const, new_intrvl)
            self.recalc |= self.method.update_holder_const(max(new_m))
            self.recalc |= self.method.update_optimum(point)
            self.recalculate()
            new_r = map(self.method.characteristic, new_intrvl)
            for trial in zip(new_r, new_intrvl):
                self.trial_data.insert(*trial)

    def get_n_intrvls_with_max_r(self, n: int) -> list[Interval]:
        intrvls = []
        for _ in range(n):
            intrvls.append(self.trial_data.get_intrvl_with_max_r())
        return intrvls
