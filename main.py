import pygame
import os

testface = pygame.image.load(os.path.join('testface.png'))

class Testface(pygame.sprite.Sprite):

    def __init__(self ):
       pygame.sprite.Sprite.__init__(self)
       self.image = testface
       self.rect = self.image.get_rect(center=(30,30))

    def move(self):
        self.rect.x += 1

class Game:
    def __init__(self):
        self.background_colour = (255,255,255)

        (width, height) = (300, 200)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('2Fight')

        self.all_sprites_list = pygame.sprite.Group()
        object_ = Testface()
        object_.rect.x = 50
        object_.rect.y = 50  

        self.all_sprites_list.add(object_)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
          self.screen.fill(self.background_colour)
          self.all_sprites_list.update() 
          box = self.all_sprites_list.sprites()[0].move()
          self.all_sprites_list.draw(self.screen) 
          clock.tick(60) 
          pygame.display.flip()
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False


if __name__ == '__main__':
    Game().run()
