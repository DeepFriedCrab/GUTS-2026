import pygame
from Classes.player import Player, Facing, BoxState,State, fill
from Classes.healthBar import HealthBar



class Game:
    window_dimensions =  (1920, 1080)
    ground_y = 4*window_dimensions[1]/5 

    healthbarL = HealthBar("L",window_dimensions[0])
    healthbarR = HealthBar("R",window_dimensions[0])

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
                    self.p1
                case (BoxState.DAMAGE, BoxState.BLOCK):
                    # parry doesnt carry tired state
                    self.p2.parryTimer = 0
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

