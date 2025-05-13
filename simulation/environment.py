from .agent import Agent
from .obstacle import Obstacle


class Environment:
    def __init__(self, width=1600, height=800, agents: list[Agent] = [], obstacles: list[Obstacle] = [], target=(0, 0)):
        self.width = width
        self.height = height
        self.agents = agents
        self.obstacles = obstacles
        self.target = target

    def update(self):
        for agent in self.agents:
            agent.update(self.obstacles)
        for ob in self.obstacles:
            ob.update(self.width, self.height)
