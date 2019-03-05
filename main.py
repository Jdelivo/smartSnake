import pygame
from SnakeModel import SnakeModel
from Game import Game
import os
import numpy as np

def mate(mother, father, chance, num_of_inputs, hidden_neurons, num_of_outputs, models):
    new_generation = []

    for i in range(models - 2):
        kid = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
        kid.mate(father, mother)
        kid.mutate(chance)
        new_generation.append(kid)

    new_generation.append(father)
    new_generation.append(mother)

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
    try:
        epochs = np.load('epochs.npy')
    except:
        np.save('epochs.npy', epochs)
    # create models folder to save our models
    if not os.path.exists('models'):
        os.makedirs('models')

    last_gen_models = []
    for i in range(num_of_models):
        last_gen_models.append(SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs))

        # if we haven't already saved models
        try:
            last_gen_models[i].load(i)
        except:
            pass

    bestScoreSoFar = 0

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

        chance = 0.1
        best_models = []
        print('Best fitness:', max(fitnesses))
        print('Best score:', max(scores))
        if max(scores) > bestScoreSoFar:
            bestScoreSoFar = max(scores)
        print('Best score so far:', bestScoreSoFar)
        for i in range(len(fitnesses)):
            best_models.append(fitnesses.index(max(fitnesses)))
            fitnesses.remove(max(fitnesses))

        last_gen_models = mate(last_gen_models[best_models[0]], last_gen_models[best_models[1]], chance,
                               num_of_inputs, hidden_neurons, num_of_outputs, num_of_models)


main()
