from imp import reload
from config import SCENE_HEIGHT, SCENE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, GREEN, GREY, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH, CROSSHAIR_COLOUR, ENEMY_NUM, RED
from player import Player
from map import Map
from enemy import Enemy
import pygame
import math
from tools.math_tools import Vector2D
from tools.merge_sort_layer_priority import merge_sort_layer_priority
from pathfinder import A_star

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
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
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
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0]
]

def generate_enemies():
    enemies = []
    for enemy in range(ENEMY_NUM):
        enemies.append(Enemy(500, 300))
    return enemies


def draw_sky(window):
    pygame.draw.rect(window, (26, 164, 255), (MAP_WIDTH, 0, SCENE_WIDTH, SCENE_HEIGHT / 2))
    # pygame.draw.rect(window, (0, 255, 0), (MAP_WIDTH, SCENE_HEIGHT / 2, SCENE_WIDTH, SCENE_HEIGHT / 2))


def draw_ui(window, user, font):
    # Draw crosshair
    pygame.draw.rect(window, CROSSHAIR_COLOUR, (MAP_WIDTH + SCENE_WIDTH / 2 - CROSSHAIR_WIDTH / 2, SCENE_HEIGHT / 2 - CROSSHAIR_LENGTH / 2, CROSSHAIR_WIDTH, CROSSHAIR_LENGTH))
    pygame.draw.rect(window, CROSSHAIR_COLOUR, (MAP_WIDTH + SCENE_WIDTH / 2 - CROSSHAIR_LENGTH / 2, SCENE_HEIGHT / 2 - CROSSHAIR_WIDTH / 2, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH))

    # Draw pistol
    test = (window, RED, (0, 0), 20)
    pygame.draw.circle(*test)
    pistol = pygame.image.load('images/pistol.png')
    window.blit(pistol, (MAP_WIDTH + SCENE_WIDTH - 300, SCENE_HEIGHT - 320))

    # Draw Ammo
    if user.ammunition == 3:
        ammo = pygame.image.load('images/ammo_3.png')
    elif user.ammunition == 2:
        ammo = pygame.image.load('images/ammo_2.png')
    elif user.ammunition == 1:
        ammo = pygame.image.load('images/ammo_1.png')
    else:
        ammo = pygame.image.load('images/ammo_0.png')
        # no_ammo = font.render("NO AMMO", 1, RED)
        # window.blit(no_ammo, (MAP_WIDTH + SCENE_WIDTH / 2, SCENE_HEIGHT / 2))
    ammo = pygame.transform.scale(ammo, (100, 50))
    window.blit(ammo, (MAP_WIDTH + SCENE_WIDTH - 150, SCENE_HEIGHT - 120))


def draw_window(window, game_map, user, enemies, font):

    """
    COMMIT CHANGES BEFORE ACTUALLY IMPLEMENTING NEW IMAGE RENDERING METHOD <<<<<<<
    """
    window.fill(GREY)

    image_layers = []

    draw_sky(window)
    
    user.draw(window, game_map)

    user.draw_scene_walls(window, game_map)
    game_map.draw_map(window)
    for enemy in enemies:
        enemy.draw_on_map(window, user)
        enemy.draw_on_scene(window, user)
    draw_ui(window, user, font)
    
    merge_sort_layer_priority(image_layers)

    for layer in image_layers:
        if layer.type == 'rect':
            pygame.draw.rect(*layer.parameters)
        elif layer.type == 'circle':
            pygame.draw.circle(*layer.parameters)
        elif layer.type == 'line':
            pygame.draw.line(*layer.parameters)
        elif layer.type == 'blit':
            window.blit(*layer.parameters)

    # pygame.display.update()


def keyboard_input(window, map, player, enemies, animation_frames):
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
    look_multiplier = 1
    if keys[pygame.K_DOWN]:
        look_multiplier *= 1/5
    if keys[pygame.K_LEFT]:
        player.rotate(-0.05 * look_multiplier)
    if keys[pygame.K_RIGHT]:
        player.rotate(0.05 * look_multiplier)

    # Player shoot  
    # print(pygame.event.get())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot(window, enemies, 'down')
            animation_frames["gun_blast"] = 1
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            player.shoot(window, enemies, 'up')
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player.reload(window)

    if animation_frames["gun_blast"] > 0:
        animation_frames["gun_blast"] -= 1
    
    return True


def update_entities(pathfinder_map, user, enemies, window):
    # Update position of enemies
    for enemy in enemies:
        enemy.pathfind(pathfinder_map, user, window)


def init():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.key.set_repeat(1, 100)

    user = Player(100, 100, GREEN)  # Create player
    game_map = Map(map)  # Create Map
    pathfinder_map = A_star(game_map)  # Create grid used for pathfinding algorithm
    enemies = generate_enemies()
    font = pygame.font.SysFont("dejavusans", 24)
    animation_frames = {
    "gun_blast": 0
    }

    run = True
    while run:
        CLOCK.tick(FPS)
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        draw_window(window, game_map, user, enemies, font)
        run = keyboard_input(window, game_map, user, enemies, animation_frames)
        update_entities(pathfinder_map, user, enemies, window)
        pygame.display.update()
        

if __name__ == "__main__":
    init()
