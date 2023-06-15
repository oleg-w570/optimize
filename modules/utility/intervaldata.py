from modules.utility.point import Point


class IntervalData:
    def __init__(self, point: Point):
        self.right: Point = point
        self.left: Point = None
        self.delta: float = -1
        self.R: float = -1

    def __lt__(self, other):
        return self.R > other.R

    def __repr__(self):
        text = f"(R={self.R}, left={self.left.x}, right={self.right.x})"
        return text
