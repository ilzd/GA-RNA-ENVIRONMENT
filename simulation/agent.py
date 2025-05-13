import pygame
import math
from ann import Network

SENSOR_COLOR = (100, 200, 250)
AGENT_COLOR = (50, 200, 50)
AGENT_COLOR_DEAD = (200, 50, 50)
BASE_SPEED = 300


class Agent:
    def __init__(self, x, y, num_sensors=8, sensor_range=150, network: Network = None, target=[0, 0]):
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
        self.totalTime = 0
        self.totalDistance = 0
        self.finalDistance = 0

    def init_angles(self):
        for i in range(self.num_sensors):
            angle = (2 * math.pi / self.num_sensors) * i
            self.sensor_angles.append(
                [angle, math.cos(angle),  math.sin(angle)])

    def update(self, obstacles, dt):
        self.check_dead(obstacles)
        
        if(self.dead):
            return
        
        self.totalTime += dt
        
        self.readings = self.cast_sensors(obstacles)
        output = self.network.forward(self.readings + self.target)
        self._move(output, dt)

    def _move(self, output, dt):
        dx, dy = normalize((output[0] - 0.5, output[1] - 0.5))
        speed = output[2] * BASE_SPEED * dt
        self.x += dx * speed
        self.y += dy * speed
        self.totalDistance += speed

    def draw(self, surface):
        if self.readings and not self.dead:
            for i in range(self.num_sensors):
                angle = self.sensor_angles[i]
                reading = self.readings[i]
                dx = angle[1] * reading
                dy = angle[2] * reading
                end_x = self.x + dx
                end_y = self.y + dy
                pygame.draw.line(surface, SENSOR_COLOR, (self.x, self.y),
                                 (end_x, end_y), 1)

        pygame.draw.circle(surface, AGENT_COLOR if self.dead == False else AGENT_COLOR_DEAD, (self.x, self.y), self.radius)

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
    
    def check_dead(self, obstacles):
        if self.dead:
            return
        for ob in obstacles:
            if ob.collides_with_point((self.x, self.y), self.radius):
                self.dead = True
                break
        

def clamp(n, smallest, largest): return max(smallest, min(n, largest))
def normalize(v):
    length = math.hypot(v[0], v[1])
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)