import random


def compute_fitness(agent):
    fitness = agent.total_time
    return fitness


def roulette(agents, amount):
    available_agents = agents.copy()
    selected = []

    # Compute initial fitness values
    fitness_values = [compute_fitness(agent) for agent in available_agents]
    min_fitness = min(fitness_values)
    adjusted_fitness = [f - min_fitness + 1e-6 for f in fitness_values]

    for _ in range(min(amount, len(available_agents))):
        total_fitness = sum(adjusted_fitness)
        pick = random.uniform(0, total_fitness)
        current = 0

        for i, (agent, fitness) in enumerate(zip(available_agents, adjusted_fitness)):
            current += fitness
            if current >= pick:
                selected.append(agent)

                # Remove agent and corresponding fitness value
                del available_agents[i]
                del adjusted_fitness[i]
                break

    return selected


def tournament(agents, amount, tournament_size=3):
    selected = []
    available_agents = agents.copy()

    while len(selected) < amount and len(available_agents) >= tournament_size:
        tournament = random.sample(available_agents, tournament_size)
        winner = max(tournament, key=compute_fitness)
        selected.append(winner)
        available_agents.remove(winner)

    return selected


def elitism(agents, amount):
    sorted_agents = sorted(agents, key=compute_fitness, reverse=True)
    return sorted_agents[:amount]
