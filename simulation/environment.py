import pygame
from .agent import Agent
from .obstacle import StaticObstacle, MovingObstacle

BG_COLOR = (30, 30, 30)


class Environment:
    def __init__(self, width=1268, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Simulation")
        self.agent = Agent(width / 2, height / 2,
                           num_sensors=32, sensor_range=1000)
        self.staticObstacles = [
            StaticObstacle((300, 250, 200, 40)),
            StaticObstacle((200, 400, 100, 100)),
            StaticObstacle((500, 100, 50, 300))
        ]
        self.movingObstacles = [
            MovingObstacle(100, 100, radius=20, speed=2),
            MovingObstacle(400, 300, radius=20, speed=3)
        ]

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.agent.x = x
        self.agent.y = y
        self.screen.fill(BG_COLOR)
        self.agent.cast_sensors(self.staticObstacles, self.screen)
        self.agent.draw(self.screen)
        for ob in self.staticObstacles:
            ob.draw(self.screen)
        for ob in self.movingObstacles:
            ob.update(self.width, self.height)
            ob.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()

        pygame.quit()
