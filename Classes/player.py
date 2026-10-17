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

    # dictionary containing keypresses and timers to track them
    press_dict = {
        "l" : {
            "held_time": 0,
            "since_time": 0,
            "down": False,
            "prev": False
        },
        "r": {
            "held_time": 0,
            "since_time": 0,
            "down": False,
            "prev": False
        },
    }
    # values to change dash input timing
    held_cap = 25
    since_cap = 30

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
        self.vx *= 0.5

        # check for a dash move
        l_dash = self.increment_timers(self.press_dict["l"])
        r_dash = self.increment_timers(self.press_dict["r"])

        if l_dash:
            print("DASH LEFTTTT")
            self.vx -= 40

        elif r_dash:
            print("DASH RIGHTTTT")
            self.vx += 40

        else:
            # match on regular movement
            match (self.press_dict["l"]["down"], self.press_dict["r"]["down"]):
                case (False, False):
                    pass
                case (False, True):
                    self.vx += 2
                case (True, False):
                    self.vx -= 2
                case (True, True):
                    pass


        self.x += self.vx
        self.y += self.vy

    # increments timers to check for dash, returns if it detects a dash move has been made
    def increment_timers(self, dicty):
        dash_found = False
        match (dicty["prev"], dicty["down"]):
            case ((False, False)):
                dicty["since_time"] += 1
            case ((False, True)):
                if dicty["since_time"] < self.since_cap and dicty["held_time"] < self.held_cap:
                    dash_found = True

                dicty["held_time"] = 1
                dicty["since_time"] = float('inf')
            case ((True, False)):
                dicty["since_time"] = 1
            case ((True, True)):
                dicty["held_time"] += 1

        return dash_found

    def tick(self):
        self.move()

        # store state at last tick
        self.press_dict["l"]["prev"] = self.press_dict["l"]["down"]
        self.press_dict["r"]["prev"] = self.press_dict["r"]["down"]