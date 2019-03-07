import pygame
from snakeModel import SnakeModel
from Game import Game
import os
import numpy as np

def mate(mother, father, chance, num_of_inputs, hidden_neurons, num_of_outputs, models):
    new_generation = []

    for i in range(models):
        kid = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
        kid.mate(father, mother)
        kid.mutate(chance)
        new_generation.append(kid)

    new_generation[-2].loadParent('parent1')
    new_generation[-1].loadParent('parent2')

    for i, model in enumerate(new_generation):
        model.save(i)
    print('--------------------')

    return new_generation


def main():
    width = 500
    rows = 20
    num_of_inputs = 6
    hidden_neurons = 25
    num_of_outputs = 3
    pygame.init()
    surface = pygame.display.set_mode((width, width))
    num_of_models = 200
    epochs = 0
    parent1 = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
    parent2 = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
    # create models folder to save our models
    if not os.path.exists('models'):
        os.makedirs('models')
    try:
        epochs = np.load('epochs.npy')
        parent1.load('parent1')
        parent2.load('parent2')
    except:
        np.save('epochs.npy', epochs)
        parent1.saveParent('parent1')
        parent2.saveParent('parent2')


    last_gen_models = []
    for i in range(num_of_models):
        last_gen_models.append(SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs))

        # if we haven't already saved models
        try:
            last_gen_models[i].load(i)
        except:
            pass

    while True:
        epochs += 1
        np.save('epochs.npy', epochs)
        print('Epoch:', epochs)

        fitnesses = []
        scores = []
        for i in range(num_of_models):
            game = Game(surface, width, rows)
            model = last_gen_models[i]

            while True:
                if not game.play_turn(model):
                    break

            fitnesses.append(game.fitness)
            scores.append(game.score)

        chance = 0.2
        print('Best fitness:', max(fitnesses))
        print('Best score:', max(scores))

        if max(fitnesses) >= parent1.fitness:
            parent2 = parent1
            parent1 = last_gen_models[fitnesses.index(max(fitnesses))]
            parent1.fitness = max(fitnesses)
            print('parent1 changed!!')
        elif max(fitnesses) >= parent2.fitness:
            parent2 = last_gen_models[fitnesses.index(max(fitnesses))]
            parent2.fitness = max(fitnesses)
            print('parent2 changed!!')

        print('parent1 fitness', parent1.fitness, end=' ')
        print('parent2 fitness', parent2.fitness)

        last_gen_models = mate(parent1, parent2, chance,
                               num_of_inputs, hidden_neurons, num_of_outputs, num_of_models)

        parent1.saveParent('parent1')
        parent2.saveParent('parent2')


main()
