from modules.utility.point import Point


class IntervalData:
    def __init__(self, point: Point):
        self.right: Point = point
        self.left: Point = None
        self.delta: float = -1
        self.r: float = -1

    def __lt__(self, other):
        return self.r > other.r

    def __repr__(self):
        text = f"(R={self.r}, left={self.left.x}, right={self.right.x})"
        return text
