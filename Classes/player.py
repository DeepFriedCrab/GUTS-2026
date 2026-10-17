from enum import Enum

import pygame

from Classes.aabb import AABB

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
    ldown: bool
    rdown: bool

    def __init__(self, sprite: pygame.Surface, x, y, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale_by(sprite, scale)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.aabb = AABB(x, y, self.rect.w, self.rect.h)

        self.vx = 0; self.vy = 0
        self.facing = Facing.RIGHT; self.action = Action.STILL
        self.ldown = False; self.rdown = False

    @property
    def x(self):
        return self.aabb.x

    @x.setter
    def x(self, x):
        self.aabb.x = x
        self.rect.x = round(x)

    @property
    def y(self):
        return self.aabb.y

    @y.setter
    def y(self, y):
        self.aabb.y = y
        self.rect.y = round(y)

    def move(self):
        self.vx *= 0.5

        match (self.ldown, self.rdown):
            case (False, False):
                pass
            case (False, True):
                self.vx += 2
            case (True, False):
                self.vx -= 2
            case (True, True):
                pass

        if abs(self.vx) < 0.01:
            self.vx = 0

        self.x += self.vx
        self.y += self.vy
