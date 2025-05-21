import numpy as np
import copy

def gaussian_mutation(weights, biases, mutation_rate=0.1, std_dev=0.1):
    new_weights = []
    new_biases = []

    for w in weights:
        w_mutated = w.copy()
        mask = np.random.rand(*w.shape) < mutation_rate
        noise = np.random.normal(0, std_dev, w.shape)
        w_mutated += noise * mask
        new_weights.append(w_mutated)

    for b in biases:
        b_mutated = b.copy()
        mask = np.random.rand(*b.shape) < mutation_rate
        noise = np.random.normal(0, std_dev, b.shape)
        b_mutated += noise * mask
        new_biases.append(b_mutated)

    return new_weights, new_biases

def uniform_mutation(weights, biases, mutation_rate=0.1, low=-1.0, high=1.0):
    new_weights = []
    new_biases = []

    for w in weights:
        w_mutated = w.copy()
        mask = np.random.rand(*w.shape) < mutation_rate
        random_values = np.random.uniform(low, high, w.shape)
        w_mutated = np.where(mask, random_values, w_mutated)
        new_weights.append(w_mutated)

    for b in biases:
        b_mutated = b.copy()
        mask = np.random.rand(*b.shape) < mutation_rate
        random_values = np.random.uniform(low, high, b.shape)
        b_mutated = np.where(mask, random_values, b_mutated)
        new_biases.append(b_mutated)

    return new_weights, new_biases