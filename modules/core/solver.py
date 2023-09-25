from abc import ABC, abstractmethod

from modules.core.trial_data import TrialData
from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from modules.utility.parameters import Parameters
from modules.utility.solution import Solution
from modules.utility.interval import Interval
from modules.core.method import Method


class Solver(ABC):
    def __init__(self,
                 problem: Problem,
                 stopcondition: StopCondition = StopCondition(),
                 parameters: Parameters = Parameters()):
        self.method: Method = Method(problem, parameters)
        self.num_proc: int = parameters.num_proc
        self.stop: StopCondition = stopcondition
        self.trial_data: TrialData = TrialData()
        self.recalc = True
        self._solution: Solution = Solution()

    @abstractmethod
    def solve(self):
        pass

    def first_iteration(self):
        lpoint, rpoint = self.method.first_points()
        first_interval = Interval(rpoint)
        first_interval.left = lpoint
        first_interval.delta = self.method.delta(first_interval)
        self.method.m = self.method.lipschitz_const(first_interval)
        self.trial_data.insert(-1, first_interval)

    def recalculate(self) -> None:
        if self.recalc:
            for trial in self.trial_data:
                trial.characteristic = self.method.characteristic(trial.interval)
            self.trial_data.refill()
            self.recalc = False
            
    @property
    def solution(self) -> Solution:
        points = list(map(lambda trial: trial.interval.right,
                          self.trial_data.queue))
        self._solution.points = points
        self._solution.ntrial = len(points)
        self._solution.optimum = min(points)
        return self._solution
