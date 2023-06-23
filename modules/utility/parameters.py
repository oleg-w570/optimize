import multiprocessing


class Parameters:
    def __init__(self,
                 r: float = 2.5,
                 process_count: int = multiprocessing.cpu_count()):
        self.r = r
        self.processCount = process_count
