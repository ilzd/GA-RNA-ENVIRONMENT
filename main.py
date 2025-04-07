from ann import Network, activation
from simulation import Environment

if __name__ == "__main__":
    env = Environment()
    env.run()


net = Network([2, 5, 4], activation_fn=activation.sigmoid)

input_data = [0.5, -0.3]
output = net.forward(input_data)

print("Output:", output)
