import json
import os

import pygame


class Animation:
    def __init__(self, frames, duration):
        order = list(range(len(frames)))
        self.frames = [frames[i] for i in order]
        self.flipped = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.durations = [duration for i in order]
        self.length = duration*(len(frames))

    def frame_at(self, time, loop=True, flip=False):
        frames = self.flipped if flip else self.frames
        if self.length <= 0:
            return frames[0]
        if loop:
            time %= self.length
        for frame, duration in zip(frames, self.durations):
            if time < duration:
                return frame
            time -= duration
        return frames[-1]


class Animator:
    def __init__(self, animation):
        self.name = None
        self.animation = animation
        self.time = 0
        self.loop = True

    def play(self, name, loop=True, restart=False):
        if name == self.name and not restart:
            return
        self.name = name
        self.time = 0
        self.loop = loop

    def update(self, dt):
        self.time += dt

    @property
    def finished(self):
        return not self.loop and self.time >= self.animation.length

    def image(self, flip=False):
        return self.animation.frame_at(self.time, self.loop, flip)
