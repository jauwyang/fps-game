from config import SCENE_HEIGHT, SCENE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, RED, GREY, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH, CROSSHAIR_COLOUR
from player import Player
from map import Map
import pygame
import math
from math_tools import Vector2D

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

    # Draw pistol
    pistol = pygame.image.load('images/pistol.png')
    window.blit(pistol, (MAP_WIDTH + SCENE_WIDTH - 300, SCENE_HEIGHT - 320))


def draw_window(window, game_map, user):
    window.fill(GREY)
    draw_sky(window)
    game_map.draw_map(window)
    user.draw(window, game_map)
    user.draw_scene_walls(window, game_map)
    draw_ui(window)
    
    pygame.display.update()


def keyboard_input(window, map, player, animation_frames):
    keys = pygame.key.get_pressed()

    # Player movement
    forward = 0
    sideways = 0
    speed_multiplier = 1
    if keys[pygame.K_LSHIFT]:
        speed_multiplier *= 2
    if keys[pygame.K_w]:
        forward = 2 * speed_multiplier
    if keys[pygame.K_s]:
        forward = -2
    if keys[pygame.K_a]:
        sideways = 2
    if keys[pygame.K_d]:
        sideways = -2
    sideways_angle = player.heading - math.pi / 2
    if sideways_angle < 0:
        sideways_angle += 2 * math.pi

    x_change = forward * math.cos(player.heading)
    y_change = forward * math.sin(player.heading)
    x_change += sideways * math.cos(sideways_angle)
    y_change += sideways * math.sin(sideways_angle)
    map.wall_collision(player, x_change, y_change)

    # Player rotation
    if keys[pygame.K_LEFT]:
        player.rotate(-0.05)
    if keys[pygame.K_RIGHT]:
        player.rotate(0.05)

    # Player shoot
    if keys[pygame.K_SPACE]:
        animation_frames["gun_blast"] = 360
    if animation_frames["gun_blast"] > 0:
        player.shoot(window)
        animation_frames["gun_blast"] -= 1


def init():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.key.set_repeat(1, 100)

    user = Player(100, 100, RED)
    game_map = Map(map)
    
    animation_frames = {
    "gun_blast": 0
    }

    run = True
    while run:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(window, game_map, user)
        keyboard_input(window, game_map, user, animation_frames)
        

if __name__ == "__main__":
    init()