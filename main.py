import math
import pygame
import sys

print(sys.path)
sys.path.append("Game Objects")
print(sys.path)  # Verify that the directory is added correctly
from ball import Ball
from paddle import Paddle
from brick import generate_bricks
from game_display import *

width, height = 800, 700
Display_Space = 50
framesPerSecond = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
Score = 0

pygame.init()
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("BRICK BREAKER")
FONT = pygame.font.SysFont("comicsans", 40)


# def ball_paddle_collision(ball, paddle):
#     # print("hello")
#     if not (paddle.x + paddle.width >= ball.x >= paddle.x ):
#         return
#     if not (ball.y + ball.radius >= paddle.y-2):
#         return
#     # print("world")
#     paddle_center = paddle.x + paddle.width / 2
#     distance_to_center = ball.x - paddle_center
#
#     percent_width = distance_to_center / paddle.width
#     angle = percent_width * 90
#     angle_radians = math.radians(angle)
#
#     x_vel = math.sin(angle_radians) * ball.VEL
#     y_vel = math.cos(angle_radians) * ball.VEL * -1
#
#     ball.updateVel(x_vel, y_vel)

def ball_paddle_collision(ball, paddle):
    if (paddle.x <= ball.x <= paddle.x + paddle.width) and (ball.y + ball.radius >= paddle.y):
        paddle_center = paddle.x + paddle.width / 2
        distance_to_center = ball.x - paddle_center
        percent_width = distance_to_center / paddle.width
        angle = percent_width * (math.pi / 2)  # Adjusted for smoother reflection
        x_vel = ball.VEL * math.sin(angle)
        y_vel = -ball.VEL * math.cos(angle)
        ball.updateVel(x_vel, y_vel)

# Ball collision with screen
def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= width:
        ball.updateVel(ball.horizontal_vel * -1, ball.vertical_vel)
    if ball.y + BALL_RADIUS + PADDLE_HEIGHT >= height or ball.y - BALL_RADIUS <= Display_Space:
        ball.updateVel(ball.horizontal_vel, ball.vertical_vel * -1)


def main():
    global Score
    clock = pygame.time.Clock()
    paddle_x = width / 2 - PADDLE_WIDTH / 2
    paddle_y = height - PADDLE_HEIGHT - 5
    paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, "black")
    ball = Ball(width / 2, paddle_y - BALL_RADIUS, BALL_RADIUS, "black")
    bricks = generate_bricks(width, Display_Space, 4, 10)
    lives = 3
    run = True
    paused = False

    pause_button = pygame.Rect(width // 2, 10, 80, 40)
    def reset():
        paddle.x = paddle_x
        paddle.y = paddle_y
        ball.x = width / 2
        ball.y = paddle_y - BALL_RADIUS

    while run:
        # clock.tick(framesPerSecond)  #to limit number of frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        pygame.draw.rect(screen, (255, 255, 255), pause_button)

        if not paused:
            keys = pygame.key.get_pressed()
            # if keys[pygame.K_SPACE]
            if keys[pygame.K_LEFT] and paddle.x + paddle.VEL >= 0:
                paddle.move(-1)
            if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL <= width:
                paddle.move(1)
            ball.move()
            ball_collision(ball)
            ball_paddle_collision(ball, paddle)
            for brick in bricks:
                # global Score
                Score = brick.collide(ball, Score)
                if brick.health <= 0:
                    bricks.remove(brick)

            if ball.y + ball.radius >= height - PADDLE_HEIGHT:
                lives -= 1
                pygame.time.delay(1000)
                ball.x = paddle.x + paddle.width / 2
                ball.y = paddle.y - BALL_RADIUS
                ball.updateVel(ball.VEL
                               , ball.VEL * -1)
                reset()

            if lives <= 0:
                bricks = generate_bricks(5, 10)
                lives = 3
                # print("condition 2")
                display_text(screen, "You Lost!", width, height, 3000)
                reset()

            if len(bricks) == 0:
                bricks = generate_bricks(5, 10)
                lives = 3
                display_text(screen,"You Won!", width, height, 3000)
                reset()

            # for i in bricks:
            #     print(i.health)
            # global Score
            draw(screen, paddle, ball, bricks, lives, width, height, Score)
        else:
            display_text(screen, "Paused", width, height, 0)
        pygame.display.flip()
        clock.tick(framesPerSecond)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
