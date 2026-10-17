import pygame

background_colour = (255,255,255)
(width, height) = (300, 200)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2fight')
screen.fill(background_colour)

pygame.display.flip()

class Player:
    x = 0
    y = 0
    vx = 0
    vy = 0

    facing = "right"

    parrying = False
  
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False