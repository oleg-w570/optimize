import multiprocessing
class Parameters:
    def __init__(self,
                 r: float = 2.5,
                 processCount: int = multiprocessing.cpu_count()):
        self.r = r
        self.processCount = processCount
