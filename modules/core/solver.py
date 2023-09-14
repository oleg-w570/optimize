from abc import ABC, abstractmethod
from queue import PriorityQueue

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
        self.num_proc: int = parameters.process_count
        self.stop: StopCondition = stopcondition
        self.Q = PriorityQueue()
        self.recalc = True
        self._solution: Solution = Solution()

    @abstractmethod
    def solve(self):
        pass

    def first_iteration(self):
        lpoint, rpoint = self.method.first_points()
        phantom_interval = IntervalData(lpoint)
        first_interval = IntervalData(rpoint)
        first_interval.left = phantom_interval.right
        first_interval.delta = self.method.calculate_delta(first_interval)
        self.method.m = self.method.calculate_m(first_interval)
        self.Q.put_nowait(first_interval)

    def re_calculate(self) -> None:
        if self.recalc:
            old_intervals = self.Q.queue
            new_r = map(self.method.calculate_r, old_intervals)
            new_intervals = list(map(self.change_r, old_intervals, new_r))
            self.Q.queue.clear()
            for interval in new_intervals:
                self.Q.put_nowait(interval)
            self.recalc = False

    @staticmethod
    def change_r(interval: IntervalData, r: float) -> IntervalData:
        interval.R = r
        return interval

    def update_m(self, m: float) -> None:
        if m > self.method.m:
            self.method.m = m
            self.recalc = True

    def update_optimum(self, point: Point) -> None:
        z = point.z
        if z < self.method.optimum:
            self.method.optimum = z
            self.recalc = True

    @property
    def solution(self):
        intervals = self.Q.queue
        points = list(map(lambda interval: interval.right, intervals))
        self._solution.trials = points
        self._solution.optimum = min(points)
        return self._solution
