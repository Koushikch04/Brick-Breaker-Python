import pygame


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
        self.health -= 1
        Score += 100
        print(Score)
        return Score


# def generate_bricks(width, displaySpace, rows, cols):
#     gap = 2
#     brick_width = width // cols - gap
#     brick_height = 20
#
#     bricks = []
#     for row in range(rows):
#         for col in range(cols):
#             # display = random.randint(0,1)
#             # if display:
#             if not (col < row or col >= cols - row):
#                 position_x = col * brick_width + gap * col
#                 position_y = row * brick_height + gap * row + displaySpace
#                 # position_y += Display_Space
#                 brick = Brick(position_x, position_y, brick_width, brick_height, 1, [(0, 255, 0), (255, 0, 0)])
#                 bricks.append(brick)
#
#     return bricks

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
                brick = Brick(position_x, position_y, brick_width, brick_height, 1, [(0, 255, 0), (255, 0, 0)])
                bricks.append(brick)

    return bricks
