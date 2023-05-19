class StopCondition:
    def __init__(self,
                 eps: float = 0.01,
                 maxiter: int = 1000):
        self.eps = eps
        self.maxiter = maxiter
