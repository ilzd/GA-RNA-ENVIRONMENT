from .agent import Agent
from .obstacle import Obstacle


class Environment:
    def __init__(self, width=1800, height=1000, agents: list[Agent] = [], obstacles: list[Obstacle] = [], max_duration=10):
        self.width = width
        self.height = height
        self.agents = agents
        self.obstacles = obstacles
        self.max_duration = max_duration
        self.curr_time = 0
        self.running = True

    def update(self, dt):
        if not self.running:
            return

        self.curr_time += dt
        if self.curr_time >= self.max_duration:
            self.stop()
            return

        all_agents_finished = True
        for agent in self.agents:
            agent.update(self.obstacles, dt)
            if not (agent.dead):
                all_agents_finished = False

        if all_agents_finished:
            self.stop()
            return

        for ob in self.obstacles:
            if (ob.speed != 0):
                ob.speed += 75 * dt
            ob.update(self.width, self.height, dt)

    def stop(self):
        self.running = False
