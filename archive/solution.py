import numpy as np
from typing import List

class Solution:
    def __init__(self):
        self.trialPoints: List = []
        self.trialValues: List = []
        self.optimumPoint: np.ndarray(shape=(1), dtype=float) = None
        self.optimumValue: float = np.infty
        self.iterationCount: int = 0


