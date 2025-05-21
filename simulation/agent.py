import pygame
import math
from ann import Network
import copy

SENSOR_COLOR = (100, 200, 250)
AGENT_COLOR = (50, 200, 50)
AGENT_COLOR_DEAD = (200, 50, 50)
AGENT_COLOR_WIN = (0, 200, 200)
BASE_SPEED = 300


class Agent:
    def __init__(self, x, y, num_sensors=8, sensor_range=150, network: Network = None, target=[0, 0, 20], bounds=[0, 0]):
        self.x = x
        self.y = y
        self.radius = 20
        self.num_sensors = num_sensors
        self.sensor_range = sensor_range
        self.sensor_angles = []
        self.init_angles()
        self.readings = []
        self.network = network
        self.target = target
        self.dead = False
        self.win = False
        self.total_time = 0
        self.total_distance = 0
        self.final_distance = 0
        self.bounds = bounds

    def init_angles(self):
        for i in range(self.num_sensors):
            angle = (2 * math.pi / self.num_sensors) * i
            self.sensor_angles.append(
                [angle, math.cos(angle),  math.sin(angle)])

    def update(self, obstacles, dt):
        self.check_dead(obstacles)
        self.check_win()
        if (self.dead or self.win):
            return

        self.total_time += dt

        self.readings = self.cast_sensors(obstacles)
        output = self.network.forward(self.readings + self.target)
        self._move(output, dt)

    def _move(self, output, dt):
        dx, dy = normalize((output[0] - 0.5, output[1] - 0.5))
        speed = output[2] * BASE_SPEED * dt
        self.x += dx * speed
        self.y += dy * speed
        self.total_distance += BASE_SPEED * dt

    def draw(self, surface):
        if self.readings and not (self.dead or self.win):
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
                           True else AGENT_COLOR if self.win == False else AGENT_COLOR_WIN, (self.x, self.y), self.radius)

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
            if x < 0 or y < 0 or x > self.bounds[0] or y > self.bounds[1]:
                return i
            if any(ob.collides_with_point(point) for ob in obstacles):
                return i
        return self.sensor_range

    def check_dead(self, obstacles):
        if self.win:
            return
        if self.dead:
            return
        for ob in obstacles:
            if ob.collides_with_point((self.x, self.y), self.radius):
                self.dead = True
                break
        if self.x < 0 or self.y < 0 or self.x > self.bounds[0] or self.y > self.bounds[1]:
            self.dead = True
            return

    def check_win(self):
        if math.hypot(self.x - self.target[0], self.y - self.target[1]) < (self.radius + self.target[2]):
            self.win = True
            return

    def finish(self, max_duration):
        max_possible_distance = BASE_SPEED * max_duration

        self.final_distance = clamp(math.hypot(
            self.x - self.target[0], self.y - self.target[1]), 0, max_possible_distance) / max_possible_distance

        self.total_time = clamp(
            self.total_time, 0, max_duration) / max_duration

        self.total_distance = clamp(
            self.total_distance, 0, max_possible_distance) / max_possible_distance


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def normalize(v):
    length = math.hypot(v[0], v[1])
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)
