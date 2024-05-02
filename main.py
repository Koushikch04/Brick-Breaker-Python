import math
import os

import pygame
import sys

sys.path.append("Game Objects")
from ball import Ball
from paddle import Paddle
from brick import Brick, generate_bricks
from game_display import *
from button import Button
from brick import levels_count

width, height = 800, 700
Display_Space = 50
framesPerSecond = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
Score = 0
gameState = "Start"
level_index = 0
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
font20 = pygame.font.SysFont('Constantia', 20)
font60 = pygame.font.SysFont('Constantia', 60)
username = ""
scores = {}

red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("BRICK BREAKER")
FONT = pygame.font.SysFont("comicsans", 40)


def updateScores(scores):
    file_name = "highest_scores.txt"
    try:
        updated_scores = {}
        # Load existing scores
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    username, score = line.strip().split(":")
                    score = int(score)
                    # Update score if the username already exists and the new score is higher
                    if username in scores and scores[username] > score:
                        updated_scores[username] = scores[username]
                    else:
                        updated_scores[username] = score
        # Add new scores
        for username, score in scores.items():
            if username not in updated_scores:
                updated_scores[username] = score

        # Write updated scores to the file
        with open(file_name, "w") as file:
            for username, score in updated_scores.items():
                file.write(f"{username}:{score}\n")
    except Exception as e:
        print("Error saving high scores:", e)


def load_high_scores():
    scores = {}
    file_name = "highest_scores.txt"
    # Check if the file exists
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as file:
                for line in file:
                    username, score = line.strip().split(":")
                    scores[username] = int(score)
            # Sort scores by value in descending order
            sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            # Get top ten scores
            top_ten_scores = dict(list(sorted_scores.items())[:10])
            return top_ten_scores
        except Exception as e:
            print("Error loading high scores:", e)
    return scores


def save_high_scores(scores):
    file_name = "highest_scores.txt"
    try:
        updated_scores = {}
        # Load existing scores
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                for line in file:
                    username, score = line.strip().split(":")
                    score = int(score)
                    # Update score if the username already exists and the new score is higher
                    if username in scores and scores[username] > score:
                        updated_scores[username] = scores[username]
                    else:
                        updated_scores[username] = score
        # Add new scores
        for username, score in scores.items():
            if username not in updated_scores:
                updated_scores[username] = score

        # Write updated scores to the file
        with open(file_name, "w") as file:
            for username, score in updated_scores.items():
                file.write(f"{username}:{score}\n")
    except Exception as e:
        print("Error saving high scores:", e)


def display_leaderboard():
    run = True
    while run:
        screen.fill(black)
        draw_text("Leaderboard", font40, white, int(width / 2 - 100), 50)
        draw_text("Username    Score", font30, white, 50, 150)
        y = 200
        scores = load_high_scores()
        for username, score in scores.items():
            draw_text(f"{username:<12}  {score}", font30, white, 50, y)
            y += 50

        pygame.draw.rect(screen, white, (50, height - 100, 100, 50))
        draw_text("Back", font30, black, 65, height - 90)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 50 <= mouse_x <= 150 and height - 100 <= mouse_y <= height - 50:
                    run = False  # Back button clicked

    return


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def ball_paddle_collision(ball, paddle):
    print("ball paddle collision")
    if (paddle.x - 10 <= ball.x <= paddle.x + paddle.width) and (ball.y + ball.radius + 5 >= paddle.y):
        paddle_center = paddle.x + paddle.width / 2
        distance_to_center = ball.x - paddle_center
        # percent_width = distance_to_center / (paddle.width / 2)
        # angle = percent_width * (math.pi / 4)
        # x_vel = ball.VEL * math.sin(angle)
        # y_vel = -abs(ball.VEL) * math.cos(angle)
        # if x_vel != 0 and y_vel != 0:
        #     ball.updateVel(x_vel, y_vel)
        percent_width = distance_to_center / paddle.width
        angle = percent_width * 45
        angle_radians = math.radians(angle)
        print(angle_radians)

        x_vel = math.sin(angle_radians) * ball.VEL
        y_vel = math.cos(angle_radians) * ball.VEL * -1
        print(x_vel, y_vel)

        ball.updateVel(x_vel, y_vel)


