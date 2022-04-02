from tabnanny import check
from config import SCENE_HEIGHT, SCENE_WIDTH, MAP_WIDTH, PLAYABLE_TO_MAP_SCREEN_SCALE, FOV, ENEMY_HITBOX_WIDTH, PISTOL_COOLDOWN, MAP_DIVISION
from pygame_object import PygameImageLayer
from tools.math_tools import Vector2D, distance
from raycast import Ray
import math
import pygame
from textures import checkerboard

class Player:
    def __init__(self, x, y, colour):
        self.pos = Vector2D(x, y)
        self.rays = []
        self.heading = 0
        self.colour = colour
        self.can_shoot = True
        self.ammunition = 3
        self.main_ray_distance = 0
        self.animate_shot = False
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

    def draw(self, window, map, image_layers):
        # Draw Circle on map
        player_location_params = (window, self.colour, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION), 5)
        player_location = PygameImageLayer('circle', False, player_location_params, 1502)
        image_layers.append(player_location)
        
        # Draw player rays on map
        index = 0
        for ray in self.rays:
            ray.cast(window, map, self.heading, image_layers)
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

    def draw_scene_walls(self, window, map, image_layers):
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
            # if ray_slice_height > SCENE_HEIGHT:  # upda
            #     ray_slice_height = SCENE_HEIGHT

            # # Determine Shade
            # if ray.horizontal_wall:
            #     shade = 1
            # else:
            #     shade = 0.5

            # pixel_height = ray_slice_height / 32
            # x_pixel_iterator = (ray.endpoint.x / 3) % 32
            # for y_pixel_iterator in range(32):
            #     texture_colour_value = checkerboard[y_pixel_iterator * 32 + int(x_pixel_iterator)] * shade
            #     colour = (texture_colour_value * 255, texture_colour_value * 255, texture_colour_value * 255)
            #     wall_pixel_params = (window, colour, (ray_x_pos * ray_slice_width, (SCENE_HEIGHT - ray_slice_height) / 2 + y_pixel_iterator * pixel_height, ray_slice_width, pixel_height + 1))  # added +1 to pixel height to account for offset?
            #     wall_pixel = PygameImageLayer('rect', False, wall_pixel_params, (1200 - round(ray.shortest_distance)))
            #     image_layers.append(wall_pixel)


            # OLD ======
            # Determine shade
            if ray.horizontal_wall:
                colour = (255, 255, 255)
            else:
                colour = (150, 150, 150)

            wall_params = (window, colour, (ray_x_pos * ray_slice_width, (SCENE_HEIGHT - ray_slice_height) / 2, ray_slice_width, ray_slice_height))
            wall = PygameImageLayer('rect', False, wall_params, (1200 - round(ray.shortest_distance)))
            image_layers.append(wall)

            ray_x_pos += 1

    def shoot(self, window, enemies, keypress):
        # Animate shot
        if self.ammunition == 0 or (keypress == 'down' and not self.can_shoot):
            return
            
        # Prevent player from being able to hold down fire button
        if keypress == 'up':
            self.can_shoot = True
            return


        self.can_shoot = False
        self.ammunition -= 1
        self.animate_shot = True
        # window.blit(blast, (MAP_WIDTH + SCENE_WIDTH - 700, SCENE_HEIGHT - 600))

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

    def animate_blast(self, image_layers):
        if self.animate_shot == False:
            return

        blast_image = pygame.image.load('images/blast.png')
        blast_params = (blast_image, (MAP_WIDTH + SCENE_WIDTH - 700, SCENE_HEIGHT - 600))
        blast = PygameImageLayer('blit', False, blast_params, 2000)
        image_layers.append(blast)
        self.animate_shot = False