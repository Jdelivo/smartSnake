import torch
import random
import torch.nn.functional as F

class snakeModel(torch.nn.Module):
    def __init__(self, inputs, hidden_neuron, outputs):
        """

        """
        super(snakeModel, self).__init__()
        self.layers = []
        self.layers.append(torch.nn.Linear(inputs, hidden_neuron).cuda())
        self.layers.append(torch.nn.Linear(hidden_neuron, hidden_neuron).cuda())
        self.layers.append(torch.nn.Linear(hidden_neuron, outputs).cuda())

    def forward(self, x):
        """

        """
        linear = self.layers[0](x).clamp(min=0)
        linear = self.layers[1](linear).clamp(min=0)
        y_pred = self.layers[2](linear).cuda()
        return y_pred

    def mutate(self, chance):
        for layer in range(len(self.layers)):
            for i in range(len(self.layers[layer].weight.data)):
                for j in range(len(self.layers[layer].weight.data[0])):
                    self.layers[layer].weight.data[i, j] = self.changeWeight(self.layers[layer].weight.data[i][j],
                                                                             chance)

    def changeWeight(self, weight, chance):
        rand = random.uniform(0, 1)
        if rand <= chance:
            weight = random.uniform(-1, 1)
        return weight

    def mate(self, mother, father):
        for layer in range(len(self.layers)):
            for i in range(len(self.layers[layer].weight.data)):
                for j in range(len(self.layers[layer].weight.data[0])):
                    self.layers[layer].weight.data[i][j] = mother.layers[layer].weight.data[i][j] \
                        if random.randint(0, 1) == 0 else father.layers[layer].weight.data[i][j]

