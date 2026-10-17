import pygame

class Start:
    window_dimensions =  (1920, 1080)

    def __init__(self):
        pygame.init()
        self.background_colour = (0,0,0) #(171,170,170)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.display.set_caption('2Fight')

        self.all_sprites_list = pygame.sprite.Group()
       
        self.p1 = Player( 50, 490, Facing.LEFT)
        self.p2 = Player( 1600, 490, Facing.RIGHT)

        # Who's facing right
        self.facing_right = "p2"


        self.all_sprites_list.add(self.p1)
        self.all_sprites_list.add(self.p2)
        self.all_sprites_list.add(self.healthbarL)
        self.all_sprites_list.add(self.healthbarR)
        
    def run(self):
        clock = pygame.time.Clock()
        running = True 
        in_round = True
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

            # ----------------- player stuff ------------------- #
            # check collisions
            self.handle_collision()
            self.check_wall_collision(self.p1)
            self.check_wall_collision(self.p2)

            # tick player logic
            self.p1.tick(dt)
            self.p2.tick(dt)
            
            if in_round:
                # Flips players
                if self.p1.x < self.p2.x:
                    self.p1.facing = Facing.LEFT
                    self.p2.facing = Facing.RIGHT

                if self.p1.x >= self.p2.x:
                    self.p2.facing = Facing.LEFT
                    self.p1.facing = Facing.RIGHT

            if in_round:
                # --------------- health stuff --------------------- #
                self.healthbarL.setHealth(self.p1.health)
                self.healthbarR.setHealth(self.p2.health)


                if self.p1.health == 0:
                    self.p1.set_state(State.DEAD)
                    in_round = False
                if self.p2.health == 0:
                    self.p2.set_state(State.DEAD)
                    in_round = False


            # ------------ drawing stuff ------------- #
            self.screen.fill(self.background_colour)
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(0,self.ground_y, self.window_dimensions[0] , self.window_dimensions[1] - self.ground_y + 1 ))

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