import pygame


class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, text_color, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text_color = text_color
        self.action = action
        self.visible = True  # Flag to indicate whether the button should be displayed

    def draw(self, screen):
        if self.visible:  # Only draw the button if it's visible
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # Check if mouse is over the button
            if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
                button_color = self.active_color
                # Check if button is clicked
                if click[0] == 1 and self.action:
                    self.action()
                    self.visible = False  # Hide the button after it's clicked
            else:
                button_color = self.inactive_color

            pygame.draw.rect(screen, button_color, (self.x, self.y, self.width, self.height))

            font = pygame.font.SysFont(None, 32)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surface, text_rect)
