import pygame

class GameOverScreen:
    def __init__(self, screen_width, screen_height, text):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.text = text # Pre given Text
        self.font = pygame.font.Font(None, 74) # Game over font size
        self.text_color = (255, 255, 255) # Game over font colour (Black)

        # Reset button
        self.button_font = pygame.font.Font(None, 48)
        self.button_text = "Press R to Reset" # Instructs user to press R to reset
        self.button_color = (0, 150, 0) # Green colour to match setting
        self.current_button_color = self.button_color # Tracks colour
        self.button_rect = pygame.Rect(0, 0, 300, 70) # Size of button
        # Centering button
        self.button_rect.center = (self.screen_width // 2, self.screen_height // 2 + 100)


    def draw(self, surface):
        """Renders the game over message and restart button on the screen."""
        # Draws the text for win/lose
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        surface.blit(text_surface, text_rect)

        # Draws Background button
        pygame.draw.rect(surface, self.current_button_color, self.button_rect, border_radius=10)
        
        # Draws button text
        button_text_surface = self.button_font.render(self.button_text, True, self.text_color)
        button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
        surface.blit(button_text_surface, button_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Tried to do mouse hover effect but ran out of time
            if self.button_rect.collidepoint(event.pos):
                self.current_button_color = self.button_hover_color
            else:
                self.current_button_color = self.button_color

        return False
