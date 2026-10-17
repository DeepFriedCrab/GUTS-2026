import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect(center=(30,30))

    x = 0
    y = 0
    vx = 0
    vy = 0

    facing = "right"

    action = "still"

    def move(self):
        self.rect.x += 1