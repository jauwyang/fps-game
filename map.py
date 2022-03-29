from config import MAP_WIDTH, MAP_HEIGHT, PLAYABLE_MAP_SIZE, PLAYABLE_TO_MAP_SCREEN_SCALE, WHITE, BLACK, GREY, MAP_DIVISION
import pygame
import math

from pygame_object import PygameImageLayer


class Map:
    def __init__(self, map):
        self.customized_map = map
        self.m_width = len(map[0])
        self.m_height = len(map)
        self.block_width = PLAYABLE_MAP_SIZE / self.m_width
        self.block_height = PLAYABLE_MAP_SIZE / self.m_height

    def draw_map(self, window, image_layers):
        map_background_params = (window, GREY, (0, 0, (self.m_height-2)*self.block_height/ MAP_DIVISION, (self.m_width - 2)*self.block_width / MAP_DIVISION))
        map_background = PygameImageLayer('rect', False, map_background_params, 1500)
        image_layers.append(map_background)

        row_pos = 0
        for row in self.customized_map:
            column_pos = 0
            for column in row:
                if column == 0:
                    colour = BLACK
                elif column == 1:
                    colour = WHITE

                map_block_params = (window, colour, (column_pos * self.block_width * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION, row_pos * self.block_height * PLAYABLE_TO_MAP_SCREEN_SCALE / MAP_DIVISION, (self.block_width * PLAYABLE_TO_MAP_SCREEN_SCALE - 1) / MAP_DIVISION, (self.block_height * PLAYABLE_TO_MAP_SCREEN_SCALE - 1) / MAP_DIVISION))
                map_block = PygameImageLayer('rect', False, map_block_params, 1501)  # 1500 can be the same since none of the blocks on the map will be overlapping
                image_layers.append(map_block)
 
                column_pos += 1
            row_pos += 1

    def wall_collision(self, player, delta_x, delta_y):
        new_x_pos = player.pos.x + delta_x
        new_y_pos = player.pos.y + delta_y
        new_x_pos_index = math.floor(new_x_pos / self.block_width)
        new_y_pos_index = math.floor(new_y_pos / self.block_height)
        x_pos_index = math.floor(player.pos.x / self.block_width)
        y_pos_index = math.floor(player.pos.y / self.block_height)

        if (new_x_pos < PLAYABLE_MAP_SIZE and new_x_pos > 0) and self.customized_map[y_pos_index][new_x_pos_index] == 0:
            player.pos.x = new_x_pos
        if (new_y_pos < PLAYABLE_MAP_SIZE and new_y_pos > 0) and self.customized_map[new_y_pos_index][x_pos_index] == 0:
            player.pos.y = new_y_pos