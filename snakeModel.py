import torch
import random


class snakeModel(torch.nn.Module):
    def __init__(self, inputs, hidden_neuron, outputs):
        """

        """
        super(snakeModel, self).__init__()
        self.score = -1
        self.linear1 = torch.nn.Linear(inputs, hidden_neuron)
        self.linear2 = torch.nn.Linear(hidden_neuron, hidden_neuron)
        self.linear3 = torch.nn.Linear(hidden_neuron, outputs)

    def forward(self, x):
        """

        """
        h1_relu = self.linear1(x).clamp(min=0)
        h2_relu = self.linear2(h1_relu).clamp(min=0)
        y_pred = self.linear3(h2_relu)
        return y_pred

    def evaluate(self, score):
        self.score = score

    def mutate(self, chance):
        weights1 = self.linear1.params()
        weights2 = self.linear2.params()
        weights3 = self.linear3.params()
        for i in range(len(weights1)):
            for j in range(len(weights1[0])):
                weights1[i][j] = self.changeWeight(weights1[i][j], chance)
        for i in range(len(weights2)):
            for j in range(len(weights2[0])):
                weights2[i][j] = self.changeWeight(weights2[i][j], chance)
        for i in range(len(weights3)):
            for j in range(len(weights3[0])):
                weights3[i][j] = self.changeWeight(weights3[i][j], chance)

    def changeWeight(self,weight, chance):
        got = random.uniform(1.0)
        if got <= chance:
            temp = random.randint(2)
            if temp == 0:
                weight = -weight
            if temp == 1:
                weight *= random.uniform(1.0)
            if temp == 2:
                weight += weight * random.uniform(1.0)
        return  weight
