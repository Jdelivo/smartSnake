import pygame
import SnakeModel
import Game
import os
import numpy as np

def mate(mother, father, chance, num_of_inputs, hidden_neurons, num_of_outputs, models):
    new_generation = []

    for i in range(models - 2):
        kid = SnakeModel.SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)
        kid.mate(father, mother)
        kid.mutate(chance)
        new_generation.append(kid)

    new_generation.append(father)
    new_generation.append(mother)

    for i, model in enumerate(new_generation):
        model.save(i)
        print('I', end='')
    print()

    return new_generation


def main():
    width = 500
    rows = 20
    num_of_inputs = 24
    hidden_neurons = 25
    num_of_outputs = 4
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
        last_gen_models.append(SnakeModel.SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs))

        # if we haven't already saved models
        try:
            last_gen_models[i].load(i)
        except:
            pass

    while True:
        epochs += 1
        np.save('epochs.npy', epochs)
        print('Epoch:', epochs)

        fitness = []
        for i in range(num_of_models):
            game = Game.Game(surface, width, rows)
            model = last_gen_models[i]

            while True:
                if not game.play_turn(model):
                    break

            fitness.append(game.fitness)

        chance = 0.1
        best_models = []
        print('Best fitness:', max(fitness))
        for i in range(len(fitness)):
            best_models.append(fitness.index(max(fitness)))
            fitness.remove(max(fitness))

        last_gen_models = mate(last_gen_models[best_models[0]], last_gen_models[best_models[1]], chance,
                               num_of_inputs, hidden_neurons, num_of_outputs, num_of_models)


main()
