import random

import numpy as np
import random


def one_point_crossover(w1, b1, w2, b2):
    child_weights = []
    child_biases = []

    for w_layer1, w_layer2 in zip(w1, w2):
        shape = w_layer1.shape
        flat1 = w_layer1.flatten()
        flat2 = w_layer2.flatten()

        point = random.randint(1, len(flat1) - 1)
        child_flat = np.concatenate([flat1[:point], flat2[point:]])
        child_weights.append(child_flat.reshape(shape))
        

    for b_layer1, b_layer2 in zip(b1, b2):
        shape = b_layer1.shape
        flat1 = b_layer1.flatten()
        flat2 = b_layer2.flatten()

        point = random.randint(1, len(flat1) - 1)
        child_flat = np.concatenate([flat1[:point], flat2[point:]])
        child_biases.append(child_flat.reshape(shape))

    return child_weights, child_biases


def uniform_crossover(w1, b1, w2, b2, swap_prob=0.5):
    child_weights = []
    child_biases = []

    for w_layer1, w_layer2 in zip(w1, w2):
        mask = np.random.rand(*w_layer1.shape) < swap_prob
        child_layer = np.where(mask, w_layer1, w_layer2)
        child_weights.append(child_layer)

    for b_layer1, b_layer2 in zip(b1, b2):
        mask = np.random.rand(*b_layer1.shape) < swap_prob
        child_layer = np.where(mask, b_layer1, b_layer2)
        child_biases.append(child_layer)

    return child_weights, child_biases
