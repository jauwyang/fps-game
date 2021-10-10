from config import SCENE_HEIGHT, SCENE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WIDTH, MAP_HEIGHT, GREEN, GREY, CROSSHAIR_LENGTH, CROSSHAIR_WIDTH, CROSSHAIR_COLOUR, ENEMY_NUM
import pygame
import math
from math_tools import Vector2D
from pathfinder_test import A_star

# ==== GLOBAL VARIABLES ====
CLOCK = pygame.time.Clock()
FPS = 60


map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



def draw_window(window, pathfinder_map, path, checked_path):
    window.fill(GREY)
    pathfinder_map.draw_map(window)
    pathfinder_map.draw_path(window, path, checked_path)


def init():
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    pygame.key.set_repeat(1, 100)


    pathfinder_map = A_star(map)  # Create grid used for pathfinding algorithm
    start = Vector2D(7,7)
    end = Vector2D(65,65)
    # path = pathfinder_map.search(start, end)
    # checked_path = pathfinder_map.closed_set

    run = True
    while run:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        path = pathfinder_map.search(start, end)
        checked_path = pathfinder_map.closed_set
        draw_window(window, pathfinder_map, path, checked_path)
        
        pygame.display.update()
        

if __name__ == "__main__":
    init()