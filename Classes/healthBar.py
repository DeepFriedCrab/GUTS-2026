import pygame
import os 

class HealthBar(pygame.sprite.Sprite):

    def __init__(self, side,width):
        pygame.sprite.Sprite.__init__(self)

        self.health = 3
        self.side= side
        self.image = pygame.image.load(os.path.join('Assets/healthBar/'+self.side+str(self.health)+'.png'))
        self.image = pygame.transform.scale(self.image, (580,self.image.get_height()))
        if side == "L":
            self.rect = self.image.get_rect(center=(250,70))
        elif side == "R":
             self.rect = self.image.get_rect(center=(width-250,70))
        else:
            raise RuntimeError("Health Bar must be left or right")

    def setHealth(self,health):
        self.health = health
        self.image = pygame.image.load(os.path.join('Assets/healthBar/'+self.side+str(self.health)+'.png'))

