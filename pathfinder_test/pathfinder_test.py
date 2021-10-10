from config import BLUE, MAP_WIDTH, MAP_HEIGHT, BLACK, RED, WHITE
from math_tools import Vector2D, distance
import math
import pygame

Y_DIMENSION = 72
X_DIMENSION = 72

class A_star:
    def __init__(self, simplified_map):
        self.scale = math.floor(Y_DIMENSION / len(simplified_map))
        self.map = simplified_map
        self.a_star_grid = []
        for y in range(Y_DIMENSION):
            a_star_x = []
            for x in range(X_DIMENSION):
                a_star_x.append(Spot(x, y, simplified_map, self.scale))
            self.a_star_grid.append(a_star_x)

        for y in range(len(self.a_star_grid)):
            for x in range(len(a_star_x)):
                self.a_star_grid[y][x].add_neighours(self.a_star_grid)
        print("done")

    def draw_map(self, window):
        block_width = MAP_WIDTH / Y_DIMENSION
        block_height = MAP_HEIGHT / X_DIMENSION

        for row_pos in range(len(self.a_star_grid)):
            for column_pos in range(len(self.a_star_grid[0])):
                if self.map[math.floor(row_pos / self.scale)][math.floor(column_pos / self.scale)] == 0:
                    colour = BLACK
                elif self.map[math.floor(row_pos / self.scale)][math.floor(column_pos / self.scale)] == 1:
                    colour = WHITE
                pygame.draw.rect(window, colour, (column_pos * block_width, row_pos * block_height, block_width - 1, block_height - 1))
                column_pos += 1
            column_pos = 0
            row_pos += 1

    def search(self, start, end):
        self.closed_set = []
        open_set = []
        path = []
        start_pos = self.a_star_grid[start.y][start.x]
        end_pos = self.a_star_grid[end.y][end.x]

        open_set.append(start_pos)

        while (len(open_set) > 0):
            # Find index with shortest F - value (cost)
            lowest_cost_spot = open_set[0]
            for spot in open_set:
                if (spot.f_value < lowest_cost_spot.f_value):
                    lowest_cost_spot = spot
            current_spot = lowest_cost_spot

            # If the lowest cost index is the end, return final path
            if current_spot == end_pos:
                temp = current_spot
                path.append(temp)
                
                while (temp.previous is not None):
                    path.append(temp.previous)
                    temp = temp.previous
                return path

            open_set.remove(current_spot)
            self.closed_set.append(current_spot)

            for neighbour in current_spot.neighbours:
                # If next spot is valid
                if neighbour not in self.closed_set and not neighbour.wall:
                    temp_g_value = current_spot.g_value + self.heuristic(neighbour, current_spot)
                    # temp_g_value = current_spot.g_value + 1

                    # If better path
                    new_path = False
                    if neighbour in open_set:
                        if (temp_g_value < neighbour.g_value):
                            neighbour.g_value = temp_g_value
                            new_path = True
                    else:
                        neighbour.g_value = temp_g_value
                        open_set.append(neighbour)
                        new_path = True

                    # Update to better path
                    if new_path == True:
                        neighbour.h_value = self.heuristic(neighbour, end_pos)
                        neighbour.f_value = neighbour.g_value + neighbour.h_value
                        neighbour.previous = current_spot

        #no solution
        print("Cannot reach endpoint")
        return []

    def draw_path(self, window, path, checked_path):
        block_width = MAP_WIDTH / X_DIMENSION
        block_height = MAP_HEIGHT / Y_DIMENSION
        for spot in checked_path:
            pygame.draw.rect(window, RED, (spot.pos.x * block_width, spot.pos.y * block_height, block_width - 1, block_height - 1))

        for spot in path:
            pygame.draw.rect(window, BLUE, (spot.pos.x * block_width, spot.pos.y * block_height, block_width - 1, block_height - 1))


    def heuristic(self, spot_a, spot_b):
        return distance(spot_a.pos.x, spot_a.pos.y, spot_b.pos.x, spot_b.pos.y)
  

class Spot:
    def __init__(self, x, y, simplified_map, scale):
        self.pos = Vector2D(x, y)
        self.f_value = 0
        self.g_value = 0
        self.h_value = 0
        self.neighbours = []
        self.previous = None
        if simplified_map[math.floor(self.pos.y / scale)][math.floor(self.pos.x / scale)] == 1:
            self.wall = True
        else:
            self.wall = False

    def add_neighours(self, map):
        x_pos = self.pos.x
        y_pos = self.pos.y
        
        # Horzontal and Vertical neighbours
        if y_pos < len(map) - 1:
            self.neighbours.append(map[y_pos + 1][x_pos])
        if y_pos > 0:
            self.neighbours.append(map[y_pos - 1][x_pos])
        if x_pos < len(map[0]) - 1:
            self.neighbours.append(map[y_pos][x_pos + 1])
        if x_pos > 0:
            self.neighbours.append(map[y_pos][x_pos - 1])
        
        # Diagonal neighbours
        if (x_pos > 0 and y_pos > 0):
            self.neighbours.append(map[y_pos - 1][x_pos - 1])
        if (x_pos < len(map[0]) - 1 and y_pos > 0):
            self.neighbours.append(map[y_pos - 1][x_pos + 1])
        if (x_pos > 0 and y_pos < len(map) - 1):
            self.neighbours.append(map[y_pos + 1][x_pos - 1])
        if (x_pos < len(map[0]) - 1 and y_pos < len(map) - 1):
            self.neighbours.append(map[y_pos + 1][x_pos + 1])