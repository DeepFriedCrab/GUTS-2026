from enum import Enum

import pygame
import os
from Classes.aabb import AABB
from Classes.spritesheet import Animator, Animation

class Facing(Enum):
    RIGHT = 1
    LEFT = -1

class BoxState(Enum):
    REST = "Rest"
    DAMAGE = "Damage"
    BLOCK = "Block"

class State(Enum):
    IDLE = "Idle"
    FORWARD_WALK = "ForwardWalk"
    BACKWARD_WALK = "BackwardWalk"
    DASH_FORWARD = "DashForward"
    DASH_BACK = "DashBack"
    PARRY = "Parry"
    HURT = "Hurt"
    TIRED = "Tired"

FREE_STATES = {State.IDLE, State.FORWARD_WALK, State.BACKWARD_WALK}

DEFAULT_LENGTHS = {
    State.DASH_FORWARD: 300,
    State.DASH_BACK: 300,
    State.PARRY: 250,
    State.HURT: 400,
    State.TIRED: 400,
}

WALK_SPEED = 6
BACKWARD_SPEED = WALK_SPEED *.75

DASH_SPEED = 30
DASH_FRICTION = 0.9

HURT_SPEED = 9
HURT_FRICTION = 0.85


def load_frames(folder_dir):
    frames = []
    for images in os.listdir(folder_dir):
        frames.append(pygame.image.load(folder_dir+"/"+images))
    return frames

def get_asset(x):
    frames = []
    match x:
        case State.IDLE:
           frames = load_frames("Assets/stick/idle") 
        case State.FORWARD_WALK:
           frames = load_frames("Assets/stick/walkfoward") 
        case State.BACKWARD_WALK:
           frames = load_frames("Assets/stick/walkback") 
        case State.DASH_FORWARD:
           frames = load_frames("Assets/stick/dashFoward") 
        case State.DASH_BACK:
           frames = load_frames("Assets/stick/dashBack") 
        case State.PARRY:
           frames = load_frames("Assets/stick/block") 
        case State.HURT:
           frames = load_frames("Assets/stick/idle") 
        case State.TIRED:
           frames = load_frames("Assets/stick/idle") 
    return frames


class Player(pygame.sprite.Sprite):
    aabb: AABB
    vx: float
    vy: float
    facing: Facing
    state: State
    boxstate: BoxState

    # values to change dash input timing
    held_cap = 15
    since_cap = 15

    def __init__(self , x, y, facing=Facing.RIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.set_state(State.IDLE)
        self.frames = get_asset(self.state)
        self.animator = Animator(Animation(self.frames, 300,))
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.aabb = AABB(x, y, self.rect.w, self.rect.h)
        self.boxstate = BoxState.REST

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
        self.frames = get_asset(self.state)
        self.animator = Animator(Animation(self.frames, 300,))
        self.state_length = DEFAULT_LENGTHS.get(state,0)

        # change bounding box state based on new state
        match state:
            case State.DASH_FORWARD:
                self.boxstate = BoxState.DAMAGE
            case State.PARRY:
                self.boxstate = BoxState.BLOCK
            case _:
                self.boxstate = BoxState.REST

    def tick(self, dt):
        # check for a dash move
        parry = self.check_parry(self.press_dict)
        l_dash = self.increment_timers(self.press_dict["l"])
        r_dash = self.increment_timers(self.press_dict["r"])

        self.state_time += dt
        self._update_state(parry)
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

    # returns if a parry is detected based on keypresses
    def check_parry(self, dicty):
        return dicty["l"]["down"] and dicty["r"]["down"] and dicty["l"]["held_time"] < self.held_cap and dicty["r"]["held_time"] < self.held_cap

    def _input_direction(self):
        return int(self.press_dict["r"]["down"]) - int(self.press_dict["l"]["down"])

    def _update_state(self, parry=False):
        if self.free:
            
            match (int(self.press_dict["l" if self.facing == Facing.RIGHT else "r"]["down"]), int(self.press_dict["r" if self.facing == Facing.RIGHT else "l"]["down"])):
                case (0, 0):
                    new_state = State.IDLE
                case (1, 0):
                    new_state = State.FORWARD_WALK
                case (0, 1):
                    new_state = State.BACKWARD_WALK
                case (1, 1):
                    if parry:
                        new_state = State.PARRY
                    else:
                        new_state = self.state

            if new_state != self.state:
                self.set_state(new_state)

        elif self.state_time >= self.state_length:
            if self.state == State.DASH_FORWARD or self.state == State.DASH_BACK:
                self.set_state(State.TIRED)
            elif self.state == State.PARRY:
                self.set_state(State.TIRED)
            else:
                self.set_state(State.IDLE)

    def _update_velocity(self, l_dash=False, r_dash=False):
        match self.state:
            case State.IDLE | State.FORWARD_WALK | State.BACKWARD_WALK:
                self.vx *= 0.5
                if l_dash:
                    self.set_state(State.DASH_BACK if self.facing == Facing.LEFT else State.DASH_FORWARD)
                    self.vx -= DASH_SPEED
                elif r_dash:
                    self.set_state(State.DASH_BACK if self.facing == Facing.RIGHT else State.DASH_FORWARD)
                    self.vx += DASH_SPEED
                else:
                    speed = BACKWARD_SPEED if self.state == State.BACKWARD_WALK else WALK_SPEED
                    self.vx += self._input_direction() * speed * 0.5
            case State.DASH_FORWARD:
                self.vx *= DASH_FRICTION
            case State.DASH_BACK:
                self.vx *= DASH_FRICTION
            case State.PARRY:
                self.vx = 0
            case State.HURT:
                self.vx *= HURT_FRICTION
            case State.TIRED:
                self.vx *= 0

        if abs(self.vx) < 0.01:
            self.vx = 0
