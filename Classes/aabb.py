import pygame

class Box:
    x: float
    y: float
    w: float
    h: float

    def __init__(self, x, y, w, h):
        self.x = x; self.y = y; self.w = w; self.h = h

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def is_overlapping(self, other):
        return (self.x < other.x + other.w and self.x + self.w > other.x and
                self.y < other.y + other.h and self.y + other.h > other.y)

