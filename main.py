from ann import Network, activation
from simulation import Environment, Game, Agent, Obstacle
from ag import roulette, tournament, elitism, compute_fitness, uniform_crossover, one_point_crossover, uniform_mutation, gaussian_mutation
import random
import keyboard
import copy

START_POS = [500, 500]
BOUNDS = [1800, 1000]
SENSOR_COUNT = 6
SENSOR_RANGE = 250
ANN_STRUCTURE = [SENSOR_COUNT + 2, 8, 3]
ACTIVATION_FUNCTION = activation.sigmoid
TARGET = [1400, 650, 30]
POPULATION_SIZE = 20
MAX_GENERATIONS = 20
MAX_DURATION = 15
OBSTACLES = [
    Obstacle(720, 510, radius=60),
    Obstacle(1140, 660, radius=60),
    Obstacle(1400, 820, radius=60),
    Obstacle(1440, 475, radius=60),
    Obstacle(130, 160, radius=60),
    Obstacle(844, 200, radius=60),
    Obstacle(230, 600, radius=60),
    Obstacle(1343, 200, radius=60),
    Obstacle(500, 900, radius=60),
    Obstacle(400, 100, radius=60, speed=350),
    Obstacle(100, 100, radius=60, speed=350),
    Obstacle(100, 800, radius=60, speed=350),
    Obstacle(900, 900, radius=60, speed=350),
    Obstacle(1600, 400, radius=60, speed=350),
    Obstacle(1700, 300, radius=60, speed=350),
    Obstacle(500, 800, radius=60, speed=350),
    Obstacle(800, 100, radius=60, speed=350),
    Obstacle(300, 900, radius=60, speed=350),
    Obstacle(800, 800, radius=60, speed=350),
    Obstacle(900, 900, radius=60, speed=350),
    Obstacle(80, 80, radius=60, speed=350),
    Obstacle(400, 100, radius=60, speed=350),
    Obstacle(100, 100, radius=60, speed=350),
    Obstacle(100, 800, radius=60, speed=350),
    Obstacle(900, 900, radius=60, speed=350),
    Obstacle(1600, 400, radius=60, speed=350),
    Obstacle(1700, 300, radius=60, speed=350),
    Obstacle(500, 800, radius=60, speed=350),
    Obstacle(800, 100, radius=60, speed=350),
    Obstacle(300, 900, radius=60, speed=350),
    Obstacle(800, 800, radius=60, speed=350),
    Obstacle(900, 900, radius=60, speed=350),
    Obstacle(80, 80, radius=60, speed=350),
]


def create_agent(weights=None, biases=None):
    return Agent(START_POS[0], START_POS[1], num_sensors=SENSOR_COUNT, sensor_range=SENSOR_RANGE, network=Network(
        ANN_STRUCTURE, activation_fn=ACTIVATION_FUNCTION, custom_weights=weights, custom_biases=biases), target=TARGET, bounds=BOUNDS)


AGENTS = []
for i in range(POPULATION_SIZE):
    AGENTS.append(create_agent())


def initialize_environment(agents):
    return Environment(width=BOUNDS[0], height=BOUNDS[1], agents=[create_agent(agt.network.get_weights(
    ), agt.network.get_biases()) for agt in agents], obstacles=copy.deepcopy(OBSTACLES), target=TARGET, max_duration=MAX_DURATION)


def get_next_generation(agents):
    selected_agents = elitism(agents=agents, amount=round(len(agents)/2))

    random.shuffle(selected_agents)
    offspring = []
    for i in range(0, len(selected_agents) - 1, 2):
        parent1: Agent = selected_agents[i]
        parent2: Agent = selected_agents[i + 1]

        for _ in range(2):
            child_weights, child_biases = one_point_crossover(
                parent1.network.get_weights(), parent1.network.get_biases(), parent2.network.get_weights(), parent2.network.get_biases())

            mutated_weights, mutated_biases = gaussian_mutation(
                child_weights, child_biases)
            mutated_agent = create_agent(mutated_weights, mutated_biases)
            offspring.append(mutated_agent)

    for agt in selected_agents:
        mutated_weights, mutated_biases = gaussian_mutation(
            agt.network.get_weights(), agt.network.get_biases(), 0.1)
        mutated_agent = create_agent(mutated_weights, mutated_biases)
        offspring.append(mutated_agent)

    return offspring


def train(initial_population=[], generation_count=MAX_GENERATIONS):
    if not initial_population:
        return
    agents = initial_population
    curr_generation = 0
    while curr_generation < generation_count:
        curr_generation += 1
        env = initialize_environment(agents)
        while env.running:
            env.update(0.05)

        sorted_fitness = sorted([compute_fitness(agt)
                                 for agt in env.agents], reverse=True)
        print(f"Generation {curr_generation}/{generation_count}: Best fitness: {sorted_fitness[0]}")
        agents = get_next_generation(env.agents)
    return agents


def run_game(agents):
    env = initialize_environment(agents)
    game = Game(env)
    game.run(True)


trained_agents = train(AGENTS, MAX_GENERATIONS)
print("Training complete. Press space to visualize the results.")

keyboard.add_hotkey('space', lambda: run_game(trained_agents))
keyboard.wait('enter')
