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
            i * ((2 * math.pi) / self.num_sensors) for i in range(self.num_sensors)
        ]
        self.readings = []

    def update(self, obstacles):
        self.readings = self.cast_sensors(obstacles)

    def draw(self, surface):
        if self.readings:
            for i in range(self.num_sensors):
                angle = self.sensor_angles[i]
                reading = self.readings[i]
                dx = math.cos(angle) * reading
                dy = math.sin(angle) * reading
                end_x = int(self.x + dx)
                end_y = int(self.y + dy)
                pygame.draw.line(surface, SENSOR_COLOR, (self.x, self.y),
                                 (end_x, end_y), 1)

        pygame.draw.circle(surface, AGENT_COLOR, (self.x, self.y), self.radius)

    def cast_sensors(self, obstacles):
        readings = []
        for angle in self.sensor_angles:
            dx = math.cos(angle)
            dy = math.sin(angle)
            distance = self._cast_single_ray(dx, dy, obstacles)
            readings.append(distance)
        return readings

    def _cast_single_ray(self, dx, dy, obstacles):
        step_size = 2
        for i in range(0, self.sensor_range, step_size):
            x = self.x + dx * i
            y = self.y + dy * i
            point = (int(x), int(y))
            if any(ob.collides_with_point(point) for ob in obstacles):
                return i
        return self.sensor_range
