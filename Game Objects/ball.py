import math
import pygame

class Ball:
    VEL = 10

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.color = color
        self.horizontal_vel = self.VEL
        self.vertical_vel = -self.VEL
        self.radius = radius

    def move(self):
        self.x += self.horizontal_vel
        self.y += self.vertical_vel

    def updateVel(self, horizontal_vel, vertical_vel):
        self.horizontal_vel = horizontal_vel
        self.vertical_vel = vertical_vel

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius, 0)
        # position is referenced based on the position of the centre.

