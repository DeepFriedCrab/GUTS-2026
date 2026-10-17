from enum import Enum

import pygame

from classes.aabb import AABB

class Facing(Enum):
    RIGHT = 0
    LEFT = 1

class Action(Enum):
    STILL = 0

class Player(pygame.sprite.Sprite):
    aabb: AABB
    vx: float
    vy: float
    facing: Facing
    action: Action

    def __init__(self, sprite, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect(center=(30,30))
        self.aabb = AABB(x, y, w, h)
        self.vx = 0; self.vy = 0
        self.facing = Facing.RIGHT; self.action = Action.STILL

    @property
    def x(self):
        return self.aabb.x

    @x.setter
    def x(self, x):
        self.rect.x = round(x)
        self.aabb.x = round(x)

    @property
    def y(self):
        return self.aabb.y

    @y.setter
    def y(self, y):
        self.rect.y = round(y)
        self.aabb.y = round(y)

    def move(self):
        self.x += 1