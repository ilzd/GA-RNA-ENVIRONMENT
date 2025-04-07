import pygame
import math

SENSOR_COLOR = (100, 200, 250)
AGENT_COLOR = (50, 200, 50)

class Agent:
    def __init__(self, x, y, num_sensors=8, sensor_range=150):
        self.x = x
        self.y = y
        self.radius = 25
        self.num_sensors = num_sensors
        self.sensor_range = sensor_range
        self.sensor_angles = [
            i * (360 / self.num_sensors) for i in range(self.num_sensors)
        ]

    def draw(self, surface):
        pygame.draw.circle(surface, AGENT_COLOR, (self.x, self.y), self.radius)

    def cast_sensors(self, obstacles, surface=None):
        readings = []
        for rel_angle in self.sensor_angles:
            angle_rad = math.radians(rel_angle)
            dx = math.cos(angle_rad)
            dy = math.sin(angle_rad)
            distance = self._cast_single_ray(dx, dy, obstacles)
            end_point = (int(self.x + dx * distance), int(self.y + dy * distance))
            pygame.draw.line(surface, SENSOR_COLOR, (self.x, self.y), end_point, 1)
            readings.append(distance)
        return readings

    def _cast_single_ray(self, dx, dy, obstacles):
        step_size = 2
        for i in range(0, self.sensor_range, step_size):
            x = self.x + dx * i
            y = self.y + dy * i
            point = (int(x), int(y))
            if any(ob.rect.collidepoint(point) for ob in obstacles):
                return i
        return self.sensor_range
