from multiprocessing import Process, Queue

from modules.core.method import Method


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
        for intrvl in iter(self.tasks.get, 'STOP'):
            trial = self.method.next_point(intrvl)
            new_intrvls = self.method.split_interval(intrvl, trial)
            lipschitz_constants = map(self.method.lipschitz_constant, new_intrvls)

            charactirics = map(self.method.characteristic, new_intrvls)
            for new_intrvl, r in zip(new_intrvls, charactirics):
                new_intrvl.r = r
                self.done.put(new_intrvl)
