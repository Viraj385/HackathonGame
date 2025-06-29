import pygame 
import sys
pygame.init()

# Display Window
width, height = 960, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Twisted Wizards")
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

clock = pygame.time.Clock()
gameRunning = True

# Player Basic Setup
player_size = (50, 50)
player = pygame.Rect(100, height - 100, *player_size)
player_color = red
player_speed = 5

while gameRunning:
    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Draw 
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, player_color, player)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()