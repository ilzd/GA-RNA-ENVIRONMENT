import random
from . import activation
import numpy as np


class Layer:
    def __init__(self, input_size, output_size, activation_fn=activation.relu, weights=None, biases=None):
        self.input_size = input_size
        self.output_size = output_size
        self.activation_fn = activation_fn

        self.weights = weights if weights is not None else np.array([
            [random.uniform(-1, 1) for _ in range(input_size)] for _ in range(output_size)
        ])
        # print('weights: ')
        # print(self.weights)
        self.biases = biases if biases is not None else np.array([
            random.uniform(-1, 1) for _ in range(output_size)])
        # print('biases: ')
        # print(self.biases)

    def forward(self, inputs):
        outputs = []
        for i in range(self.output_size):
            weighted_sum = sum(inputs[j] * self.weights[i][j]
                               for j in range(self.input_size)) + self.biases[i]
            outputs.append(self.activation_fn(weighted_sum))
        return outputs
