from abc import abstractmethod, ABC
import pygame
import math
import random

STATIC_OBSTACLE_COLOR = (100, 100, 100)
MOVING_OBSTACLE_COLOR = (255, 165, 0)


class Obstacle:
    def __init__(self, x, y, radius=15, speed=0, angle=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle if angle is not None else random.uniform(
            0, 2 * math.pi)
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        
    def update(self, screen_width, screen_height, dt):
        if (self.speed == 0):
            return

        self.x += self.dx * dt * self.speed
        self.y += self.dy * dt * self.speed
        margin = 200

        if self.x - self.radius <= -margin:
            self.x = self.radius - margin
            self.dx *= -1
        if self.x + self.radius >= screen_width + margin:
            self.x = screen_width - self.radius + margin
            self.dx *= -1
            
        if self.y - self.radius <= -margin:
            self.y = self.radius - margin
            self.dy *= -1
        if self.y + self.radius >= screen_height + margin:
            self.y = screen_height - self.radius + margin
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, STATIC_OBSTACLE_COLOR if self.speed ==
                           0 else MOVING_OBSTACLE_COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), self.radius, width=1)

    def collides_with_point(self, point, radius = 0):
        px, py = point
        distance = math.hypot(self.x - px, self.y - py)
        return distance <= (self.radius + radius)


# class Obstacle(ABC):
#     @abstractmethod
#     def collides_with_point(self, point):
#         pass


# class StaticObstacle(Obstacle):
#     def __init__(self, x, y, radius=15):
#         self.x = x
#         self.y = y
#         self.radius = radius

#     def draw(self, surface):
#         pygame.draw.circle(surface, STATIC_OBSTACLE_COLOR,
#                            (self.x, self.y), self.radius)

#     def collides_with_point(self, point):
#         px, py = point
#         distance = math.hypot(self.x - px, self.y - py)
#         return distance <= self.radius


# class MovingObstacle(Obstacle):
#     def __init__(self, x, y, radius=15, speed=2, angle=None):
#         self.x = x
#         self.y = y
#         self.radius = radius
#         self.speed = speed
#         self.angle = angle if angle is not None else random.uniform(
#             0, 2 * math.pi)
#         self.dx = math.cos(self.angle) * speed
#         self.dy = math.sin(self.angle) * speed

#     def update(self, screen_width, screen_height):
#         self.x += self.dx
#         self.y += self.dy

#         if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
#             self.dx *= -1
#         if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
#             self.dy *= -1

#     def draw(self, surface):
#         pygame.draw.circle(surface, MOVING_OBSTACLE_COLOR,
#                            (self.x, self.y), self.radius)

#     def collides_with_point(self, point):
#         px, py = point
#         distance = math.hypot(self.x - px, self.y - py)
#         return distance <= self.radius
