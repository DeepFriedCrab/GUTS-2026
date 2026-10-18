import pygame
from Classes.player import load_frames
from Classes.animator import Animator, Animation

class Logo(pygame.sprite.Sprite):

    def __init__(self, file_dir, speed, pos):
        pygame.sprite.Sprite.__init__(self)

        self.logo_frames = load_frames(file_dir)
        for i in range(len(self.logo_frames)):
            self.logo_frames[i] = pygame.transform.scale(self.logo_frames[i], (1024, 512))

        self.logo_animator = Animator(Animation(self.logo_frames, speed, 'repeat'))

        self.image = self.logo_frames[0]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, dt):
        self.logo_animator.update(dt)
        self.image = self.logo_animator.image()