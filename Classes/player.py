from enum import Enum

import pygame

from Classes.aabb import AABB
from Classes.spritesheet import Animator, SpriteSheet

class Facing(Enum):
    RIGHT = 1
    LEFT = -1

class State(Enum):
    IDLE = "Idle"
    FORWARD_WALK = "ForwardWalk"
    BACKWARD_WALK = "BackwardWalk"
    LUNGE_FORWARD = "LungeForward"
    HOP_BACKWARD = "HopBackward"
    PARRY = "Parry"
    HURT = "Hurt"

FREE_STATES = {State.IDLE, State.FORWARD_WALK, State.BACKWARD_WALK}

DEFAULT_LENGTHS = {
    State.LUNGE_FORWARD: 300,
    State.HOP_BACKWARD: 400,
    State.PARRY: 250,
    State.HURT: 400,
}

WALK_SPEED = 4
BACKWARD_SPEED = 3
DASH_SPEED = 40
LUNGE_SPEED = 12
HOP_SPEED = 8
HOP_FRICTION = 0.9
HURT_SPEED = 9
HURT_FRICTION = 0.85

class Player(pygame.sprite.Sprite):
    aabb: AABB
    vx: float
    vy: float
    facing: Facing
    state: State

    # values to change dash input timing
    held_cap = 15
    since_cap = 15

    def __init__(self, sheet: SpriteSheet, x, y, facing=Facing.RIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.animator = Animator(sheet)
        self.image = sheet.get(State.IDLE.value).frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.aabb = AABB(x, y, self.rect.w, self.rect.h)

        self.vx = 0; self.vy = 0
        self.facing = facing

        # dictionary containing keypresses and timers to track them
        self.press_dict = {
            "l" : {
                "held_time": 0,
                "since_time": float('inf'),
                "down": False,
                "prev": False
            },
            "r": {
                "held_time": 0,
                "since_time": float('inf'),
                "down": False,
                "prev": False
            },
        }

        self.state_time = 0
        self.state_length = 0
        self.set_state(State.IDLE)

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

    @property
    def free(self):
        return self.state in FREE_STATES

    @property
    def parrying(self):
        return self.state == State.PARRY

    def set_state(self, state: State):
        self.state = state
        self.state_time = 0

        sheet = self.animator.sheet
        if sheet.has(state.value):
            self.state_length = sheet.get(state.value).length
        else:
            self.state_length = DEFAULT_LENGTHS.get(state, 0)

        self.animator.play(state.value, loop=state in FREE_STATES, restart=True)

        match state:
            case State.HOP_BACKWARD:
                self.vx = -self.facing.value * HOP_SPEED
            case State.PARRY:
                self.vx = 0

    def lunge(self):
        if self.free:
            self.set_state(State.LUNGE_FORWARD)

    def hop_back(self):
        if self.free:
            self.set_state(State.HOP_BACKWARD)

    def parry(self):
        if self.free:
            self.set_state(State.PARRY)

    def hurt(self, direction=None):
        if direction is None:
            direction = -self.facing.value
        self.set_state(State.HURT)
        self.vx = direction * HURT_SPEED

    def tick(self, dt):
        # check for a dash move
        l_dash = self.increment_timers(self.press_dict["l"])
        r_dash = self.increment_timers(self.press_dict["r"])

        self.state_time += dt
        self._update_state()
        self._update_velocity(l_dash, r_dash)
        self.x += self.vx
        self.y += self.vy

        self.animator.update(dt)
        self.image = self.animator.image(flip=self.facing == Facing.LEFT)

        # store state at last tick
        self.press_dict["l"]["prev"] = self.press_dict["l"]["down"]
        self.press_dict["r"]["prev"] = self.press_dict["r"]["down"]

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

    def _input_direction(self):
        return int(self.press_dict["r"]["down"]) - int(self.press_dict["l"]["down"])

    def _update_state(self):
        if self.free:
            direction = self._input_direction()
            if direction == 0:
                new_state = State.IDLE
            elif direction == self.facing.value:
                new_state = State.FORWARD_WALK
            else:
                new_state = State.BACKWARD_WALK
            if new_state != self.state:
                self.set_state(new_state)

        elif self.state_time >= self.state_length:
            self.set_state(State.IDLE)

    def _update_velocity(self, l_dash=False, r_dash=False):
        match self.state:
            case State.IDLE | State.FORWARD_WALK | State.BACKWARD_WALK:
                self.vx *= 0.5
                if l_dash:
                    print("DASH LEFTTTT")
                    self.vx -= DASH_SPEED
                elif r_dash:
                    print("DASH RIGHTTTT")
                    self.vx += DASH_SPEED
                else:
                    speed = BACKWARD_SPEED if self.state == State.BACKWARD_WALK else WALK_SPEED
                    self.vx += self._input_direction() * speed * 0.5
            case State.LUNGE_FORWARD:
                progress = min(self.state_time / self.state_length, 1) if self.state_length else 1
                self.vx = self.facing.value * LUNGE_SPEED * (1 - progress)
            case State.HOP_BACKWARD:
                self.vx *= HOP_FRICTION
            case State.PARRY:
                self.vx = 0
            case State.HURT:
                self.vx *= HURT_FRICTION

        if abs(self.vx) < 0.01:
            self.vx = 0
