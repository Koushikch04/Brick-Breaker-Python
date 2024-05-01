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
        # print(self.horizontal_vel,self.vertical_vel)
        # if self.horizontal_vel == 6.50208949395206 and self.vertical_vel == -7.597554357333564:
        #     self.x += self.VEL
        #     self.y += self.VEL
        # else:
        self.x += self.horizontal_vel
        self.y += self.vertical_vel
        # print("Move", self.x, self.y)

    def updateVel(self, horizontal_vel, vertical_vel):
        self.horizontal_vel = horizontal_vel
        self.vertical_vel = vertical_vel

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.radius, 0)
        # position is referenced based on the position of the centre.
