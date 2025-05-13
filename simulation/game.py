import pygame
from .environment import Environment


BG_COLOR = (30, 30, 30)
TARGET_COLOR = (100, 100, 255)


class Game:

    def __init__(self, environment: Environment):
        self.environment = environment
        pygame.init()
        self.screen = pygame.display.set_mode(
            (environment.width, environment.height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()

    def update(self):
        self.screen.fill(BG_COLOR)

        tX, tY = self.environment.target
        pygame.draw.circle(self.screen, TARGET_COLOR, (tX, tY), 15)

        for agent in self.environment.agents:
            agent.draw(self.screen)

        for ob in self.environment.obstacles:
            ob.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)

    def run(self, update_env=False):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if update_env:
                self.environment.update()
            self.update()

        pygame.quit()
