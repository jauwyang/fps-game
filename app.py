from imp import reload
from config import MAX_ENEMIES, SCENE_HEIGHT, SCENE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, GREEN, GREY, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH, CROSSHAIR_COLOUR, ENEMY_NUM, RED
from player import Player
from map import Map
from enemy import Enemy
import pygame
import math
from pygame_object import PygameImageLayer
from tools.math_tools import Vector2D, distance
from tools.merge_sort_layer_priority import merge_sort_layer_priority
from pathfinder import A_star
import random

# ==== GLOBAL VARIABLES ====
CLOCK = pygame.time.Clock()
FPS = 60

# ========= The TODO list ==========
# TODO: add point system (+100 per kill) where points tracked and shown beneath the map
# TODO: add sounds for when player shoots and hits enemy
# TODO: fix enemy sometimes clipping directly through wall
# TODO: add title screen and death screen
# TODO (maybe): make player have limited ammo with ammo drops around the map (to force the player to move around) - also make player get 1 bullet back per kill

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

# map = [
#     [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
#     [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#     [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0]
# ]

map = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def generate_enemies():
    enemies = []
    for enemy in range(ENEMY_NUM):
        enemies.append(Enemy(500, 300))
        enemies.append(Enemy(600, 800))
    return enemies


def draw_sky(window, image_layers):
    image_parameters = (window, (26, 164, 255), (MAP_WIDTH, 0, SCENE_WIDTH, SCENE_HEIGHT / 2))
    sky = PygameImageLayer('rect', False, image_parameters, -1)
    image_layers.append(sky)


def draw_ui(window, user, font, image_layers):
    # UI parameters have priority of 2001+
    # Blast has a priority of 2000
    # Draw crosshair
    crosshair_horizontal_params = (window, CROSSHAIR_COLOUR, (MAP_WIDTH + SCENE_WIDTH / 2 - CROSSHAIR_WIDTH / 2, SCENE_HEIGHT / 2 - CROSSHAIR_LENGTH / 2, CROSSHAIR_WIDTH, CROSSHAIR_LENGTH))
    crosshair_horizontal = PygameImageLayer('rect', False, crosshair_horizontal_params, 2001)
    image_layers.append(crosshair_horizontal)

    crosshair_vertical_params = (window, CROSSHAIR_COLOUR, (MAP_WIDTH + SCENE_WIDTH / 2 - CROSSHAIR_LENGTH / 2, SCENE_HEIGHT / 2 - CROSSHAIR_WIDTH / 2, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH))
    crosshair_vertical = PygameImageLayer('rect', False, crosshair_vertical_params, 2001)
    image_layers.append(crosshair_vertical)

    # Draw pistol
    pistol_image = pygame.image.load('images/pistol.png')
    pistol_params = (pistol_image, (MAP_WIDTH + SCENE_WIDTH - 300, SCENE_HEIGHT - 320))
    pistol = PygameImageLayer('blit', False, pistol_params, 2001)
    image_layers.append(pistol)

    # Animate Shot
    user.animate_blast(image_layers)

    # Draw Ammo
    if user.ammunition == 3:
        ammo_image = pygame.image.load('images/ammo_3.png')
    elif user.ammunition == 2:
        ammo_image = pygame.image.load('images/ammo_2.png')
    elif user.ammunition == 1:
        ammo_image = pygame.image.load('images/ammo_1.png')
    else:
        ammo_image = pygame.image.load('images/ammo_0.png')
        # no_ammo = font.render("NO AMMO", 1, RED)
        # window.blit(no_ammo, (MAP_WIDTH + SCENE_WIDTH / 2, SCENE_HEIGHT / 2))
    ammo_image = pygame.transform.scale(ammo_image, (100, 50))

    ammo_params = (ammo_image, (MAP_WIDTH + SCENE_WIDTH - 150, SCENE_HEIGHT - 120))
    ammo = PygameImageLayer('blit', False, ammo_params, 2002)
    image_layers.append(ammo)


def draw_window(window, game_map, user, enemies, font):

    window.fill(GREY)

    image_layers = []

    draw_sky(window, image_layers)
    
    user.draw(window, game_map, image_layers)

    user.draw_scene_walls(window, game_map, image_layers)
    # Values for the map go from 0-12 (0-1200), so map will start at 1500

    game_map.draw_map(window, image_layers)
    for enemy in enemies:
        enemy.draw_on_map(window, user, image_layers)
        enemy.draw_on_scene(window, user, image_layers)
    draw_ui(window, user, font, image_layers)
    
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

    pygame.display.update()


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


def update_entities(pathfinder_map, user, enemies):
    # Update position of enemies
    for enemy in enemies:
        enemy.pathfind(pathfinder_map, user)
    
    # Respawn enemies
    while len(enemies) < MAX_ENEMIES:
        found_vacant_spot = False
        while not found_vacant_spot:
            x_spawn_on_map_index = random.randint(0, len(map[0]) - 1)
            y_spawn_on_map_index = random.randint(0, len(map) - 1)
            x_spawn = x_spawn_on_map_index * 100 - 50
            y_spawn = y_spawn_on_map_index * 100 - 50
            if map[y_spawn_on_map_index][x_spawn_on_map_index] == 0 and distance(user.pos.x, user.pos.y, x_spawn, y_spawn) > 600:
                enemies.append(Enemy(x_spawn, y_spawn))
                found_vacant_spot = True


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
        update_entities(pathfinder_map, user, enemies)
        pygame.display.update()
        

if __name__ == "__main__":
    init()
