import pygame
from snakeModel import SnakeModel
from Game import Game


def main():
    ''' This is used to test the best neural network so far. Luck is a great factor of whether it runs smoothly. '''
    width = 500
    rows = 20
    num_of_inputs = 6
    hidden_neurons = 25
    num_of_outputs = 3
    pygame.init()
    surface = pygame.display.set_mode((width, width))
    delay = 100  # delay is necessary so that we can see what the snake does
    model = SnakeModel(num_of_inputs, hidden_neurons, num_of_outputs)

    try:
        model.loadParent('parent1')
    except:
        pass

    game = Game(surface, width, rows)
    while True:
        if not game.play_turn(model, delay):
            break

    print('Score was ', game.score)


main()
