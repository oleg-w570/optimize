import multiprocessing


class Parameters:
    def __init__(self,
                 r: float = 2.5,
                 process_count: int = multiprocessing.cpu_count(),
                 evolvent_density: int = 10):
        self.r = r
        self.process_count = process_count
        self.evolvent_density = evolvent_density
