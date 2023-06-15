from typing import Callable, List
import numpy as np

class Problem:
    def __init__(self,
                 func: Callable[..., float],
                 lowerBound: List[float],
                 upperBound: List[float],
                 dimension: int):
        self.f = func
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.dimension = dimension