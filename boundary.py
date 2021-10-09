# from math_tools import Vector2D, distance
# import math

# class Boundary:
#     def __init__(self, ray):
#         # Rectangle
#         self.first_point = Vector2D(ray.pos.x, ray.pos.y)
#         self.second_point = Vector2D(ray.pos.x, ray.pos.y2)
#         self.is_upwards = True if (x2 - x1) >= 0 else False
#         self.is_rightwards = True if (y2 - y1) >= 0 else False
#         # self.top_right_p = Vector2D(x1 + length * math.cos(angle) - height * math.cos(math.pi / 2 - angle), y1 + )

#     def query(self, points, ray):
#         near_points = []
#         for point in points:
#             in_x_range = False
#             in_y_range = False
#             # Checks x bounds
#             if self.is_rightwards:
#                 if point.x >= self.first_point.x and point.x < self.second_point.x:
#                     in_x_range = True
#             else:
#                 if point.x >= self.second_point.x and point.x < self.first_point.x:
#                     in_x_range = True
            
#             # Checks y bounds
#             if self.is_upwards:
#                 if point.y >= self.first_point.y and point.y < self.second_point.y:
#                     in_y_range = True
#             else:
#                 if point.y >= self.second_point.y and point.y < self.first_point.y:
#                     in_y_range = True
            
#             if in_x_range and in_y_range:
#                 near_points.append(point)

#         hit = []
#         for point in near_points:
#             if 

#             slope = (self.first_point.y - self.second_point.y) / (self.first_point.x - self.second_point.x)
#             inverse_slope = -1 / slope

#             x_poi = ((point.pos.y - point.pos.x * inverse_slope) - (self.first_point.y - self.first_point.x * slope)) / (slope - inverse_slope)
#             y_poi = (self.first_point.x - x_poi) * slope + self.first_point.y

#             dist = distance(self.first_point.x, self.first_point.y, x_poi, y_poi)

#             if dist < 10:
#                 hit.append(point)