import pygame 
from Player import Player
import sys
pygame.init()

# Display
width, height = 960, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Twisted Wizards")
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (width, height))
ground_y = 600

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)


clock = pygame.time.Clock()
gameRunning = True

def draw_health(health, x, y):
    health_ratio = health / 100
    pygame.draw.rect(screen, black, (x - 1, y - 1, 352, 32))  # Outline of health bar
    pygame.draw.rect(screen, red, (x, y, 350, 30))  # Background of health bar
    pygame.draw.rect(screen, green, (x, y, 350 * health_ratio, 30))

# Player Instances
player_height = 190
player1 = Player(50, ground_y - player_height)
player2 = Player(800, ground_y - player_height)  # Placeholder for player2

pygame.mixer.init()
pygame.mixer.music.load("assets/Mountkid.mp3")  # or .wav
pygame.mixer.music.play(-1)  # -1 = loop forever
pygame.mixer.music.set_volume(0.5)  # Optional: volume from 0.0 to 1.0


while gameRunning:
    # Event Handler
    clock.tick(60)  # Frame rate
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    # Draw 
    screen.blit(background, (0, 0))

    # Health Bars
    draw_health(player1.health, 20, 20)
    draw_health(player2.health, 580, 20)

    # Player Movement
    player1.move(width, ground_y, screen, player2)
    # player2.move(width, ground_y, screen, player1)  # Assuming player2 has a move method

    # player2.move()

     # Draw Players
    player1.draw(screen)
    player2.draw(screen)  # Assuming player2 has a draw method
    # player2.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()