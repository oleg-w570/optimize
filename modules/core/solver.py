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
        phantomInterval = IntervalData(lpoint)
        firstInterval = IntervalData(rpoint)
        firstInterval.left = phantomInterval.right
        firstInterval.delta = self.method.CalculateDelta(firstInterval)
        self.method.m = self.method.CalculateM(firstInterval)
        self.Q.put(firstInterval)

    def ReCalculate(self) -> None:
        if self.recalc:
            tmpQ = PriorityQueue()
            while not self.Q.empty():
                interval = self.Q.get()
                interval.R = self.method.CalculateR(interval)
                tmpQ.put(interval)
            self.Q = tmpQ
            self.recalc = False

    def UpdateM(self, m) -> None:
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
        while not self.Q.empty():
            interval: IntervalData = self.Q.get()
            point = interval.right
            self.solution.trials.append(point)
            self.solution.optimum = point if point < self.solution.optimum else self.solution.optimum
        return self._solution
