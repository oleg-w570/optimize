class Point:
    def __init__(self,
                 x: float,
                 y,
                 z: float):
        self.x = x
        self.y = y
        self.z = z

    def __lt__(self, other):
        return self.z < other.z
