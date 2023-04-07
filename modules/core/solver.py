import math
import queue
import numpy as np
from typing import List
from modules.utility.problem import Problem
from modules.utility.parameters import Parameters
from modules.utility.interval import IntervalData
from modules.core.evolvent import Evolvent


class Solver:
    def __init__(self,
                 problem: Problem,
                 parameters: Parameters):
        self.problem: Problem = problem
        self.param: Parameters = parameters
        self.evolvent: Evolvent = Evolvent(problem.lowerBound, problem.upperBound, problem.dimension)
        self.Q = queue.PriorityQueue()
        self.m: float = 1
        self.z_opt: float = 0
        self.iterationCount: int = 0

    def CalculateDelta(self, interval: IntervalData):
        rx = interval.x
        lx = interval.leftInterval.x
        return pow(rx - lx, 1 / self.problem.dimension)

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
        m = self.m
        r = self.param.r
        return delta + (rz - lz) * (rz - lz) / (r * r * m * m * delta) - 2 * (rz + lz - 2 * self.z_opt) / (r * m)

    def FirstIteration(self):
        lx = 0.0
        rx = 1.0
        ly = self.evolvent.GetImage(lx)
        ry = self.evolvent.GetImage(rx)
        rz = self.problem.f(ry)
        lz = self.problem.f(ly)

        phantomInterval = IntervalData(ly, lx, lz)
        firstInterval = IntervalData(ry, rx, rz)
        firstInterval.leftInterval = phantomInterval
        firstInterval.delta = self.CalculateDelta(firstInterval)

        self.m = self.CalculateM(firstInterval)
        self.Q.put(firstInterval)

        self.iterationCount = 0

    def NextPoint(self, interval: IntervalData) -> float:
        rx = interval.x
        lx = interval.leftInterval.x
        m = self.m
        r = self.param.r
        n = self.problem.dimension
        dif = interval.z - interval.leftInterval.z
        dg = 1.0 if dif > 0 else -1.0
        return 0.5 * (rx + lx) - 0.5 * dg * (abs(dif) / m)**n / r

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
        y = self.evolvent.GetImage(x)
        z = self.problem.f(y)
        self.z_opt = z

    def solve(self):
        self.FirstIteration()
        interval_t: IntervalData = self.Q.get()

        while interval_t.delta > self.param.eps:
            x = self.NextPoint(interval_t)
            y = self.evolvent.GetImage(x)
            z = self.problem.f(y)
            newIntervals = self.SplitInterval(interval_t, y, x, z)

            changedM = False
            for interval in newIntervals:
                m = self.CalculateM(interval)
                if m > self.m:
                    self.m = m
                    changedM = True

            if changedM or abs(self.z_opt - z) > 1e-8:
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
            self.z_opt = z
            self.iterationCount += 1

        self.Finalize(interval_t)
