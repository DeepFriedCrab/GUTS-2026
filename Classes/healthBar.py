import pygame
import os 
from Classes.player import fill

class HealthBar(pygame.sprite.Sprite):


    def __init__(self, side,width):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_dict={}
        self.side= side

        self.sprite_dict[0] =  self.image = pygame.image.load(os.path.join('Assets/healthBar/Empty.png'))

        for i in range(1,4):
            self.sprite_dict[i] = pygame.image.load(os.path.join('Assets/healthBar/'+self.side+str(i)+'.png'))
            self.sprite_dict[i] = pygame.transform.scale(self.sprite_dict[i], (580,self.sprite_dict[i].get_height()))
 
            fill(self.sprite_dict[i], pygame.Color(0,255,255))
        self.health = 3
        
        if side == "L":
            self.rect = self.sprite_dict[self.health].get_rect(center=(250,70))
        elif side == "R":
             self.rect = self.sprite_dict[self.health].get_rect(center=(width-250,70))
        else:
            raise RuntimeError("Health Bar must be left or right")

    def setHealth(self,health):
        self.health = health
        self.image = self.sprite_dict[health]


