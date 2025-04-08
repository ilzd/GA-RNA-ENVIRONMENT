from .agent import Agent
from .obstacle import StaticObstacle, MovingObstacle


class Environment:
    def __init__(self, width=1268, height=720):
        self.width = width
        self.height = height
        self.agent = Agent(width / 2, height / 2,
                           num_sensors=16, sensor_range=1000)
        self.staticObstacles = [
            StaticObstacle((300, 250, 200, 40)),
            StaticObstacle((200, 400, 100, 100)),
            StaticObstacle((500, 100, 50, 300))
        ]
        self.movingObstacles = [
            MovingObstacle(500, 500, radius=40, speed=2),
            MovingObstacle(800, 300, radius=40, speed=2)
        ]

    def update(self):
        for ob in self.movingObstacles:
            ob.update(self.width, self.height)
