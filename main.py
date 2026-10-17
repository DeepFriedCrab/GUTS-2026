import pygame
from Classes.player import Player

pygame.init()

background_colour = (255,255,255)
(width, height) = (300, 200)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2fight')
screen.fill(background_colour)

pygame.display.flip()

def parse_keydown(key):
    match key:
        case pygame.K_a:
            print("a has been pressed")
        case pygame.K_d:
            print("d has been pressed")
        case pygame.K_j:
            print("j has been pressed")
        case pygame.K_l:
            print("l has been pressed")
        case _:
            print("Another key has been pressed")

p1 = Player()
p2 = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            parse_keydown(event.key)