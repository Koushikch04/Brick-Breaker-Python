import pygame

pygame.init()
FONT = pygame.font.SysFont("comicsans", 40)
print(FONT)


def draw(screen, paddle, ball, bricks, lives, width, height, Score):
    screen.fill("white")
    paddle.draw(screen)
    ball.draw(screen)
    for brick in bricks:
        brick.draw(screen)
    lives_display = FONT.render(f"Lives: {lives}", 1, "black")
    score_display = FONT.render(f"Score: {Score}", 1, "black")
    screen.blit(lives_display, (0, 0))
    screen.blit(score_display, (width - score_display.get_width(), 0))
    pygame.display.update()

def display_text(screen, text, width, height, time_delay):
    text_render = FONT.render(text, 1, "red")
    screen.blit(text_render, (width / 2 - text_render.get_width() /
                                  2, height / 2 - text_render.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(time_delay)
