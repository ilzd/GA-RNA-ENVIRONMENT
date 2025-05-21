from .layer import Layer
from . import activation
import copy

class Network:
    def __init__(self, layer_sizes, activation_fn=activation.sigmoid, custom_weights=None, custom_biases=None):
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            weights = custom_weights[i] if custom_weights else None
            biases = custom_biases[i] if custom_biases else None
            layer = Layer(
                input_size=layer_sizes[i],
                output_size=layer_sizes[i + 1],
                activation_fn=activation_fn,
                weights=weights,
                biases=biases
            )
            self.layers.append(layer)

    def forward(self, input_data):
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def get_weights(self):
        return copy.deepcopy([layer.weights for layer in self.layers])
    
    def get_biases(self):
        return copy.deepcopy([layer.biases for layer in self.layers])
