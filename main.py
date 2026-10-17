import pygame
from Classes.player import Player

background_colour = (255,255,255)
(width, height) = (300, 200)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2fight')
screen.fill(background_colour)

pygame.display.flip()

p1 = Player()
p2 = Player()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False