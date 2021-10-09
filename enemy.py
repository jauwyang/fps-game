from math_tools import Vector2D, distance
import pygame
from config import SCENE_HEIGHT, SCENE_WIDTH, MAP_WIDTH, FOV, RED, LIMITED_VISION
import math

class Enemy:
    def __init__(self, x ,y):
        self.pos = Vector2D(x, y)
        self.distance_from_player = 0

    def get_distance_from_player(self, player):
        dist = distance(self.pos.x, self.pos.y, player.pos.x, player.pos.y)
        self.distance_from_player = dist
        return dist

    def get_angle_from_player(self, player):
        x_diff = self.pos.x - player.pos.x
        y_diff = self.pos.y - player.pos.y
        angle = math.atan2(y_diff, x_diff)
        angle_from_player = player.heading - angle
        if angle_from_player > 2 * math.pi:
            angle_from_player -= 2 * math.pi
        elif angle_from_player < 0:
            angle_from_player += 2 * math.pi
        self.angle_from_player = angle_from_player
        return self.angle_from_player

    def is_player_in_view(self, player):
        self.get_distance_from_player(player)
        angle_slice = math.ceil(math.degrees(self.get_angle_from_player(player)))
        if (angle_slice <= FOV / 2):
            index_of_pointing_ray = int(FOV / 2 - angle_slice)
        else:
            index_of_pointing_ray = int(360 - angle_slice + FOV / 2)
        
        return ((angle_slice > 360 - FOV / 2 or angle_slice < FOV / 2) and 
            (index_of_pointing_ray >= 0 or index_of_pointing_ray < len(player.rays)) and
            (player.rays[index_of_pointing_ray].length >= self.get_distance_from_player(player)))

    def draw_on_scene(self, window, player):
        if self.is_player_in_view(player):
            angle_slice = math.ceil(math.degrees(self.get_angle_from_player(player)))
            screen_ray = SCENE_WIDTH / FOV
            if angle_slice < FOV / 2:
                angle_slice = FOV / 2 - angle_slice
            elif angle_slice > 360 - FOV / 2:
                angle_slice = 360 - angle_slice + FOV / 2
            ray_slice_height = (SCENE_HEIGHT * 30) / self.distance_from_player
            ray_slice_width = SCENE_WIDTH * 5 / self.distance_from_player
            if ray_slice_height > SCENE_HEIGHT:
                ray_slice_height = SCENE_HEIGHT
            pygame.draw.rect(window, RED, (MAP_WIDTH + angle_slice * screen_ray, (SCENE_HEIGHT - ray_slice_height) / 2, ray_slice_width, ray_slice_height))
            # enemy = pygame
            # window.blit()

    def draw_on_map(self, window, player):
        if LIMITED_VISION:
            if self.is_player_in_view(player):
                pygame.draw.circle(window, RED, (self.pos.x, self.pos.y), 5)
        else:
            pygame.draw.circle(window, RED, (self.pos.x, self.pos.y), 5)