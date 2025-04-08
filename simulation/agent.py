import pygame
import math
from ann import Network, activation

SENSOR_COLOR = (100, 200, 250)
AGENT_COLOR = (50, 200, 50)
BASE_SPEED = 5


class Agent:
    def __init__(self, x, y, num_sensors=8, sensor_range=150):
        self.x = x
        self.y = y
        self.radius = 25
        self.num_sensors = num_sensors
        self.sensor_range = sensor_range
        self.sensor_angles = []
        self.init_angles()
        self.readings = []
        self.network = Network(
            [self.num_sensors, 10, 10, 3], activation_fn=activation.sigmoid)

    def init_angles(self):
        for i in range(self.num_sensors):
            angle = (2 * math.pi / self.num_sensors) * i
            self.sensor_angles.append(
                [angle, math.cos(angle),  math.sin(angle)])

    def update(self, obstacles):
        self.readings = self.cast_sensors(obstacles)
        output = self.network.forward(self.readings)
        self._move(output)

    def _move(self, output):
        dx = output[0] - 0.5
        dy = output[1] - 0.5
        speed = output[2] * BASE_SPEED
        self.x += dx * speed
        self.y += dy * speed

    def draw(self, surface):
        if self.readings:
            for i in range(self.num_sensors):
                angle = self.sensor_angles[i]
                reading = self.readings[i]
                dx = angle[1] * reading
                dy = angle[2] * reading
                end_x = self.x + dx
                end_y = self.y + dy
                pygame.draw.line(surface, SENSOR_COLOR, (self.x, self.y),
                                 (end_x, end_y), 1)

        pygame.draw.circle(surface, AGENT_COLOR, (self.x, self.y), self.radius)

    def cast_sensors(self, obstacles):
        readings = []
        for angle in self.sensor_angles:
            dx = angle[1]
            dy = angle[2]
            distance = self._cast_single_ray(dx, dy, obstacles)
            readings.append(distance)
        return readings

    def _cast_single_ray(self, dx, dy, obstacles):
        step_size = 5
        for i in range(0, self.sensor_range, step_size):
            x = self.x + dx * i
            y = self.y + dy * i
            point = (x, y)
            if any(ob.collides_with_point(point) for ob in obstacles):
                return i
        return self.sensor_range
