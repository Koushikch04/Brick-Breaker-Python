from random import random

import pygame
import pygame.mixer
pygame.mixer.init()
brick_sound = pygame.mixer.Sound("./BackGroundMusic/brick-dropped-on-other-bricks-14722-[AudioTrimmer.com].mp3")

class Brick:
    def __init__(self, x, y, width, height, health, colors):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.colors = colors
        self.color = colors[0]

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    # def collide(self, ball):
    #     if not (self.x + self.width >= ball.x >= self.x):
    #         return False
    #     if not (ball.y - ball.radius <= self.y + self.height):
    #         # print("Y-direction hit missed")
    #         return False
    #     self.hit()
    #     # print("Hello")
    #     # self.health -= 1
    #     ball.updateVel(ball.horizontal_vel, ball.vertical_vel * -1)
    #     return True

    def collide(self, ball, Score):
        if (self.x - ball.radius <= ball.x <= self.x + self.width + ball.radius) and (
                self.y - ball.radius <= ball.y <= self.y + self.height + ball.radius):
            Score = self.hit(Score)
            ball.updateVel(ball.horizontal_vel, -ball.vertical_vel)
            return Score
        return Score

    def hit(self, Score):
        brick_sound.play()
        print(self.max_health,self.health)
        self.health -= 1
        Score += 100
        self.color = self.interpolate(*self.colors, self.health / self.max_health)
        return Score

    @staticmethod
    def interpolate(color_a, color_b, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))


levels = [[

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
],
    [
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    ],
    [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    ],
    # [
    #     [0, 0, 0, 1, 1, 0, 1, 1, 0, 0],
    #     [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    #     [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    # ],
    # [
    #     [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    #     [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    #     [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    # ]
]

levels_count = len(levels)


def generate_bricks(width, displaySpace, rows, cols, level_number):
    gap = 2
    brick_width = width // cols - gap
    brick_height = 20

    bricks = []
    level_data = levels[level_number]
    for row_index, row in enumerate(level_data):
        for col_index, brick_type in enumerate(row):
            if brick_type == 1:
                position_x = col_index * brick_width + gap * col_index
                position_y = displaySpace + row_index * brick_height + gap * row_index
                brick = Brick(position_x, position_y, brick_width, brick_height, 1, [(0, 0, 255), (255, 0, 0)])
                bricks.append(brick)

    return bricks
