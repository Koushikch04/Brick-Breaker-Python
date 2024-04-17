import math
import pygame

width, height = 800, 600
framesPerSecond = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

pygame.init()
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("BRICK BREAKER")


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


class Ball:
    VEL = 5

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.color = color
        self.horizontal_vel = 0
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

    def collide(self, ball):
        if not (self.x + self.width >= ball.x >= self.x):
            return False
        if not (ball.y - ball.radius <= self.y + self.height):
            return False

        # self.hit()
        self.health -= 1
        ball.updateVel(ball.horizontal_vel, ball.vertical_vel * -1)
        return True


def ball_paddle_collision(ball, paddle):
    # print("hello")
    if not (paddle.x + paddle.width >= ball.x >= paddle.x):
        return
    if not (ball.y + ball.radius >= paddle.y):
        return
    print("world")
    paddle_center = paddle.x + paddle.width / 2
    distance_to_center = ball.x - paddle_center

    percent_width = distance_to_center / paddle.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL * -1

    ball.updateVel(x_vel, y_vel)


def generate_bricks(rows, cols):
    gap = 2
    brick_width = width // cols - gap
    brick_height = 20

    bricks = []
    for row in range(rows):
        for col in range(cols):
            # display = random.randint(0,1)
            # if display:
            if not (col < row or col >= cols - row):
                brick = Brick(col * brick_width + gap * col, row * brick_height +
                              gap * row, brick_width, brick_height, 2, [(0, 255, 0), (255, 0, 0)])
                bricks.append(brick)

    return bricks


def draw(screen, paddle, ball, bricks, lives):
    screen.fill("white")
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    pygame.display.update()


def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= width:
        ball.updateVel(ball.horizontal_vel * -1, ball.vertical_vel)
    if ball.y + BALL_RADIUS + PADDLE_HEIGHT >= height or ball.y - BALL_RADIUS <= 0:
        ball.updateVel(ball.horizontal_vel, ball.vertical_vel * -1)


def main():
    clock = pygame.time.Clock()
    paddle_x = width / 2 - PADDLE_WIDTH / 2
    paddle_y = height - PADDLE_HEIGHT - 5
    paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, "black")
    ball = Ball(width / 2, paddle_y - BALL_RADIUS, BALL_RADIUS, "black")
    bricks = generate_bricks(10, 20)
    lives = 3
    run = True

    while run:
        clock.tick(framesPerSecond)  #to limit number of frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.x + paddle.VEL >= 0:
            paddle.move(-1)
        if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL <= width:
            paddle.move(1)
        ball.move()
        ball_collision(ball)
        ball_paddle_collision(ball, paddle)
        for brick in bricks:
            brick.collide(ball)
            if brick.health <= 0:
                bricks.remove(brick)

        if ball.y + ball.radius >= height - PADDLE_HEIGHT:
            lives -= 1
            pygame.time.delay(1000)
            ball.x = paddle.x + paddle.width/2
            ball.y = paddle.y - BALL_RADIUS
            ball.updateVel(0, ball.VEL * -1)

        if lives <= 0:
            bricks = generate_bricks(3, 10)
            lives = 3
            print("condition 2")
            # reset()
            # display_text("You Lost!")

        if len(bricks) == 0:
            bricks = generate_bricks(3, 10)
            lives = 3
            # reset()


        # for i in bricks:
        #     print(i.health)
        draw(screen, paddle, ball, bricks, lives)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
