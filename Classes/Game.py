import pygame
from Classes.player import Player, Facing, BoxState,State
from Classes.healthBar import HealthBar
from Classes.Logo import Logo

class Game:
    window_dimensions =  (1500, 1000)
    ground_y = 4*window_dimensions[1]/5 


    def __init__(self):
        pygame.init()
        self.background_colour = (25,24,26) #(171,170,170)
        self.screen = pygame.display.set_mode(self.window_dimensions)

        pygame.display.set_caption('2Fight')

        self.all_sprites_list = pygame.sprite.Group()

        self.healthbarL = HealthBar("Left",self.window_dimensions[0])
        self.healthbarR = HealthBar("Right",self.window_dimensions[0])
       
        self.p1 = Player( 0, 0, Facing.LEFT)
        self.p2 = Player( 0, 0, Facing.RIGHT)
        self.p1.x = 50
        self.p2.x = self.window_dimensions[0] - 50 - self.p2.aabb.w
        self.p1.rect.y = self.ground_y - self.p1.aabb.h + 70
        self.p2.rect.y = self.ground_y - self.p2.aabb.h + 70
        # Who's facing right
        self.facing_right = "p2"


    def Start(self):
        clock = pygame.time.Clock()
        logo = Logo('Assets/start/logo/', 100, (250, 100))
        self.all_sprites_list.add(logo)

        while True:
            dt = clock.tick(60)

            # display logo
            self.screen.fill(self.background_colour)
            self.all_sprites_list.draw(self.screen)
            logo.update(dt)

            # display startup text
            font = pygame.font.SysFont("consolas", 36)
            txtsurf = font.render("< press any button to start >", True, (200,200,200))
            self.screen.blit(txtsurf,(self.window_dimensions[0]/2 - txtsurf.get_width() // 2, self.ground_y - txtsurf.get_height() // 2))
            #pygame.display.update()

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.all_sprites_list.remove(logo)
                    self.all_sprites_list.add(self.healthbarL)
                    self.all_sprites_list.add(self.healthbarR)
                    self.all_sprites_list.add(self.p1)
                    self.all_sprites_list.add(self.p2)
                    self.run()

    def End(self):
        self.all_sprites_list.remove(self.healthbarL)
        self.all_sprites_list.remove(self.healthbarR)
        self.all_sprites_list.remove(self.p1)
        self.all_sprites_list.remove(self.p2)

        clock = pygame.time.Clock()
        logo = Logo('Assets/end/round_over/', 150, (220, 100))
        self.all_sprites_list.add(logo)

        while True:
            dt = clock.tick(200)

            # display logo
            self.screen.fill(self.background_colour)
            self.all_sprites_list.draw(self.screen)
            logo.update(dt)

            # display startup text
            font = pygame.font.SysFont("consolas", 36)
            txt1 = font.render("< press 'a' to restart >", True, (200,200,200))
            txt2 = font.render("< press 'd' to quit >", True, (200,200,200))
            self.screen.blit(txt1,(self.window_dimensions[0]/2 - txt1.get_width() // 2, self.ground_y - txt1.get_height() // 2))
            self.screen.blit(txt2,(self.window_dimensions[0]/2 - txt2.get_width() // 2, self.ground_y + 50 - txt2.get_height() // 2))
            #pygame.display.update()

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.__init__()
                        self.Start()
                    elif event.key == pygame.K_d:
                        pygame.quit()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True 
        in_round = True
        end_timer = 0
        while running:
            dt = clock.tick(60)

            if not in_round:
                end_timer += 1

                if end_timer > 100:
                    self.End()
        
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
            self.healthbarL.update(dt)
            self.healthbarR.update(dt)
            self.screen.fill(self.background_colour)

            pygame.draw.rect(self.screen, (78,22,108), pygame.Rect(0,130, self.window_dimensions[0]/3 , 5 ))
            pygame.draw.rect(self.screen, (66,62,101), pygame.Rect(self.window_dimensions[0]-self.window_dimensions[0]/3,130, self.window_dimensions[0]/3 , 5 ))
           

            self.all_sprites_list.draw(self.screen)
            ground = pygame.image.load('Assets/Ground/Ground.png')
            self.screen.blit(ground, (0, self.ground_y))

            
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

    def handle_collision(self):
        if self.p1.state == State.DEAD or self.p2.state == State.DEAD:
            return 

        if self.p1.aabb.is_overlapping(self.p2.aabb):
            match (self.p1.boxstate, self.p2.boxstate):
                case (BoxState.REST, BoxState.DAMAGE):
                    # damage p1
                    if self.p1.parryTimer > 50: 
                        self.p1.set_state(State.HURT)
                        self.p1.damage()
                        self.p1.bounce()

                        # bounce puncher back
                        self.p2.bounce()
                case (BoxState.DAMAGE, BoxState.REST):
                    # damage p2
                    if self.p2.parryTimer > 50: 
                        self.p2.set_state(State.HURT)
                        self.p2.damage()
                        self.p2.bounce()

                        # bounch puncher back
                        self.p1.bounce()
                case (BoxState.BLOCK, BoxState.DAMAGE):
                    # parry doesnt carry tired state
                    self.p1.parryTimer = 0
                    self.p1.set_state(State.SUCCESSFUL_PARRY)


                case (BoxState.DAMAGE, BoxState.BLOCK):
                    # parry doesnt carry tired state
                    self.p2.parryTimer = 0
                    self.p2.set_state(State.SUCCESSFUL_PARRY)
                    

                case (BoxState.DAMAGE, BoxState.DAMAGE):
                    # bounce apart when two attacks meet
                    self.p1.bounce()
                    self.p2.bounce()

    def check_wall_collision(self, player):
        if player.x < -25:
            player.vx = 0
            player.x = -25

        elif player.x + player.aabb.w > self.window_dimensions[0] + 25:
            player.vx = 0

            player.x = self.window_dimensions[0] - player.aabb.w + 25

