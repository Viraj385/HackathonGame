import pygame 
import sys
pygame.init()

# Display Window
width, height = 960, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Twisted Wizards")

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)

clock = pygame.time.Clock()
gameRunning = True

while gameRunning:
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    keys = pygame.key.get_pressed()

pygame.quit()
