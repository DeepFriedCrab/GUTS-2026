import pygame
import os 

class HealthBar(pygame.sprite.Sprite):

    def __init__(self, side,ground_y,width):
        pygame.sprite.Sprite.__init__(self)

        self.health = 3
        self.side= side
        self.image = pygame.image.load(os.path.join('Assets/healthBar/'+self.side+str(self.health)+'.png'))
        
        if side == "L":
            self.rect = self.image.get_rect(center=(210,ground_y+70))
        elif side == "R":
             self.rect = self.image.get_rect(center=(width-210,ground_y+70))
        else:
            raise RuntimeError("Health Bar must be left or right")

    def setHealth(self,health):
        self.health = health
        self.image = pygame.image.load(os.path.join('Assests/healthBar/'+self.side+str(self.health)+'.png'))

