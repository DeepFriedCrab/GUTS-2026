import pygame
from Classes.player import load_frames
from Classes.animator import Animator, Animation

class Logo(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.logo_frames = load_frames('Assets/start/logo/')
        for i in range(len(self.logo_frames)):
            self.logo_frames[i] = pygame.transform.scale(self.logo_frames[i], (1024, 512))

        self.logo_animator = Animator(Animation(self.logo_frames, 100, 'repeat'))

        self.image = self.logo_frames[0]
        self.rect = self.image.get_rect(topleft=(250, 100))

    def update(self, dt):
        self.logo_animator.update(dt)
        self.image = self.logo_animator.image()