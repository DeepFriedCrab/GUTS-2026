import pygame
from Classes.player import Player, Facing, BoxState,State
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

        # Who's facing right
        self.facing_right = "p2"


        self.all_sprites_list.add(self.p1)
        self.all_sprites_list.add(self.p2)
        self.all_sprites_list.add(self.healthbarL)
        self.all_sprites_list.add(self.healthbarR)
        
    def run(self):
        clock = pygame.time.Clock()
        running = True 
        
        while running:
            dt = clock.tick(60)

            # ------------- check events ---------------- #
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
            self.handle_collision(self.p1, self.p2)

            # tick player logic
            self.p1.tick(dt)
            self.p2.tick(dt)

            # Flips players
            if self.p1.x < self.p2.x:
                self.p1.facing = Facing.LEFT
                self.p2.facing = Facing.RIGHT

            if self.p1.x >= self.p2.x:
                self.p2.facing = Facing.LEFT
                self.p1.facing = Facing.RIGHT

            # ------------ drawing stuff ------------- #
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

    def handle_collision(self, p1, p2):
        if p1.aabb.is_overlapping(p2.aabb):
            match (p1.boxstate, p2.boxstate):
                case (BoxState.REST, BoxState.DAMAGE):
                    # damage p1
                    print("DAMAGE P1")
                    self.p1.set_state(State.HURT)
                    pass
                case (BoxState.DAMAGE, BoxState.REST):
                    # damage p2
                    print("DAMAGE P2")
                    self.p2.set_state(State.HURT)
                    pass
                case (BoxState.BLOCK, BoxState.DAMAGE):
                    # parry doesnt carry tired state
                    print("P1 BLOCKED")
                    pass
                case (BoxState.DAMAGE, BoxState.BLOCK):
                    # parry doesnt carry tired state
                    print("P2 BLOCKED")
                    pass
                case (BoxState.DAMAGE, BoxState.DAMAGE):
                    # bounce apart
                    print("BOUNCE APART")
                    pass
                case _:
                    print("calm")
                    pass
