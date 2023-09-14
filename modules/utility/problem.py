class Problem:
    def __init__(self,
                 func: callable,
                 lower_bound: list[float],
                 upper_bound: list[float],
                 dimension: int):
        self.f = func
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.dim = dimension

