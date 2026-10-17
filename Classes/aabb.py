class AABB:
    x: float
    y: float
    w: float
    h: float

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def is_overlapping(self, other):
        return (self.x < other.x + other.w and self.x + self.w > other.x and
                self.y < other.y + other.h and self.y + self.h > other.y)

