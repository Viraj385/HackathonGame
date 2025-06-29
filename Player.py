import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 120)
        self.color = (255, 0, 0)
        self.speed = 25
        self.vel_y = 0

    def move(self, screen_width, ground_y):
        gravity = 2.5
        jump_force = -20
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        # Horizontal Movement
        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        # Jumping (only if on the ground)
        if keys[pygame.K_w] and self.rect.bottom >= ground_y:
            self.vel_y = jump_force

        # Apply gravity
        self.vel_y += gravity
        dy += self.vel_y

        # Horizontal Boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        # Ground Collision
        if self.rect.bottom + dy >= ground_y:
            self.rect.bottom = ground_y
            dy = 0
            self.vel_y = 0

        # Apply updates
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
