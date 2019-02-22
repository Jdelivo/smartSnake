import pygame
import torch
import snakeModel
import Game
import os

def mate(mother, father, chance, num_of_inputs, models):
    modelFather = snakeModel.snakeModel(num_of_inputs, 25, 4).cuda()
    modelMother = snakeModel.snakeModel(num_of_inputs, 25, 4).cuda()

    modelFather.load_state_dict(torch.load('models/model' + str(father) + '.pt'))
    modelMother.load_state_dict(torch.load('models/model' + str(mother) + '.pt'))

    for i in range(models - 2):
        kid = snakeModel.snakeModel(num_of_inputs, 25, 4).cuda()
        kid.mate(modelFather, modelMother)
        kid.mutate(chance)
        torch.save(kid.state_dict(), 'models/model' + str(i) + '.pt')
        print('I', end='')
    print()
    torch.save(modelMother.state_dict(), 'models/model8.pt')
    torch.save(modelFather.state_dict(), 'models/model9.pt')


def main():
    width = 500
    rows = 20
    num_of_inputs = 8
    surface = pygame.display.set_mode((width, width))
    num_of_models = 100
    epochs = 0
    pygame.init()
    for i in range(num_of_models):
        # create models folder to save our models
        if not os.path.exists('models'):
            os.makedirs('models')
        model = snakeModel.snakeModel(num_of_inputs, 25, 4).cuda()
        # if we haven't already saved models
        try:
            model.load_state_dict(torch.load('models/model' + str(i) + '.pt'))
        except:
            torch.save(model.state_dict(), 'models/model' + str(i) + '.pt')

    while True:
        print('Epoch:', epochs)
        epochs += 1

        fitness = []
        for i in range(num_of_models):
            game = Game.Game(surface, width, rows, num_of_models, num_of_inputs)
            model = snakeModel.snakeModel(num_of_inputs, 25, 4).cuda()
            model.load_state_dict(torch.load('models/model' + str(i) + '.pt'))

            while game.playTurn(model):
                pass

            fitness.append(game.fitness)

        chance = 0.1
        bestModels = []
        print('Best fitness:', max(fitness))
        for i in range(len(fitness)):
            bestModels.append(fitness.index(max(fitness)))
            fitness.remove(max(fitness))

        mate(bestModels[0], bestModels[1], chance, num_of_inputs, num_of_models)


main()
