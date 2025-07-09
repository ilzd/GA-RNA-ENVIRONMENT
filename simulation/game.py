import pygame
from .environment import Environment


BG_COLOR = (30, 30, 30)


class Game:

    def __init__(self, environment: Environment):
        self.environment = environment
        pygame.init()
        self.screen = pygame.display.set_mode(
            (environment.width, environment.height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.updating = False

    def update(self):
        self.screen.fill(BG_COLOR)

        for agent in self.environment.agents:
            agent.draw(self.screen)

        for ob in self.environment.obstacles:
            ob.draw(self.screen)

        pygame.display.flip()
        self.dt = self.clock.tick(20) / 1000.0

    def run(self, update_env=False):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.updating = not self.updating
            if (self.updating):
                if update_env:
                    self.environment.update(self.dt)
            self.update()

        pygame.quit()
