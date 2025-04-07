from abc import abstractmethod, ABC
import pygame
import math
import random

OBSTACLE_COLOR = (200, 50, 50)
MOVING_OBSTACLE_COLOR = (255, 165, 0)


class Obstacle(ABC):
    @abstractmethod
    def collides_with_point(self, point):
        pass


class StaticObstacle(Obstacle):
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

    def draw(self, surface):
        pygame.draw.rect(surface, OBSTACLE_COLOR, self.rect)

    def collides_with_point(self, point):
        return self.rect.collidepoint(point)


class MovingObstacle(Obstacle):
    def __init__(self, x, y, radius=15, speed=2, angle=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.angle = angle if angle is not None else random.uniform(
            0, 2 * math.pi)
        self.dx = math.cos(self.angle) * speed
        self.dy = math.sin(self.angle) * speed

    def update(self, screen_width, screen_height):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius <= 0 or self.x + self.radius >= screen_width:
            self.dx *= -1
        if self.y - self.radius <= 0 or self.y + self.radius >= screen_height:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, MOVING_OBSTACLE_COLOR,
                           (self.x, self.y), self.radius)

    def collides_with_point(self, point):
        px, py = point
        distance = math.hypot(self.x - px, self.y - py)
        return distance <= self.radius
