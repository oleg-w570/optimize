from modules.utility.point import Point


class Interval:
    def __init__(self, right_point: Point, left_point: Point = None):
        self.right: Point = right_point
        self.left: Point = left_point
        self.delta: float = -1

    def __repr__(self):
        return f"({self.left.x}, {self.right.x})"
