import math
import pygame


class Paddle:
    VEL = 10

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # (x, y) represents the top-left corner of the paddle rectangle, and the rectangle

    def move(self, direction=1):
        self.x = self.x + self.VEL * direction
