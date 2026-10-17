from enum import Enum

import pygame
import os
from Classes.aabb import AABB
from Classes.animator import Animator, Animation

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
    SUCCESSFUL_PARRY = "SuccessfulParry"
    HURT = "Hurt"
    TIRED = "Tired"
    DEAD = "Dead"

FREE_STATES = {State.IDLE, State.FORWARD_WALK, State.BACKWARD_WALK}

DEFAULT_LENGTHS = {
    State.DASH_FORWARD: 300,
    State.DASH_BACK: 300,
    State.PARRY: 250,
    State.HURT: 400,
    State.TIRED: 400,
    State.DEAD: 400,
}

WALK_SPEED = 6
BACKWARD_SPEED = WALK_SPEED *.75

DASH_SPEED = 30
DASH_FRICTION = 0.9

HURT_SPEED = 9
HURT_FRICTION = 0.85


def load_frames(folder_dir):
    files = []
    for image in os.listdir(folder_dir):
        files.append(image)
    
    frames = []
    for image in sorted(files):
        frames.append(pygame.image.load(folder_dir+"/"+image))
    return frames


# recolouring code from
# https://stackoverflow.com/questions/42821442/how-do-i-change-the-colour-of-an-image-in-pygame-without-changing-its-transparen
def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))




class Player(pygame.sprite.Sprite):
    aabb: AABB
    vx: float
    facing: Facing
    state: State
    prevState: State
    boxstate: BoxState
    health: int
    parryTimer = int

    # values to change dash input timing
    held_cap = 15
    since_cap = 15

    def __init__(self , x, y, facing=Facing.RIGHT):

        # Loads sprite in silly style
        self.sprite_dict = {
            "idle": load_frames("Assets/stick/idle"),
            "walkfoward": load_frames("Assets/stick/walkfoward") ,
            "walkback": load_frames("Assets/stick/walkback") ,
            "dashForward": load_frames("Assets/stick/dashFoward") ,
            "dashBack": load_frames("Assets/stick/dashBack") ,
            "block": load_frames("Assets/stick/block") ,
            "sucblock": load_frames("Assets/stick/succesffulblock" ) ,
            "hurt": load_frames("Assets/stick/hurt") ,
            "tired": load_frames("Assets/stick/tired"),
            "dead":load_frames("Assets/stick/defete")
        }

        # Recolours the frames
        for sprite_frames in list(self.sprite_dict.values()):
            for frame in sprite_frames:
                if facing==Facing.LEFT:
                    fill(frame, pygame.Color(255,255,255))
                else:
                    fill(frame, pygame.Color(210,210,210))

        for fram in self.sprite_dict["hurt"]:
            fill(fram, pygame.Color(255,0,0))
        for fram in self.sprite_dict["sucblock"]:
            fill(fram, pygame.Color(103,235,252))

        
        pygame.sprite.Sprite.__init__(self)
        self.state = State.IDLE
        self.set_state(State.IDLE)
        self.frames = self.get_asset(self.state)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.aabb = AABB(x, y, self.rect.w, self.rect.h)
        self.boxstate = BoxState.REST
        self.health = 3
        self.parryTimer = 1000000000000


        self.vx = 0
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







    def get_asset(self, x):
        frames = []
        match x:
            case State.IDLE:
                frames = self.sprite_dict["idle"]
            case State.FORWARD_WALK:
                frames = self.sprite_dict["walkfoward"]
            case State.BACKWARD_WALK:
                frames = self.sprite_dict["walkback"]
            case State.DASH_FORWARD:
                frames = self.sprite_dict["dashForward"]
            case State.DASH_BACK:
                frames = self.sprite_dict["dashBack"]
            case State.PARRY:
                frames = self.sprite_dict["block"]
            case State.HURT:
                frames = self.sprite_dict["hurt"]
            case State.TIRED:
                frames = self.sprite_dict["tired"]
            case State.DEAD:
                frames = self.sprite_dict["dead"]
            case State.SUCCESSFUL_PARRY:
                frames = self.sprite_dict["sucblock"]
        return frames

    @property
    def x(self):
        return self.aabb.x

    @x.setter
    def x(self, x):
        self.aabb.x = x
        self.rect.x = round(x)

    @property
    def free(self):
        return self.state in FREE_STATES

    @property
    def parrying(self):
        return self.state == State.PARRY

    def set_state(self, state: State):
        if self.state == State.DEAD:
            return
        self.prevState = self.state
        self.state = state
        self.state_time = 0
        self.frames = self.get_asset(self.state)
        self.animator = Animator(Animation(self.frames, 300,"once" if self.state == State.DEAD else "repeat"))
        print(state)
        if state != State.SUCCESSFUL_PARRY:
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
        self.parryTimer += 1
        l_dash = self.increment_timers(self.press_dict["l"])
        r_dash = self.increment_timers(self.press_dict["r"])

        self.state_time += dt
        self._update_state(parry)
        self._update_velocity(l_dash, r_dash)
        self.x += self.vx

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
        if self.state == State.DEAD:
            return
        elif self.free:
            
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
            if self.state == State.DASH_FORWARD :
                self.set_state(State.TIRED)
            elif self.state == State.PARRY and self.parryTimer > 50:

                self.set_state(State.TIRED)
            else:
                self.set_state(State.IDLE)

    def _update_velocity(self, l_dash=False, r_dash=False):
        match self.state:
            case State.IDLE | State.FORWARD_WALK | State.BACKWARD_WALK:
                self.vx *= 0.5
                if l_dash:
                    self.set_state(State.DASH_BACK if self.facing == Facing.LEFT else State.DASH_FORWARD)
                    self.vx -= DASH_SPEED * (0.7 if self.state == State.DASH_BACK else 1)
                elif r_dash:
                    self.set_state(State.DASH_BACK if self.facing == Facing.RIGHT else State.DASH_FORWARD)
                    self.vx += DASH_SPEED * (0.7 if self.state == State.DASH_BACK else 1)
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
            case State.DEAD:
                self.vx *= 0

        if abs(self.vx) < 0.01:
            self.vx = 0

    def bounce(self):
        if self.facing == Facing.LEFT:
            self.vx -= DASH_SPEED * 2
        elif self.facing == Facing.RIGHT:
            self.vx += DASH_SPEED * 2

    def damage(self):
        if self.prevState != State.HURT:
            self.health -= 1
