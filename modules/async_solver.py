from multiprocessing import Process, Queue, current_process
from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.solver import Solver


class AsyncSolver(Solver):
    def calculator(self, input: Queue, output: Queue):
        for intrvl in iter(input.get, 'STOP'):
            ...
            # trial: Point = self.method.nextPoint(intrvl)
            # new_intrvls = self.method.splitInterval(intrvl, trial)
            # new_r = map(self.method.calculateR, new_intrvls)
            # new_intrvls = list(map(self.changeR, new_intrvls, new_r))
            # for new_intrvl in new_intrvls:
            #     output.put(new_intrvl)

    def solve(self):
        self.first_iteration()
        task_queue: Queue = Queue()
        done_queue: Queue = Queue()
        task_queue.put(3)
        for _ in range(self.num_proc):
            Process(target=self.calculator, args=(task_queue, done_queue)).start()
        mindelta: float = float('inf')
        niter: int = 0
        # while mindelta > self.stop.eps and niter < self.stop.maxiter:
        #     print(f'Iteration {niter}')
        #     new_intrvl: IntervalData = done_queue.get()
        #     new_m: float = self.method.calculateM(new_intrvl)
        #     self.updateM(new_m)
        #     self.updateOptimum(new_intrvl.right)
        #     self.reCalculate
        #     self.Q.put(new_intrvl)
        #     intrvlT = self.Q.get()
        #     task_queue.put(intrvlT)
        #     mindelta = intrvlT.delta
        #     niter += 1
        for _ in range(self.num_proc):
            task_queue.put('STOP')
        self._solution.accuracy = mindelta
        self._solution.iterationCount = niter

