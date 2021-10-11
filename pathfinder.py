from config import PLAYABLE_MAP_SIZE
from math_tools import Vector2D, distance
import math
from tools import printProgressBar

# MAP SCALES
'''
These scales are used to convert the coordinates of one map to another.
There are three maps:
- Custom Map
- Playable Map
- A Star Map
Multiplying the scales convert the coordinates according to the name.
Dividing the scales convert the coordinates opposite to their names.
'''
PLAYABLE_TO_A_STAR_SCALE = 1/15
A_STAR_TO_SIMPLIFIED_SCALE = 1/6
A_STAR_SIZE = PLAYABLE_MAP_SIZE * PLAYABLE_TO_A_STAR_SCALE
# PLAYABLE_TO_SIMPLIFIED_SCALE = (1 / PLAYABLE_TO_A_STAR_SCALE) * (1 / A_STAR_TO_SIMPLIFIED_SCALE)


class A_star:
    def __init__(self, simplified_map):
        self.a_star_grid = []

        # Generate map
        printProgressBar(0, int(A_STAR_SIZE * 2), prefix = 'Rendering Map:', suffix = 'Complete', length = 50)
        percent_complete = 1
        for y in range(int(A_STAR_SIZE)):
            a_star_x = []
            for x in range(int(A_STAR_SIZE)):
                a_star_x.append(Spot(x, y, simplified_map))
            percent_complete += 1
            printProgressBar(percent_complete, int(A_STAR_SIZE * 2), prefix = 'Rendering Map:', suffix = 'Complete', length = 50)
            self.a_star_grid.append(a_star_x)
        for y in range(len(self.a_star_grid)):
            for x in range(len(a_star_x)):
                self.a_star_grid[y][x].add_neighours(self.a_star_grid)
            printProgressBar(percent_complete, int(A_STAR_SIZE * 2), prefix = 'Rendering Map:', suffix = 'Complete', length = 50)
            percent_complete += 1
        print("Finished rendering map")

    def search(self, start, end):
        closed_set = []
        open_set = []
        path = []
        start_pos = self.a_star_grid[math.floor(start.y * PLAYABLE_TO_A_STAR_SCALE)][math.floor(start.x * PLAYABLE_TO_A_STAR_SCALE)]
        end_pos = self.a_star_grid[math.floor(end.y * PLAYABLE_TO_A_STAR_SCALE)][math.floor(end.x * PLAYABLE_TO_A_STAR_SCALE)]


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
                path.append(Vector2D(temp.pos.x / PLAYABLE_TO_A_STAR_SCALE, temp.pos.y / PLAYABLE_TO_A_STAR_SCALE))
                temp.reset_values()
                for node in closed_set:
                    node.reset_values()
                while (temp.previous is not None):
                    temp.previous.reset_values()
                    path.append(Vector2D(temp.previous.pos.x / PLAYABLE_TO_A_STAR_SCALE, temp.previous.pos.y / PLAYABLE_TO_A_STAR_SCALE))
                    child = temp
                    temp = temp.previous
                    child.previous = None
                path.reverse()
                return path

            open_set.remove(current_spot)
            closed_set.append(current_spot)

            for neighbour in current_spot.neighbours:
                # If next spot is valid
                if neighbour not in closed_set and not neighbour.wall:
                    temp_g_value = current_spot.g_value + self.heuristic(neighbour, current_spot)

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

        return []  # No solution

    def heuristic(self, spot_a, spot_b):
        return distance(spot_a.pos.x, spot_a.pos.y, spot_b.pos.x, spot_b.pos.y)
  

class Spot:
    def __init__(self, x, y, simplified_map):
        self.pos = Vector2D(math.floor(x), math.floor(y))
        self.f_value = 0
        self.g_value = 0
        self.h_value = 0
        self.neighbours = []
        self.previous = None
        if simplified_map.customized_map[math.floor(y * A_STAR_TO_SIMPLIFIED_SCALE)][math.floor(x * A_STAR_TO_SIMPLIFIED_SCALE)] == 1:
            self.wall = True
        else:
            self.wall = False

    def reset_values(self):
        self.f_value = 0
        self.g_value = 0
        self.h_value = 0

    def add_neighours(self, map):
        x_pos = self.pos.x
        y_pos = self.pos.y

        # Horizontal and Vertical neighbours
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