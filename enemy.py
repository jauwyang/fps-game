from pygame_object import PygameImageLayer
from tools.math_tools import Vector2D, distance
import pygame
from config import MAP_DIVISION, SCENE_HEIGHT, SCENE_WIDTH, MAP_WIDTH, PLAYABLE_TO_MAP_SCREEN_SCALE, FOV, RED, LIMITED_VISION
import math

WALK_DELAY = 30

class Enemy:
    def __init__(self, x ,y):
        self.pos = Vector2D(x, y)
        self.distance_from_player = 0

        self.movement_delay = 15
        self.movement_counter = 15
        self.movement_direction = 0
        self.speed = 1.5

        self.key_frame = None
        self.key_frame_type = 1
        self.walk_timer = 0


        self.path = None

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

    def draw_on_scene(self, window, player, image_layers):
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
            
            # Determine key frame
            if self.walk_timer <= 0:
                self.walk_timer = WALK_DELAY
                if self.key_frame_type == 1:
                    self.key_frame = pygame.image.load('images/walk_1.png')
                else:
                    self.key_frame = pygame.image.load('images/walk_2.png')
                self.key_frame_type *= -1
            frame_width = self.key_frame.get_size()[0]
            frame_length = self.key_frame.get_size()[1]
            self.key_frame = pygame.transform.scale(self.key_frame, (int(ray_slice_width)*5, int(ray_slice_height*2)))

            enemy_parameters = (self.key_frame, (MAP_WIDTH + angle_slice * screen_ray - frame_width / 2, (SCENE_HEIGHT - ray_slice_height * 1.5) / 2))
            enemy = PygameImageLayer('blit', False, enemy_parameters, 1200 - round(self.get_distance_from_player(player)))
            image_layers.append(enemy)

            self.walk_timer -= 1


    def draw_on_map(self, window, player, image_layers):
        if LIMITED_VISION:
            if self.is_player_in_view(player):
                enemy_mapview_params = (window, RED, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION), 10 / MAP_DIVISION)
                enemy_mapview = PygameImageLayer('circle', False, enemy_mapview_params, 1505)
                image_layers.append(enemy_mapview)
        else:
            enemy_mapview_params = (window, RED, (self.pos.x * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION, self.pos.y * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION), 10 / MAP_DIVISION)
            enemy_mapview = PygameImageLayer('circle', False, enemy_mapview_params, 1505)
            image_layers.append(enemy_mapview)


    def pathfind(self, pathfinder_map, player):
        if math.floor(self.get_distance_from_player(player)) >= 15 and self.movement_counter == self.movement_delay:
            self.path = pathfinder_map.search(self.pos, player.pos)
            if len(self.path) >= 3:
                self.movement_direction = math.atan2(self.path[3].y - self.pos.y, self.path[3].x - self.pos.x)
            elif len(self.path) == 2:
                self.movement_direction = math.atan2(self.path[2].y - self.pos.y, self.path[2].x - self.pos.x)
            else:
                print("YOUR DED")
                
            if self.movement_direction < 0:
                self.movement_direction += 2*math.pi
            # print(math.degrees(self.movement_direction))
            
            # self.pos = Vector2D(self.path[1].x, self.path[1].y)
            self.movement_counter = 0
        
        self.movement_counter += 1
        self.pos.x += self.speed * math.cos(self.movement_direction)
        self.pos.y += self.speed * math.sin(self.movement_direction)
        # print(math.cos(self.movement_direction))
        # print(math.sin(self.movement_direction))
        
    def draw_path(self, window, image_layers):
        for step in self.path:
            pathfinder_trail_params = (window, RED, (step.x * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION, step.y * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION), 1)
            pathfinder_trail = PygameImageLayer('circle', False, pathfinder_trail_params, 1510)
            image_layers.append(pathfinder_trail)
