import pygame
from Game import Game

def main():
    width = 500
    rows = 20
    pygame.init()
    surface = pygame.display.set_mode((width, width))
    game = Game(surface, width, rows)
    while True:
        if game.moveUser():
            break

main()