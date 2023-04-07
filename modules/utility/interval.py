class IntervalData:
    def __init__(self,
                 y,
                 x: float,
                 z: float,
                 ):
        self.y = y
        self.x: float = x
        self.z: float = z
        self.leftInterval: IntervalData = None
        self.delta: float = -1
        self.R: float = -1

    def __lt__(self, other):
        return self.R > other.R
