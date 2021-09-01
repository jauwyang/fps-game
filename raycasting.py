from math_tools import Vector2D, distance
import math
import pygame
from config import SCENE_HEIGHT, SCENE_WIDTH, MAP_WIDTH, FOV, WHITE, GREEN, BLUE

class Player:
    def __init__(self, x, y, colour):
        self.pos = Vector2D(x, y)
        self.rays = []
        self.heading = 0
        self.colour = colour
        for angle in range(round(-FOV / 2), round(FOV / 2)):
            self.rays.append(Ray(self.pos, math.radians(angle)))

    def rotate(self, angle):
        self.heading += angle
        while self.heading > 2 * math.pi:
            self.heading -= 2 * math.pi
        for ray in self.rays:
            ray.set_angle(ray.angle + angle)

    def update_position(self, delta_x, delta_y):
        self.pos.x += delta_x
        self.pos.y += delta_y

    def draw(self, window, map):
        pygame.draw.circle(window, self.colour, (self.pos.x, self.pos.y), 5)
        pygame.draw.line(window, self.colour, (self.pos.x, self.pos.y), (self.pos.x + 30 * math.cos(self.heading), self.pos.y + 30 * math.sin(self.heading)))
        for ray in self.rays:
            ray.cast(window, map)

    def draw_scene_walls(self, window, map):
        ray_x_pos = 0
        for ray in self.rays:
            # Fix fish-eye effect
            ray_angle_difference = self.heading - ray.angle
            if ray_angle_difference < 0:
                ray_angle_difference += 2 * math.pi
            elif ray_angle_difference > 2 * math.pi:
                ray_angle_difference -= 2 * math.pi
            ray.shortest_distance = ray.shortest_distance * math.cos(ray_angle_difference)
            if ray.shortest_distance == 0:
                ray.shortest_distance = 1
            # Determine wall slice dimensions
            ray_slice_height = (SCENE_HEIGHT * map.block_width) / ray.shortest_distance
            ray_slice_width = SCENE_WIDTH / FOV
            if ray_slice_height > SCENE_HEIGHT:
                ray_slice_height = SCENE_HEIGHT

            # Determine shade
            if ray.horizontal_wall:
                colour = (255, 255, 255)
            else:
                colour = (150, 150, 150)

            pygame.draw.rect(window, colour, (MAP_WIDTH + ray_x_pos * ray_slice_width, (SCENE_HEIGHT - ray_slice_height) / 2, ray_slice_width, ray_slice_height))
            ray_x_pos += 1


class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.dir = Vector2D(math.cos(angle), math.sin(angle))  # direction is relative to the origin
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle < 0:
            self.angle += 2 * math.pi

    def draw(self, window):
        pygame.draw.line(window, WHITE, (self.pos.x, self.pos.y), (self.pos.x + self.dir.x * 100, self.pos.y + self.dir.y * 100))

    def set_angle(self, angle):
        self.dir = Vector2D(math.cos(angle), math.sin(angle))
        self.angle = angle
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle < 0:
            self.angle += 2 * math.pi

    def cast(self, window, map):
        self.shortest_distance = math.inf

        # Rounded variables used for comparisons
        pi = round(math.pi, 10)
        ray_angle = round(self.angle, 10)

        # Horizontal Line
        horizontal_line_check = True
        if (ray_angle < pi and ray_angle > 0):  # Looking down
            horizontal_line_direction_offset = 0
            aTan = -1/math.tan(self.angle)
            ray_y = round(self.pos.y / map.block_height) * map.block_height
            if ray_y < self.pos.y:
                ray_y += map.block_height
            ray_x = (self.pos.y - ray_y) * aTan + self.pos.x
            offset_y = map.block_height
            offset_x = -offset_y * aTan
        
        elif (ray_angle > pi):  # Looking up
            horizontal_line_direction_offset = -1
            aTan = -1/math.tan(self.angle)
            ray_y = round(self.pos.y / map.block_height) * map.block_height
            if ray_y > self.pos.y:
                ray_y -= map.block_height
            ray_x = (self.pos.y - ray_y) * aTan + self.pos.x
            offset_y = -map.block_height
            offset_x = -offset_y * aTan

        else:  # Looking left or right
            ray_y = math.inf
            ray_x = math.inf
            horizontal_line_check = False

        while horizontal_line_check:
            map_pos_x = math.ceil(ray_x / map.block_width) - 1
            map_pos_y = math.ceil(ray_y / map.block_width) + horizontal_line_direction_offset
            if map_pos_x >= map.m_width or map_pos_y >= map.m_height or map_pos_x < 0 or map_pos_y < 0:
                horizontal_line_check = False
            elif map_pos_x < map.m_width and map.map[map_pos_y][map_pos_x] == 1:
                horizontal_line_check = False
            else:
                ray_x += offset_x
                ray_y += offset_y
        
        if not (ray_x == math.inf or ray_y == math.inf):
            horizontal_distance = distance(self.pos.x, self.pos.y, ray_x, ray_y)
            self.shortest_distance = horizontal_distance
            shortest_ray_x = ray_x
            shortest_ray_y = ray_y
            self.horizontal_wall = True

        # Vertical Line
        vertical_line_check = True
        if (ray_angle > pi / 2 and ray_angle < 3 / 2 * pi):  # Looking left
            vertical_line_direction_offset = -1
            nTan = -math.tan(self.angle)
            ray_x = round(self.pos.x / map.block_width) * map.block_width
            if ray_x > self.pos.x:
                ray_x -= map.block_width
            ray_y = (self.pos.x - ray_x) * nTan + self.pos.y
            offset_x = -map.block_width
            offset_y = -offset_x * nTan
        
        elif (ray_angle < pi / 2 or ray_angle > 3 / 2 * pi):  # Looking right
            vertical_line_direction_offset = 0
            nTan = -math.tan(self.angle)
            ray_x = round(self.pos.x / map.block_width) * map.block_width
            if ray_x < self.pos.x:
                ray_x += map.block_width
            ray_y = (self.pos.x - ray_x) * nTan + self.pos.y
            offset_x = map.block_width
            offset_y = -offset_x * nTan

        else:  # Looking up or down
            ray_x = self.pos.x
            ray_y = self.pos.y
            vertical_line_check = False

        while vertical_line_check:
            map_pos_x = math.ceil(ray_x / map.block_width) + vertical_line_direction_offset
            map_pos_y = math.ceil(ray_y / map.block_width) - 1
            if map_pos_x >= map.m_width or map_pos_y >= map.m_height or map_pos_x < 0 or map_pos_y < 0:
                vertical_line_check = False
            elif map_pos_x < map.m_width and map.map[map_pos_y][map_pos_x] == 1:
                vertical_line_check = False
            else:
                ray_x += offset_x
                ray_y += offset_y
        
        if not (ray_x == math.inf or ray_y == math.inf):
            vertical_distance = distance(self.pos.x, self.pos.y, ray_x, ray_y)
            if vertical_distance < self.shortest_distance:
                self.shortest_distance = vertical_distance
                shortest_ray_x = ray_x
                shortest_ray_y = ray_y
                self.horizontal_wall = False

        pygame.draw.line(window, BLUE, (self.pos.x, self.pos.y), (shortest_ray_x, shortest_ray_y))