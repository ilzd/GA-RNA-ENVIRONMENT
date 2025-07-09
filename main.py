from ann import Network, activation
from simulation import Environment, Game, Agent, Obstacle
from ag import roulette, tournament, elitism, compute_fitness, uniform_crossover, one_point_crossover, uniform_mutation, gaussian_mutation
import random
import keyboard
import copy
import json
import time

START_POS = [500, 500]
BOUNDS = [1000, 1000]
SENSOR_COUNT = 4
SENSOR_RANGE = 250
ANN_STRUCTURE = [SENSOR_COUNT, 16, 4]
ACTIVATION_FUNCTION = activation.sigmoid
POPULATION_SIZE = 50
SELECTION_COUNT = 24
MAX_GENERATIONS = 300
MAX_DURATION = 1
DELTA_TIME = 0.025
OBSTACLES = [
    Obstacle(250, 250, radius=50),
    Obstacle(250, 750, radius=50),
    Obstacle(750, 250, radius=50),
    Obstacle(750, 750, radius=50),
    Obstacle(500, 900, radius=50),
    Obstacle(100, 100, radius=50, speed=400),
    Obstacle(300, 100, radius=50, speed=400),
    Obstacle(400, 100, radius=50, speed=400),
    Obstacle(500, 100, radius=50, speed=400),
    Obstacle(600, 100, radius=50, speed=400),
    Obstacle(700, 100, radius=50, speed=400),
    Obstacle(900, 100, radius=50, speed=400),
    Obstacle(900, 300, radius=50, speed=400),
    Obstacle(900, 400, radius=50, speed=400),
    Obstacle(900, 500, radius=50, speed=400),
    Obstacle(900, 600, radius=50, speed=400),
    Obstacle(900, 700, radius=50, speed=400),
    Obstacle(900, 900, radius=50, speed=400),
    Obstacle(700, 900, radius=50, speed=400),
    Obstacle(600, 900, radius=50, speed=400),
    Obstacle(500, 900, radius=50, speed=400),
    Obstacle(400, 900, radius=50, speed=400),
    Obstacle(300, 900, radius=50, speed=400),
    Obstacle(100, 900, radius=50, speed=400),
    Obstacle(100, 700, radius=50, speed=400),
    Obstacle(100, 600, radius=50, speed=400),
    Obstacle(100, 500, radius=50, speed=400),
    Obstacle(100, 400, radius=50, speed=400),
    Obstacle(100, 300, radius=50, speed=400),
    Obstacle(100, 100, radius=50, speed=400),
]


def create_agent(weights=None, biases=None):
    return Agent(START_POS[0], START_POS[1], num_sensors=SENSOR_COUNT, sensor_range=SENSOR_RANGE, network=Network(
        ANN_STRUCTURE, activation_fn=ACTIVATION_FUNCTION, custom_weights=weights, custom_biases=biases), bounds=BOUNDS)


AGENTS = []
for i in range(POPULATION_SIZE):
    AGENTS.append(create_agent())


def initialize_environment(agents: list[Agent]):
    return Environment(width=BOUNDS[0], height=BOUNDS[1], agents=[create_agent(agt.network.get_weights(
    ), agt.network.get_biases()) for agt in agents], obstacles=copy.deepcopy(OBSTACLES), max_duration=MAX_DURATION)


def get_next_generation(agents, selection_count):
    selected_agents = elitism(agents=agents, amount=selection_count)

    random.shuffle(selected_agents)
    offspring = []

    for i in range(0, len(selected_agents) - 1, 2):
        parent1: Agent = selected_agents[i]
        parent2: Agent = selected_agents[i + 1]

        for _ in range(2):
            child_weights, child_biases = one_point_crossover(
                parent1.network.get_weights(), parent1.network.get_biases(), parent2.network.get_weights(), parent2.network.get_biases())

            mutated_weights, mutated_biases = uniform_mutation(
                child_weights, child_biases, 0.02)
            mutated_agent = create_agent(mutated_weights, mutated_biases)
            offspring.append(mutated_agent)

    for agt in selected_agents:
        # mutated_weights, mutated_biases = uniform_mutation(
        #     agt.network.get_weights(), agt.network.get_biases(), 0.02)
        # mutated_agent = create_agent(mutated_weights, mutated_biases)
        # offspring.append(mutated_agent)
        offspring.append(agt)

    while (len(offspring) < len(agents)):
        offspring.append(create_agent())

    return offspring


def train(initial_population=[], generation_count=MAX_GENERATIONS, selection_count=None):
    if not initial_population:
        return

    if selection_count == None:
        selection_count = round(len(initial_population) / 2)

    agents = initial_population
    data = {}
    env = initialize_environment(agents)
    while env.running:
        env.update(DELTA_TIME)

    curr_generation = 0
    while curr_generation < generation_count:
        curr_generation += 1

        agents = get_next_generation(env.agents, selection_count)

        env = initialize_environment(agents)
        while env.running:
            env.update(DELTA_TIME)

        sorted_fitness = sorted([compute_fitness(agt)
                                 for agt in env.agents], reverse=True)
        data[curr_generation] = sorted_fitness
        print(
            f"Generation {curr_generation}/{generation_count}: Best fitness: {sorted_fitness[0]}")

    with open(f"{time.strftime("%Y%m%d-%H%M%S")}.json", "a") as f:
        f.write(json.dumps(data))
    return env.agents


def run_game(agents):
    env = initialize_environment(agents)
    game = Game(env)
    game.run(True)


trained_agents = sorted(train(AGENTS, MAX_GENERATIONS, SELECTION_COUNT),
                        key=compute_fitness, reverse=True)
print("Training complete. Press space to visualize the results.")

keyboard.add_hotkey('space', lambda: run_game([create_agent()]))
keyboard.wait('enter')
