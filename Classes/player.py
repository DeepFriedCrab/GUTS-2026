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

        self.rect.x += self.vx
        self.rect.y += self.vy