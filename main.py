from ann import Network, activation
from simulation import Environment, Game, Agent, Obstacle
import random

# random.seed(0)'

if __name__ == "__main__":

    sensor_count = 6
    target = [1400, 650]

    agents = []
    for i in range(20):
        agents.append(Agent(200, 200, num_sensors=sensor_count, sensor_range=250, network=Network(
            [sensor_count + 2, 8, 3], activation_fn=activation.sigmoid), target=target))

    obstacles = [
        Obstacle(700, 400, radius=60),
        Obstacle(250, 700, radius=60),
        Obstacle(1200, 250, radius=60),
        Obstacle(500, 500, radius=40, speed=200),
        Obstacle(800, 300, radius=40, speed=150),
        Obstacle(1200, 600, radius=40, speed=250)
    ]

    env = Environment(agents=agents, obstacles=obstacles, target=target)
    game = Game(env)
    game.run(True)
