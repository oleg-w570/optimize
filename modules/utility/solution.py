from modules.utility.point import Point


class Solution:
    def __init__(self):
        self.points: list[Point] = []
        self.optimum: Point = Point(float('inf'), [float('inf')], float('inf'))
        self.accuracy: float = float('inf')
        self.niter: int = 0
        self.ntrial: int = 0
        self.time: float = 0

    def __repr__(self) -> str:
        return (f'Calculated optimum point: {self.optimum.y}\n'
                f'Calculated optimum value: {self.optimum.z}\n'
                f'Accuracy: {self.accuracy}\n'
                f'Number of iterations: {self.niter}\n'
                f'Number of trials: {self.ntrial}\n'
                f'Solution time: {self.time} sec.')