def ball_collision(ball):
    if ball.x - BALL_RADIUS <= 0 or ball.x + BALL_RADIUS >= width:
        ball.updateVel(ball.horizontal_vel * -1, ball.vertical_vel)
    if ball.y + BALL_RADIUS >= height:
        ball.updateVel(ball.horizontal_vel, ball.vertical_vel * -1)
    elif ball.y - BALL_RADIUS <= Display_Space:
        ball.updateVel(ball.horizontal_vel, abs(ball.vertical_vel))


button_width = 120
button_height = 40
button_inactive_color = (200, 200, 200)
button_active_color = (150, 150, 150)
text_color = (0, 0, 0)


def start_game():
    global gameState
    gameState = "playing"
    print("Start button clicked!")
    start_button.action = None


def play_again():
    global gameState, level_index, Score
    gameState = "playing"  # Set the game state to playing
    level_index = 0
    Score = 0
    print("Play Again button clicked!")
    play_again_button.visible = False
    quit_button.visible = False


def quit_game():
    print("Quit button clicked!")
    pygame.quit()
    quit()


start_button = Button("Start", width // 2 - 60, height // 2 - 20, 120, 40, (200, 200, 200), (150, 150, 150),
                      (0, 0, 0), start_game)

play_again_button = Button("Play Again", width // 2 - 100, height // 2 - 20, 200, 40, (200, 200, 200), (150, 150, 150),
                           (0, 0, 0), play_again)

quit_button = Button("Quit", width // 2 - 60, height // 2 + 40, 120, 40, (200, 200, 200), (150, 150, 150),
                     (0, 0, 0), quit_game)

leaderboard_button = Button("Leaderboard", width // 2 - 100, height // 2 + 250, 200, 50, (200, 200, 200),
                            (150, 150, 150),
                            (0, 0, 0), )

username_entered = False
while not username_entered:
    screen.fill((0, 0, 0))  # Clear the screen
    draw_text("Enter Your Username:", font30, white, 150, 300)

    # Render the username on the screen
    username_rendered = font30.render(username, True, white)
    screen.blit(username_rendered, (150, 350))

    pygame.display.update()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                username_entered = True
            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            else:
                username += event.unicode


