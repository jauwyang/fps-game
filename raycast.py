from math_tools import Vector2D, distance
import math
import pygame
from config import PLAYABLE_TO_MAP_SCREEN_SCALE, FOV, RED, WHITE, BLUE


class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.length = 0
        self.dir = Vector2D(math.cos(angle), math.sin(angle))  # direction is relative to the origin
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle < 0:
            self.angle += 2 * math.pi

    def draw(self, window):
        pygame.draw.line(window, WHITE, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE), (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE + self.dir.x * 100, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE + self.dir.y * 100))

    def set_angle(self, angle):
        self.dir = Vector2D(math.cos(angle), math.sin(angle))
        self.angle = angle
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle < 0:
            self.angle += 2 * math.pi

    def cast(self, window, map, heading):
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
            elif map_pos_x < map.m_width and map.customized_map[map_pos_y][map_pos_x] == 1:
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
            elif map_pos_x < map.m_width and map.customized_map[map_pos_y][map_pos_x] == 1:
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

        self.length = distance(self.pos.x, self.pos.y, shortest_ray_x, shortest_ray_y)

        self.endpoint = Vector2D(shortest_ray_x, shortest_ray_y)
        if self.angle == heading:
            colour = RED
        else:
            colour = BLUE
        pygame.draw.line(window, colour, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE), (shortest_ray_x * PLAYABLE_TO_MAP_SCREEN_SCALE, shortest_ray_y * PLAYABLE_TO_MAP_SCREEN_SCALE))

    

    def get_points_in_line(self, points, radius):
        # Narrow Search
        near = []
        ray_delta_y = self.pos.y - self.endpoint.y
        ray_delta_x = self.pos.x - self.endpoint.x
        for point in points:

            # If aligned on x-axis
            if ray_delta_y == 0:
                if abs(point.pos.y - self.pos.y) <= radius:
                    near.append(point)
            # If aligned on y-axis
            elif ray_delta_x == 0:
                if abs(point.pos.x - self.pos.x) <= radius:
                    near.append(point)
            else:
                slope = (self.pos.y - self.endpoint.y) / (self.pos.x - self.endpoint.x)
                inverse_slope = -1 / slope

                x_poi = ((point.pos.y - point.pos.x * inverse_slope) - (self.pos.y - self.pos.x * slope)) / (slope - inverse_slope)
                y_poi = (x_poi - self.pos.x) * slope + self.pos.y
                dist = distance(point.pos.x, point.pos.y, x_poi, y_poi)

                if dist <= radius:
                    near.append(point)
                    point.distance_from_player = dist

        return near