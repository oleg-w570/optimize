from abc import ABC, abstractmethod
from queue import PriorityQueue
from time import perf_counter

from modules.utility.problem import Problem
from modules.utility.stopcondition import StopCondition
from modules.utility.parameters import Parameters
from modules.utility.solution import Solution
from modules.utility.intervaldata import IntervalData
from modules.utility.point import Point
from modules.core.method import Method


class Solver(ABC):
    def __init__(self,
                 problem: Problem,
                 stopcondition: StopCondition = StopCondition(),
                 parameters: Parameters = Parameters()):
        self.method: Method = Method(problem, parameters)
        self.numberOfProcess = parameters.processCount
        self.stop: StopCondition = stopcondition
        self.Q = PriorityQueue()
        self.recalc = True
        self._solution: Solution = Solution()

    @abstractmethod
    def solve(self):
        pass

    def FirstIteration(self):
        lpoint, rpoint = self.method.FirstPoints()
        phantom_interval = IntervalData(lpoint)
        first_interval = IntervalData(rpoint)
        first_interval.left = phantom_interval.right
        first_interval.delta = self.method.CalculateDelta(first_interval)
        self.method.m = self.method.CalculateM(first_interval)
        self.Q.put_nowait(first_interval)

    def ReCalculate(self) -> None:
        if self.recalc:
            old_intervals = self.Q.queue
            new_r = map(self.method.CalculateR, old_intervals)
            new_intervals = list(map(self.ChangeR, old_intervals, new_r))
            self.Q.queue.clear()
            for interval in new_intervals:
                self.Q.put_nowait(interval)
            self.recalc = False

    @staticmethod
    def ChangeR(interval: IntervalData, R: float) -> IntervalData:
        interval.R = R
        return interval

    def UpdateM(self, m: float) -> None:
        if m > self.method.m:
            self.method.m = m
            self.recalc = True

    def UpdateOptimum(self, point: Point) -> None:
        z = point.z
        if z < self.method.optimum:
            self.method.optimum = z
            self.recalc = True

    @property
    def solution(self):
        intervals = self.Q.queue
        points = map(lambda interval: interval.right, intervals)
        self._solution.trials = points
        self._solution.optimum = min(points)
        return self._solution
