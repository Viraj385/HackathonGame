import pygame 
from Player import Player
import sys
pygame.init()

# Display Window
width, height = 960, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Twisted Wizards")
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (width, height))
ground_y = 500

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

clock = pygame.time.Clock()
gameRunning = True


# Player Instances
player_height = 120
player1 = Player(50, ground_y - player_height)

while gameRunning:
    # Event Handler
    clock.tick(60)  # Frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    # Draw 
    screen.blit(background, (0, 0))

    # Player Movement
    player1.move(width, ground_y)

    # player2.move()

     # Draw Players
    player1.draw(screen)
    # player2.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()