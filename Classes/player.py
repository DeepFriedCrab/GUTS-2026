import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect(center=(30,30))

    ldown = False
    rdown = False
    x = 0
    y = 0
    vx = 0
    vy = 0

    facing = "right"

    action = "still"

    def move(self):
        match (self.ldown, self.rdown):
            case (False, False):
                pass
            case (False, True):
                self.rect.x += 3
            case (True, False):
                self.rect.x -= 3
            case (True, True):
                pass