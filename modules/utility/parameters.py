import multiprocessing


class Parameters:
    def __init__(self,
                 r: float = 2.5,
                 num_proc: int = multiprocessing.cpu_count(),
                 evolvent_density: int = 10):
        self.r = r
        self.num_proc = num_proc
        self.evolvent_density = evolvent_density
