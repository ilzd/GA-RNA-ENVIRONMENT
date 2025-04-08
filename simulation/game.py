import pygame

BG_COLOR = (30, 30, 30)


class Game:

    def __init__(self, environment):
        self.environment = environment
        pygame.init()
        self.screen = pygame.display.set_mode(
            (environment.width, environment.height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()

    def update(self):

        self.screen.fill(BG_COLOR)
        self.environment.agent.cast_sensors(self.environment.staticObstacles +
                                            self.environment.movingObstacles, self.screen)
        self.environment.agent.draw(self.screen)

        for ob in self.environment.staticObstacles:
            ob.draw(self.screen)
        for ob in self.environment.movingObstacles:
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
