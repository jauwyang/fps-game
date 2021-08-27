from math_tools import Vector2D
import math
import pygame

class Player:
    def __init__(self, x, y, colour):
        self.pos = Vector2D(x, y)
        self.rays = []
        self.heading = 0
        self.colour = colour

    def rotate(self, angle):
        self.heading += angle
        offset = 0
        for ray in self.rays:
            ray.set_angle(math.radians(offset) + self.heading)
            offset += 1

    def update_position(self, delta_x, delta_y):
        self.pos.x += delta_x
        self.pos.y += delta_y

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.pos.x, self.pos.y), 5)