class Point:
    def __init__(self, x: float, y: list[float], z: float = None):
        self.x = x
        self.y = y
        self.z = z

    def __lt__(self, other):
        return self.z < other.z

    def __repr__(self):
        return f'x={self.x}, y={self.y}, z={self.z}'
