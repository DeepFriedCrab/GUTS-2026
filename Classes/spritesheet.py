import json
import os

import pygame


class Animation:
    def __init__(self, frames, durations, direction="forward"):
        order = list(range(len(frames)))
        match direction:
            case "reverse":
                order.reverse()
            case "pingpong":
                order = order + order[-2:0:-1]
            case "pingpong_reverse":
                order.reverse()
                order = order + order[-2:0:-1]

        self.frames = [frames[i] for i in order]
        self.flipped = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.durations = [durations[i] for i in order]
        self.length = sum(self.durations)

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


class SpriteSheet:
    def __init__(self, image_path, json_path=None, scale=1, default="Idle"):
        image = pygame.image.load(image_path)
        if pygame.display.get_surface() is not None:
            image = image.convert_alpha()

        if json_path is None:
            candidate = os.path.splitext(image_path)[0] + ".json"
            if os.path.exists(candidate):
                json_path = candidate

        self.default = default
        self.animations = {}

        if json_path is None:
            frame = pygame.transform.scale_by(image, scale)
            self.animations[default] = Animation([frame], [100])
            self.size = frame.get_size()
            return

        with open(json_path) as f:
            data = json.load(f)

        entries = data["frames"]
        if isinstance(entries, dict):
            entries = list(entries.values())

        frames = [self._cut(image, entry, scale) for entry in entries]
        durations = [entry.get("duration", 100) for entry in entries]

        for tag in data.get("meta", {}).get("frameTags", []):
            start, end = tag["from"], tag["to"] + 1
            self.animations[tag["name"]] = Animation(
                frames[start:end], durations[start:end], tag.get("direction", "forward"))

        if not self.animations:
            self.animations[default] = Animation(frames, durations)

        self.size = frames[0].get_size()

    def _cut(self, image, entry, scale):
        frame = entry["frame"]
        offset = entry.get("spriteSourceSize", {"x": 0, "y": 0})
        size = entry.get("sourceSize", {"w": frame["w"], "h": frame["h"]})

        canvas = pygame.Surface((size["w"], size["h"]), pygame.SRCALPHA)
        canvas.blit(image, (offset["x"], offset["y"]),
                    pygame.Rect(frame["x"], frame["y"], frame["w"], frame["h"]))

        if scale != 1:
            canvas = pygame.transform.scale_by(canvas, scale)
        return canvas

    def has(self, name):
        return name in self.animations

    def get(self, name):
        if name in self.animations:
            return self.animations[name]
        if self.default in self.animations:
            return self.animations[self.default]
        return next(iter(self.animations.values()))


class Animator:
    def __init__(self, sheet):
        self.sheet = sheet
        self.name = None
        self.animation = sheet.get(sheet.default)
        self.time = 0
        self.loop = True

    def play(self, name, loop=True, restart=False):
        if name == self.name and not restart:
            return
        self.name = name
        self.animation = self.sheet.get(name)
        self.time = 0
        self.loop = loop

    def update(self, dt):
        self.time += dt

    @property
    def finished(self):
        return not self.loop and self.time >= self.animation.length

    def image(self, flip=False):
        return self.animation.frame_at(self.time, self.loop, flip)
