import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return self.x**2 + self.y**2

    def unit_vector(self):
        mag = self.magnitude()
        if (mag != 0):
            return Vector2D(self.x / mag, self.y / mag)
        else:
            return Vector2D()

    # operator functions
    def add(self, right):
        return Vector2D(self.x + right.x, self.y + right.y)
    
    def subtract(self, right):
        return Vector2D(self.x - right.x, self.y - right.y)
    
    def dot(self, right):
        return ((self.x * right.x) + (self.y + right.y))

    def scalar_multiply(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)