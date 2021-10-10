from config import MAP_WIDTH, MAP_HEIGHT, PLAYABLE_MAP_SIZE, PLAYABLE_TO_MAP_SCREEN_SCALE, WHITE, BLACK
import pygame
import math

PLAYABLE_TO_MAP_SCREEN_SCALE = 5/6

class Map:
    def __init__(self, map):
        self.map = map
        self.m_width = len(map[0])
        self.m_height = len(map)
        self.block_width = PLAYABLE_MAP_SIZE / self.m_width
        self.block_height = PLAYABLE_MAP_SIZE / self.m_height

    def draw_map(self, window):
        row_pos = 0
        column_pos = 0

        for row in self.map:
            for column in row:
                if column == 0:
                    colour = BLACK
                elif column == 1:
                    colour = WHITE
                pygame.draw.rect(window, colour, (column_pos * self.block_width * PLAYABLE_TO_MAP_SCREEN_SCALE, row_pos * self.block_height * PLAYABLE_TO_MAP_SCREEN_SCALE, self.block_width * PLAYABLE_TO_MAP_SCREEN_SCALE - 1, self.block_height * PLAYABLE_TO_MAP_SCREEN_SCALE - 1))
                column_pos += 1
            column_pos = 0
            row_pos += 1

    def wall_collision(self, player, delta_x, delta_y):
        new_x_pos = player.pos.x + delta_x
        new_y_pos = player.pos.y + delta_y
        new_x_pos_index = math.floor(new_x_pos / self.block_width)
        new_y_pos_index = math.floor(new_y_pos / self.block_height)

        if self.map[new_y_pos_index][new_x_pos_index] == 0:
            if new_x_pos < PLAYABLE_MAP_SIZE and new_x_pos > 0:
                player.pos.x = new_x_pos
            if new_y_pos < PLAYABLE_MAP_SIZE and new_y_pos > 0:
                player.pos.y = new_y_pos