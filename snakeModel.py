import random
import numpy as np


class SnakeModel:
    ''' Neural network class with feedforward, sigmoid activation and mutation '''
    fitness = 0

    def __init__(self, num_of_inputs, hidden_neurons, num_of_outputs):
        self.layers = []
        self.layers.append(np.random.rand(num_of_inputs, hidden_neurons))
        self.layers.append(np.random.rand(hidden_neurons, hidden_neurons))
        self.layers.append(np.random.rand(hidden_neurons, num_of_outputs))

    def feedforward(self, x):
        hidden_layer1 = self.sigmoid(np.dot(x, self.layers[0]))
        hidden_layer2 = self.sigmoid(np.dot(hidden_layer1, self.layers[1]))
        output = self.sigmoid(np.dot(hidden_layer2, self.layers[2]))
        return output

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def mutate(self, chance):
        for layer in range(len(self.layers)):
            for i in range(len(self.layers[layer])):
                for j in range(len(self.layers[layer][0])):
                    self.layers[layer][i, j] = self.change_weight(self.layers[layer][i][j], chance)

    def change_weight(self, weight, chance):
        rand = random.uniform(0, 1)
        if rand <= chance:
            weight = random.uniform(-1, 1)
        return weight

    def mate(self, mother, father):
        for layer in range(len(self.layers)):
            for i in range(len(self.layers[layer])):
                for j in range(len(self.layers[layer][0])):
                    self.layers[layer][i][j] = mother.layers[layer][i][j] if \
                        random.randint(0, 1) == 0 else father.layers[layer][i][j]

    def save(self, i):
        np.save('models/model' + str(i) + '.npy', self.layers)

    def load(self, i):
        self.layers = np.load('models/model' + str(i) + '.npy')

    def saveParent(self, parent):
        np.save('models/' + parent + 'layers.npy', self.layers)
        np.save('models/' + parent + 'fitness.npy', self.fitness)

    def loadParent(self, parent):
        self.layers = np.load('models/' + parent + 'layers.npy')
        self.fitness = np.load('models/' + parent + 'fitness.npy')
