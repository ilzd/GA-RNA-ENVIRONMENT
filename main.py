from ann import Network, activation
from simulation import Environment, Game
import random

# random.seed(0)'

if __name__ == "__main__":
    env = Environment()
    game = Game(env)
    game.run(True)