import pygame
import math
from ann import Network
import copy

SENSOR_COLOR = (100, 200, 250)
AGENT_COLOR = (50, 200, 50)
AGENT_COLOR_DEAD = (200, 50, 50)
BASE_SPEED = 300


class Agent:
    def __init__(self, x, y, num_sensors=8, sensor_range=150, network: Network = None, bounds=[0, 0]):
        self.x = x
        self.y = y
        self.radius = 20
        self.num_sensors = num_sensors
        self.sensor_range = sensor_range
        self.sensor_angles = []
        self.init_angles()
        self.readings = []
        self.network = network
        self.dead = False
        self.total_time = 0
        self.bounds = bounds

    def init_angles(self):
        for i in range(self.num_sensors):
            angle = (2 * math.pi / self.num_sensors) * i
            self.sensor_angles.append(
                [angle, math.cos(angle),  math.sin(angle)])

    def update(self, obstacles, dt):
        self.check_dead(obstacles)
        if (self.dead):
            return

        self.total_time += dt

        self.readings = self.cast_sensors(obstacles)
        output = self.network.forward(self.readings)
        self._move(output, dt)

    def _move(self, output, dt):
        dx = 0
        dy = 0
        
        if(output[0] > 0.5):
            dx += 1
        if(output[1] > 0.5):
            dx += -1
        if(output[2] > 0.5):
            dy += 1
        if(output[3] > 0.5):
            dy += -1

        speed = BASE_SPEED * dt
        self.x += dx * speed
        self.y += dy * speed

    def draw(self, surface):
        if self.readings and not (self.dead):
            for i in range(self.num_sensors):
                angle = self.sensor_angles[i]
                reading = self.readings[i]
                dx = angle[1] * reading
                dy = angle[2] * reading
                end_x = self.x + dx
                end_y = self.y + dy
                pygame.draw.line(surface, SENSOR_COLOR, (self.x, self.y),
                                 (end_x, end_y), 1)
        pygame.draw.circle(surface, AGENT_COLOR_DEAD if self.dead ==
                           True else AGENT_COLOR, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), self.radius, width=1)

    def cast_sensors(self, obstacles):
        readings = []
        for angle in self.sensor_angles:
            dx = angle[1]
            dy = angle[2]
            distance = self._cast_single_ray(dx, dy, obstacles)
            readings.append(distance)
        return readings

    def _cast_single_ray(self, dx, dy, obstacles):
        step_size = 10
        for i in range(0, self.sensor_range, step_size):
            x = self.x + dx * i
            y = self.y + dy * i
            point = (x, y)
            if x < 0 or y < 0 or x > self.bounds[0] or y > self.bounds[1]:
                return i
            if any(ob.collides_with_point(point) for ob in obstacles):
                return i
        return self.sensor_range

    def check_dead(self, obstacles):
        if self.dead:
            return
        for ob in obstacles:
            if ob.collides_with_point((self.x, self.y), self.radius):
                self.dead = True
                break
        if self.x < 0 or self.y < 0 or self.x > self.bounds[0] or self.y > self.bounds[1]:
            self.dead = True
            return


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def normalize(v):
    length = math.hypot(v[0], v[1])
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)
