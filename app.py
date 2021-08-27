from config import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, RED, GREY
from raycasting import Player
from map import draw_map
import pygame

# ==== GLOBAL VARIABLES ====
CLOCK = pygame.time.Clock()
FPS = 60


def draw_window(window, user):
    window.fill(GREY)
    draw_map(window)
    user.draw(window)
    
    pygame.display.update()


def keyboard_input(player):
    keys = pygame.key.get_pressed()
    current_x = player.pos.x
    current_y = player.pos.y
    delta_X = 0
    delta_Y = 0
    if keys[pygame.K_w]:
        delta_Y -= 5
    if keys[pygame.K_s]:
        delta_Y += 5
    if keys[pygame.K_a]:
        delta_X -= 5
    if keys[pygame.K_d]:
        delta_X += 5
    current_x += delta_X
    current_y += delta_Y
    if not (current_x > MAP_WIDTH or current_x < 0):
        player.pos.x = current_x
    if not (current_y > MAP_HEIGHT or current_y < 0):
        player.pos.y = current_y

    if keys[pygame.K_LEFT]:
        player.rotate(-0.05)
    if keys[pygame.K_RIGHT]:
        player.rotate(0.05)


def init():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    user = Player(100, 100, RED)

    run = True
    while run:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keyboard_input(user)

        draw_window(window, user)
        


if __name__ == "__main__":
    init()