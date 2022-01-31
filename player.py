from config import SCENE_HEIGHT, SCENE_WIDTH, MAP_WIDTH, PLAYABLE_TO_MAP_SCREEN_SCALE, FOV, ENEMY_HITBOX_WIDTH, PISTOL_COOLDOWN
from math_tools import Vector2D, distance
from raycast import Ray
import math
import pygame


class Player:
    def __init__(self, x, y, colour):
        self.pos = Vector2D(x, y)
        self.rays = []
        self.heading = 0
        self.colour = colour
        self.can_shoot = True
        self.ammunition = 3
        self.main_ray_distance = 0
        for angle in range(round(-FOV / 2), round(FOV / 2)):
            self.rays.append(Ray(self.pos, math.radians(angle)))
            if angle == self.heading:
                self.main_ray_index = len(self.rays) - 1

    def rotate(self, angle):
        self.heading += angle
        while self.heading > 2 * math.pi:
            self.heading -= 2 * math.pi
        while self.heading < 0:
            self.heading += 2 * math.pi
        for ray in self.rays:
            ray.set_angle(ray.angle + angle)

    def update_position(self, delta_x, delta_y):
        self.pos.x += delta_x
        self.pos.y += delta_y

    def draw(self, window, map):
        pygame.draw.circle(window, self.colour, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE), 5)
        pygame.draw.line(window, self.colour, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE), (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE + 30 * math.cos(self.heading), self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE + 30 * math.sin(self.heading)))
        index = 0
        for ray in self.rays:
            ray.cast(window, map, self.heading)
            if index == self.main_ray_index:
                self.main_ray_distance = ray.length
            index += 1

    def get_points_in_fov(self, points):
        points_seen = []
        for point in points:
            delta_angle = point.get_angle_from_player(self)
            if delta_angle >= math.pi:
                delta_angle = 2 * math.pi - delta_angle
            if math.degrees(abs(delta_angle)) < FOV / 2:
                points_seen.append(point)
        return points_seen

    def draw_scene_walls(self, window, map):
        ray_x_pos = 0
        for ray in self.rays:
            # Fix fish-eye effect
            ray_angle_difference = self.heading - ray.angle
            if ray_angle_difference < 0:
                ray_angle_difference += 2 * math.pi
            elif ray_angle_difference > 2 * math.pi:
                ray_angle_difference -= 2 * math.pi
            ray.shortest_distance *= math.cos(ray_angle_difference)
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

    def shoot(self, window, enemies, keypress):
        # Animate shot
        if self.ammunition == 0 or (keypress == 'down' and not self.can_shoot):
            return
        
        if keypress == 'up':
            print("up")
            self.can_shoot = True
            return

        print("down")
        self.can_shoot = False
        self.ammunition -= 1
        blast = pygame.image.load('images/blast.png')
        window.blit(blast, (MAP_WIDTH + SCENE_WIDTH - 700, SCENE_HEIGHT - 600))

        # Test collision
        line_of_sight = self.rays[self.main_ray_index]
        points_in_fov = self.get_points_in_fov(enemies)
        points_on_line = line_of_sight.get_points_in_line(points_in_fov, ENEMY_HITBOX_WIDTH)
        if len(points_on_line) > 0:
            for enemy in points_on_line:
                enemies.remove(enemy)
                print("Killed")
            # print(len(points_on_line))
            # print(type(points_on_line[0]))

    def reload(self, window):
        if self.ammunition == 3:
            return
        
        self.ammunition = 3
        self.can_shoot = True