def main():
    global Score, gameState, level_index
    clock = pygame.time.Clock()
    paddle_x = width / 2 - PADDLE_WIDTH / 2
    paddle_y = height - PADDLE_HEIGHT - 5
    # paddle_x = 0
    # paddle_y = height - PADDLE_HEIGHT - 5
    paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, "black")
    ball = Ball(width / 2, paddle_y - BALL_RADIUS, BALL_RADIUS, "black")

    # bricks = levels[level_index]["bricks"]
    bricks = generate_bricks(width, Display_Space, 2, 10, level_index)
    lives = 3
    run = True
    paused = False
    win_timer = 0
    win_display_time = 1000
    play_again_clicked = False

    def reset(Condition):
        global level_index, Score, gameState
        nonlocal bricks, lives
        if Condition == "Progress":
            level_index += 1
            if level_index < levels_count:
                bricks = generate_bricks(width, Display_Space, 2, 10, level_index)
                ball.x = paddle.x + paddle.width / 2
                ball.y = paddle.y - BALL_RADIUS
            else:
                print("Else condition applied")
                gameState = "Won"  # Set the game state to "Won" only when all levels are completed
        elif Condition == "Chance":
            paddle.x = paddle_x
            paddle.y = paddle_y
            ball.x = width / 2
            ball.y = paddle_y - BALL_RADIUS
        elif Condition == "Won":
            level_index = 0
            bricks = generate_bricks(width, Display_Space, 2, 10, level_index)
            Score = 0
            lives = 3
            paddle.x = paddle_x
            paddle.y = paddle_y
            ball.x = width / 2
            ball.y = paddle_y - BALL_RADIUS
            print(gameState)
        elif Condition == "Lost":
            level_index = 0
            bricks = generate_bricks(width, Display_Space, 2, 10, level_index)
            Score = 0
        # gameState = "playing"

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if gameState == "playing":
                        gameState = "paused"
                    else:
                        gameState = "playing"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameState == "Won":
                    mouse_pos = pygame.mouse.get_pos()
                    if (play_again_button.x <= mouse_pos[0] <= play_again_button.x + play_again_button.width and
                            play_again_button.y <= mouse_pos[1] <= play_again_button.y + play_again_button.height):
                        # reset("Start")
                        play_again()
                        reset("Won")

                    elif (quit_button.x <= mouse_pos[0] <= quit_button.x + quit_button.width and
                          quit_button.y <= mouse_pos[1] <= quit_button.y + quit_button.height):
                        quit_button.action()
                    elif (leaderboard_button.x <= mouse_pos[0] <= leaderboard_button.x + leaderboard_button.width and
                          leaderboard_button.y <= mouse_pos[1] <= leaderboard_button.y + leaderboard_button.height):
                        print("Leaderboard Displayed")
                        display_leaderboard()
        screen.fill((255, 255, 255))  # Clear the screen
        # print(gameState)
        if gameState == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.x + paddle.VEL - 20 > 0:
                paddle.move(-1)
            if keys[pygame.K_RIGHT] and paddle.x + paddle.width + paddle.VEL + 20 <= width:
                paddle.move(1)
            ball.move()
            ball_collision(ball)
            ball_paddle_collision(ball, paddle)
            for brick in bricks:
                Score = brick.collide(ball, Score)
                if brick.health <= 0:
                    bricks.remove(brick)

            if ball.y + ball.radius >= height - PADDLE_HEIGHT:
                lives -= 1
                pygame.time.delay(1000)
                ball.x = paddle.x + paddle.width / 2
                ball.y = paddle.y - BALL_RADIUS
                ball.updateVel(ball.VEL, ball.VEL * -1)
                reset("Chance")

            if lives <= 0:
                # bricks = generate_bricks(width, Display_Space, 5, 10)
                lives = 3
                display_text(screen, "You Lost!", width, height, 3000)
                reset("Lost")
                gameState = "Won"
                print('reset is being called here')
                play_again_button.visible = True
                quit_button.visible = True

            if len(bricks) == 0:
                # bricks = generate_bricks(width, Display_Space, 5, 10)
                if level_index == levels_count - 1:
                    display_text(screen, "You Won!", width, height, 1000)
                    print("GameSate set here 1")
                    gameState = "Won"
                    print('reset is being called here')
                    play_again_button.visible = True
                    quit_button.visible = True
                else:
                    display_text(screen, f"Level, {level_index + 1}!", width, height, 1000)
                    reset("Progress")

                # print("You won")

            draw(screen, paddle, ball, bricks, lives, width, height, Score)
        elif gameState == "paused":
            display_text(screen, "Paused", width, height, 0)
        elif gameState == "Won":
            win_timer += clock.get_time()
            if win_timer < win_display_time:
                print("Hello", win_timer)
                display_text(screen, "You Won!", width, height, 0)
            else:
                # print("world")
                # global Score
                scores[username] = Score
                save_high_scores(scores)
                play_again_button.draw(screen)
                quit_button.draw(screen)
                leaderboard_button.draw(screen)
                # if play_again_clicked:
                #     print("condition")
                #     play_again()
                #     play_again_clicked = False
                # gameState = "playing"
        else:  # gameState == "Start"
            start_button.draw(screen)

        pygame.display.flip()
        clock.tick(framesPerSecond)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
