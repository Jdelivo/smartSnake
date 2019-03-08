import pygame
from snakeModel import SnakeModel
from Game import Game
import os
import numpy as np


def mate(mother, father, chance, num_of_inputs, hidden_neurons, num_of_outputs, models):
    ''' used to produce a new generation of neural networks '''
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
    delay = 0  # delay is necessary so that we can see what the snake does
    epochs = 0
    parent1 = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
    parent2 = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
    highscore = 0

    # create models folder to save our models
    if not os.path.exists('models'):
        os.makedirs('models')

    # try to load a generation from a previous execution
    try:
        epochs = np.load('epochs.npy')
        parent1.loadParent('parent1')
        parent2.loadParent('parent2')
        highscore = np.load('highscore.npy')
    except:
        np.save('epochs.npy', epochs)
        np.save('highscore.npy', highscore)
        parent1.saveParent('parent1')
        parent2.saveParent('parent2')

    last_gen_models = []
    for i in range(num_of_models):
        last_gen_models.append(SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs))

        try:
            last_gen_models[i].load(i)
        except:
            pass

    while True:
        epochs += 1
        np.save('epochs.npy', epochs)
        print('Epoch:', epochs)

        # try all the neural networks of this generation
        fitnesses = []
        scores = []
        for i in range(num_of_models):
            game = Game(surface, width, rows)
            model = last_gen_models[i]

            while True:
                if not game.play_turn(model, delay):
                    break

            fitnesses.append(game.fitness)
            scores.append(game.score)

        # produce new networks with 2 parents and mutation chance
        chance = 0.2
        print('Best score:', max(scores))
        if max(scores) > highscore:
            highscore = max(scores)

        print('Highscore:', highscore)

        if max(fitnesses) >= parent1.fitness:
            parent2 = parent1
            parent1 = last_gen_models[fitnesses.index(max(fitnesses))]
            parent1.fitness = max(fitnesses)
        elif max(fitnesses) >= parent2.fitness:
            parent2 = last_gen_models[fitnesses.index(max(fitnesses))]
            parent2.fitness = max(fitnesses)

        last_gen_models = mate(parent1, parent2, chance,
                               num_of_inputs, hidden_neurons, num_of_outputs, num_of_models)

        parent1.saveParent('parent1')
        parent2.saveParent('parent2')
        np.save('highscore.npy', highscore)


main()
