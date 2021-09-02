from config import SCENE_HEIGHT, SCENE_WIDTH, MAP_WIDTH, FOV
from math_tools import Vector2D
from raycast import Ray
import math
import pygame


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

    def shoot(self, window):
        # Animate
        blast = pygame.image.load('images/blast.png')
        window.blit(blast, (MAP_WIDTH + SCENE_WIDTH - 700, SCENE_HEIGHT - 600))