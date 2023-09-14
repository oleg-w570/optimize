import queue
from typing import List

from modules.core.solver import Solver
from modules.utility.problem import Problem
from archive.solution import Solution
from archive.parameters import Parameters
from archive.interval import IntervalData
from modules.core.evolvent_ import Evolvent


class SequentialSolver(Solver):
    def __init__(self,
                 problem: Problem,
                 parameters: Parameters):
        self.problem: Problem = problem
        self.param: Parameters = parameters
        self.solution: Solution = Solution()
        self.evolvent: Evolvent = Evolvent(problem.lower_bound, problem.upper_bound, problem.dim)
        self.Q = queue.PriorityQueue()
        self.m: float = 1

    def CalculateDelta(self, interval: IntervalData):
        rx = interval.x
        lx = interval.leftInterval.x
        return pow(rx - lx, 1 / self.problem.dim)

    @staticmethod
    def CalculateM(interval: IntervalData) -> float:
        rz = interval.z
        lz = interval.leftInterval.z
        delta = interval.delta
        return abs(rz - lz) / delta

    def CalculateR(self, interval: IntervalData) -> float:
        rz = interval.z
        lz = interval.leftInterval.z
        delta = interval.delta
        z_opt = self.solution.optimumValue
        m = self.m
        r = self.param.r
        return delta + (rz - lz) * (rz - lz) / (r * r * m * m * delta) - 2 * (rz + lz - 2 * z_opt) / (r * m)

    def getSolution(self) -> Solution:
        return self.solution

    def first_iteration(self):
        lx = 0.0
        rx = 1.0
        ly = self.evolvent.get_image(lx)
        ry = self.evolvent.get_image(rx)
        rz = self.problem.f(ry)
        lz = self.problem.f(ly)

        phantomInterval = IntervalData(ly, lx, lz)
        firstInterval = IntervalData(ry, rx, rz)
        firstInterval.leftInterval = phantomInterval
        firstInterval.delta = self.CalculateDelta(firstInterval)

        self.m = self.CalculateM(firstInterval)
        self.Q.put(firstInterval)

    def NextPoint(self, interval: IntervalData) -> float:
        rx = interval.x
        lx = interval.leftInterval.x
        m = self.m
        r = self.param.r
        n = self.problem.dim
        dif = interval.z - interval.leftInterval.z
        dg = 1.0 if dif > 0 else -1.0
        return 0.5 * (rx + lx) - 0.5 * dg * (abs(dif) / m) ** n / r

    def SplitInterval(self, interval: IntervalData, y, x: float, z: float) -> List[IntervalData]:
        left = IntervalData(y, x, z)
        left.leftInterval = interval.leftInterval
        right = IntervalData(interval.y, interval.x, interval.z)
        right.leftInterval = left

        left.delta = self.CalculateDelta(left)
        right.delta = self.CalculateDelta(right)

        return [left, right]

    def Finalize(self, interval_t: IntervalData):
        x = self.NextPoint(interval_t)
        y = self.evolvent.get_image(x)
        z = self.problem.f(y)
        lastIntervals = self.SplitInterval(interval_t, y, x, z)
        for interval in lastIntervals:
            self.Q.put(interval)

        if z < self.solution.optimumValue:
            self.solution.optimumPoint = y
            self.solution.optimumValue = z
        while not self.Q.empty():
            trial: IntervalData = self.Q.get()
            self.solution.trialPoints.append(trial.y)
            self.solution.trialValues.append(trial.z)

    def solve(self):
        self.first_iteration()
        interval_t: IntervalData = self.Q.get()

        while interval_t.delta > self.param.eps:
            x = self.NextPoint(interval_t)
            y = self.evolvent.get_image(x)
            z = self.problem.f(y)
            newIntervals = self.SplitInterval(interval_t, y, x, z)

            recalc = False
            if z < self.solution.optimumValue:
                self.solution.optimumPoint = y
                self.solution.optimumValue = z
                recalc = True
            for interval in newIntervals:
                m = self.CalculateM(interval)
                if m > self.m:
                    self.m = m
                    recalc = True

            if recalc:
                tmpQ = queue.PriorityQueue()
                while not self.Q.empty():
                    interval = self.Q.get()
                    interval.R = self.CalculateR(interval)
                    tmpQ.put(interval)
                self.Q = tmpQ
            for interval in newIntervals:
                interval.R = self.CalculateR(interval)
                self.Q.put(interval)

            interval_t = self.Q.get()
            self.solution.iterationCount += 1

        self.Finalize(interval_t)
