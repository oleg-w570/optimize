from modules.utility.point import Point


class Interval:
    def __init__(self, point: Point):
        self.right: Point = point
        self.left: Point = None
        self.delta: float = -1

    def __repr__(self):
        return f"({self.left.x}, {self.right.x})" 
