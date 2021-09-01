from config import SCENE_HEIGHT, SCENE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, RED, GREY, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH, CROSSHAIR_COLOUR
from raycasting import Player
from map import Map
import pygame
import math

# ==== GLOBAL VARIABLES ====
CLOCK = pygame.time.Clock()
FPS = 60


# ===== MAP =====
# map = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]

map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def draw_sky(window):
    pygame.draw.rect(window, (26, 164, 255), (MAP_WIDTH, 0, SCENE_WIDTH, SCENE_HEIGHT / 2))
    # pygame.draw.rect(window, (0, 255, 0), (MAP_WIDTH, SCENE_HEIGHT / 2, SCENE_WIDTH, SCENE_HEIGHT / 2))

def draw_ui(window):
    # Draw crosshair
    pygame.draw.rect(window, CROSSHAIR_COLOUR, (MAP_WIDTH + SCENE_WIDTH / 2 - CROSSHAIR_WIDTH / 2, SCENE_HEIGHT / 2 - CROSSHAIR_LENGTH / 2, CROSSHAIR_WIDTH, CROSSHAIR_LENGTH))
    pygame.draw.rect(window, CROSSHAIR_COLOUR, (MAP_WIDTH + SCENE_WIDTH / 2 - CROSSHAIR_LENGTH / 2, SCENE_HEIGHT / 2 - CROSSHAIR_WIDTH / 2, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH))

def draw_window(window, game_map, user):
    window.fill(GREY)
    draw_sky(window)
    game_map.draw_map(window)
    user.draw(window, game_map)
    user.draw_scene_walls(window, game_map)
    draw_ui(window)
    
    pygame.display.update()


def keyboard_input(player, map):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        map.wall_collision(player, 0, -5)
    if keys[pygame.K_s]:
        map.wall_collision(player, 0, 5)
    if keys[pygame.K_a]:
        map.wall_collision(player, -5, 0)
    if keys[pygame.K_d]:
        map.wall_collision(player, 5, 0)

    if keys[pygame.K_LEFT]:
        player.rotate(-0.05)
    if keys[pygame.K_RIGHT]:
        player.rotate(0.05)


def init():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    user = Player(100, 100, RED)
    game_map = Map(map)

    run = True
    while run:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keyboard_input(user, game_map)
        draw_window(window, game_map, user)
        

if __name__ == "__main__":
    init()