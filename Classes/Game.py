import pygame
import os
from Classes.player import Player


testface = pygame.image.load(os.path.join('assets/stickman_test.png'))


class Testface(pygame.sprite.Sprite):

    def __init__(self ):
       pygame.sprite.Sprite.__init__(self)
       self.image = testface
       self.rect = self.image.get_rect(center=(30,30))

    def move(self):
        self.rect.x += 1


class Game:
    p1 = Player(testface, 0, 0, 50, 100)
    p2 = Player(testface, 0, 0, 50, 100)

    def __init__(self):
        pygame.init()
        self.background_colour = (255,255,255)
        self.window_dimensions =  (640, 360)
        self.ground_y = 4*self.window_dimensions[1]/5 
        self.screen = pygame.display.set_mode(self.window_dimensions, pygame.SCALED)
        pygame.display.set_caption('2Fight')

        self.all_sprites_list = pygame.sprite.Group()
        self.p1.x = 50
        self.p1.y = 50  

        self.all_sprites_list.add(self.p1)

    def run(self):
        clock = pygame.time.Clock()
        running = True 
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # checks key inputs
                elif event.type == pygame.KEYDOWN:
                    self.parse_keydown(event.key)

                elif event.type == pygame.KEYUP:
                    self.parse_keyup(event.key)
            
            
            # move players
            self.p1.move()
            self.p2.move()
                
            self.screen.fill(self.background_colour)
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0,self.ground_y, self.window_dimensions[0] , self.window_dimensions[1] - self.ground_y ))  

            self.all_sprites_list.update() 
            #box = self.all_sprites_list.sprites()[0].move()
            self.all_sprites_list.draw(self.screen) 
            clock.tick(60) 
            pygame.display.flip()

    def parse_keydown(self, key):
        match key:
            case pygame.K_a:
                print("a has been pressed")
                self.p1.ldown = True
            case pygame.K_d:
                print("d has been pressed")
                self.p1.rdown = True
            case pygame.K_j:
                print("j has been pressed")
            case pygame.K_l:
                print("l has been pressed")
            case _:
                print("Another key has been pressed")

    def parse_keyup(self, key):
            match key:
                case pygame.K_a:
                    print("a has been lifted")
                    self.p1.ldown = False
                case pygame.K_d:
                    print("d has been lifted")
                    self.p1.rdown = False
                case pygame.K_j:
                    print("j has been lifted")
                case pygame.K_l:
                    print("l has been lifted")
                case _:
                    print("Another key has been lifted")
