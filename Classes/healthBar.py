import pygame
import os 
from Classes.player import fill
from Classes.player import load_frames
from Classes.animator import Animator, Animation

class HealthBar(pygame.sprite.Sprite):


    def __init__(self, side,width):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_dict={}
        self.side= side

        self.sprite_dict[0] =  [pygame.image.load(os.path.join('Assets/healthBar/Empty.png'))]
        
        colours = [
                (158,29,2),
                (149,167,10),
                (28,97,0)
                ]
        for x in range(1,4):
            self.sprite_dict[x]= load_frames('Assets/healthBar/'+self.side+"/H"+str(x))
            for i in range(len(self.sprite_dict[x])):
                self.sprite_dict[x][i]  = pygame.transform.scale(self.sprite_dict[x][i], (580,self.sprite_dict[x][i].get_height()))
                fill(self.sprite_dict[x][i], pygame.Color(colours[x-1]))



        self.animator = Animator(Animation(self.sprite_dict[3], 400, 'repeat'))


        self.health = 3
        
        if side == "Left":
            self.rect = self.sprite_dict[self.health][0].get_rect(center=(250,70))
        elif side == "Right":
             self.rect = self.sprite_dict[self.health][0].get_rect(center=(width-250,70))
        else:
            raise RuntimeError("Health Bar must be left or right")

    def setHealth(self,health):
        if health != self.health:
            self.animator = Animator(Animation(self.sprite_dict[health], 400, 'repeat'))

        self.health = health
        
    def update(self, dt):
        self.animator.update(dt)
        self.image = self.animator.image()
