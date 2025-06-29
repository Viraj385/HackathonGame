import pygame
from Player import Player
from GameOver import GameOverScreen
import sys
pygame.init()

# Display window
width, height = 960, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Twisted Wizards")
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (width, height))
ground_y = 600 # Ground level Y coordinate

# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)


clock = pygame.time.Clock()
gameRunning = True

def draw_health(health, x, y):
    health_ratio = health / 100
    pygame.draw.rect(screen, black, (x - 1, y - 1, 352, 32))
    pygame.draw.rect(screen, red, (x, y, 350, 30))
    pygame.draw.rect(screen, green, (x, y, 350 * health_ratio, 30))

# Player instances and height
player_height = 190
player1 = None
player2 = None

# Game Over Screen Instance (initially None)
game_over_screen = None

# Loading in background music
pygame.mixer.init()
pygame.mixer.music.load("assets/Mountkid.mp3")
pygame.mixer.music.set_volume(0.2)

# Reset game
def reset_game():
    global player1, player2, game_over_screen # Global variables 
    
    # Recreates players
    player1 = Player(50, ground_y - player_height, is_bot=False) # Human-controlled
    player2 = Player(800, ground_y - player_height, is_bot=True) # Random-controlled bot

    # Resets death states for players
    player1.is_dead = False
    player1.death_animation_finished = False
    player2.is_dead = False
    player2.death_animation_finished = False

    game_over_screen = None # Clears game over screen
    pygame.mixer.music.play(-1) # Replays music

reset_game()


while gameRunning:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        
        # R resets game only if game over
        if game_over_screen is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game() # Calls reset function 


    # Drawing health, background
    screen.blit(background, (0, 0))
    draw_health(player1.health, 20, 20)
    draw_health(player2.health, 580, 20)

    # If game is active
    if game_over_screen is None:
        player1.move(width, ground_y, screen, player2) # Movement for players
        player2.move(width, ground_y, screen, player1)

        # Check for game over conditions
        if player1.health <= 0:
            result_text = "DEFEAT!" # User lost
            game_over_screen = GameOverScreen(width, height, result_text)
            pygame.mixer.music.stop() # Stops music
        elif player2.health <= 0:
            result_text = "VICTORY!" # User won
            game_over_screen = GameOverScreen(width, height, result_text)
            pygame.mixer.music.stop()

    # Draw players
    player1.draw(screen)
    player2.draw(screen)

    # Draws game over screen if condition met
    if game_over_screen is not None:
        game_over_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
