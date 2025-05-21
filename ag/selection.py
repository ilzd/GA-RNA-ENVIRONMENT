import random


def compute_fitness(agent):
    fitness = 0

    if agent.win:
        fitness += 1
        fitness += 0.2 * (1 - agent.total_distance)
        fitness -= 0.1 * (1 - agent.total_time)
    else:
        fitness += 1 * agent.total_time
        fitness += 0.5 * (1 - agent.final_distance)

    return fitness


def roulette(agents, amount):
    fitness_values = [compute_fitness(agent) for agent in agents]
    min_fitness = min(fitness_values)

    adjusted_fitness = [f - min_fitness + 1e-6 for f in fitness_values]
    total_fitness = sum(adjusted_fitness)

    selected = []
    for _ in range(amount):
        pick = random.uniform(0, total_fitness)
        current = 0
        for agent, fitness in zip(agents, adjusted_fitness):
            current += fitness
            if current >= pick:
                selected.append(agent)
                break
    return selected


def tournament(agents, amount, tournament_size=3):
    selected = []
    for _ in range(amount):
        tournament = random.sample(agents, tournament_size)
        winner = max(tournament, key=compute_fitness)
        selected.append(winner)
    return selected


def elitism(agents, amount):
    sorted_agents = sorted(agents, key=compute_fitness, reverse=True)
    return sorted_agents[:amount]
