from .agent import Agent
from .obstacle import Obstacle

class Environment:
    def __init__(self, width=1800, height=1000, agents: list[Agent] = [], obstacles: list[Obstacle] = [], target=[0, 0, 20], max_duration = 10):
        self.width = width
        self.height = height
        self.agents = agents
        self.obstacles = obstacles
        self.target = target
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
            if not (agent.dead or agent.win):
                all_agents_finished = False
        
        if all_agents_finished:
            self.stop()
            return
        
        for ob in self.obstacles:
            ob.update(self.width, self.height, dt)
        
        return 
    
    def stop(self):
        self.running = False
        for agent in self.agents:
            agent.finish(self.max_duration)