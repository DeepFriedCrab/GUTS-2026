import pygame
from Classes.player import Player, Facing
from Classes.healthBar import HealthBar


class Game:
    window_dimensions =  (1200, 800)
    ground_y = 4*window_dimensions[1]/5 

    healthbarL = HealthBar("L",window_dimensions[0])
    healthbarR = HealthBar("R",window_dimensions[0])
    def __init__(self):
        pygame.init()
        self.background_colour = (171,170,170)
        self.screen = pygame.display.set_mode(self.window_dimensions)

        pygame.display.set_caption('2Fight')

        self.all_sprites_list = pygame.sprite.Group()
       
        self.p1 = Player( 50, 255, Facing.LEFT)
        self.p2 = Player( 450, 255, Facing.RIGHT)


        self.all_sprites_list.add(self.p1)
        self.all_sprites_list.add(self.p2)
        self.all_sprites_list.add(self.healthbarL)
        self.all_sprites_list.add(self.healthbarR)
        
    def run(self):
        clock = pygame.time.Clock()
        running = True 
        
        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # checks key inputs
                elif event.type == pygame.KEYDOWN:
                    self.parse_keydown(event.key)

                elif event.type == pygame.KEYUP:
                    self.parse_keyup(event.key)
            
            # tick player logic
            self.p1.tick(dt)
            self.p2.tick(dt)

            self.screen.fill(self.background_colour)
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0,self.ground_y, self.window_dimensions[0] , self.window_dimensions[1] - self.ground_y + 1 ))

            self.all_sprites_list.draw(self.screen)
            pygame.display.flip()

        pygame.quit()

    def parse_keydown(self, key):
        match key:
            case pygame.K_a:
                self.p1.press_dict["l"]["down"] = True
            case pygame.K_d:
                self.p1.press_dict["r"]["down"] = True
                
            case pygame.K_j:
                self.p2.press_dict["l"]["down"] = True
            case pygame.K_l:
                self.p2.press_dict["r"]["down"] = True

    def parse_keyup(self, key):
        match key:
            case pygame.K_a:
                self.p1.press_dict["l"]["down"] = False
            case pygame.K_d:
                self.p1.press_dict["r"]["down"] = False

            case pygame.K_j:
                self.p2.press_dict["l"]["down"] = False
            case pygame.K_l:
                self.p2.press_dict["r"]["down"] = False
