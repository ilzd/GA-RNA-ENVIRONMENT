from ann import Network, activation

net = Network([5, 2, 10], activation_fn=activation.sigmoid)

input_data = [0.5, -0.3, 0.8, -0.1, 0.2]
output = net.forward(input_data)

print("Output:", output)
