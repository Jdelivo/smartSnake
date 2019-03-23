import pygame
from Snake import Snake
import random
from Cube import Cube
import numpy as np
import math


class Game:
    def __init__(self, surface, width, rows):
        self.surface = surface
        self.width = width
        self.rows = rows
        self.snake = Snake((10, 10))
        self.allowedSteps = 40
        self.fitness = 0
        self.snack = self.innit_snack(is_random=True)
        self.distance = math.sqrt((self.snack.pos[0] - self.snake.head.pos[0])**2 +
                                  (self.snack.pos[1] - self.snake.head.pos[1])**2)
        self.score = 0

    def play_turn(self, model, delay):
        ''' Each turn move or eat a snack'''
        if self.allowedSteps > 0:
            self.allowedSteps -= 1

            pygame.time.delay(delay)

            inputs = np.array([*self.inputs()]).reshape(-1)
            direction = np.argmax(model.feedforward(inputs))
            crashed = None
            if direction == 0:
                crashed = self.move(self.snake.direction)
            elif direction == 1:
                if self.snake.direction == (1, 0):
                    crashed = self.moveDown()
                elif self.snake.direction == (-1, 0):
                    crashed = self.moveUp()
                elif self.snake.direction == (0, -1):
                    crashed = self.moveRight()
                elif self.snake.direction == (0, 1):
                    crashed = self.moveLeft()
            else:
                if self.snake.direction == (1, 0):
                    crashed = self.moveUp()
                elif self.snake.direction == (-1, 0):
                    crashed = self.moveDown()
                elif self.snake.direction == (0, -1):
                    crashed = self.moveLeft()
                elif self.snake.direction == (0, 1):
                    crashed = self.moveRight()

            if crashed:
                return False

            newDistance = abs(self.snack.pos[0] - self.snake.head.pos[0]) +\
                          abs(self.snack.pos[1] - self.snake.head.pos[1])

            if newDistance < self.distance:
                self.fitness += 1
            else:
                self.fitness -= 1.5

            self.distance = newDistance
            return True
        else:
            return False

    def inputs(self):
        ''' Calculate what the snake sees and where is the snack '''
        snackAhead = 0
        snackRight = 0
        snackLeft = 0
        wallAhead = 1
        wallRight = 1
        wallLeft = 1
        if self.snake.direction == (1, 0):
            if self.snack.pos[1] == self.snake.head.pos[1] and self.snake.head.pos[0] < self.snack.pos[0]:
                snackAhead = 1
            else:
                if self.snack.pos[1] > self.snake.head.pos[1]:
                    snackRight = 1
                else:
                    snackLeft = 1
                snackAhead = 0
            wallAhead = self.look((1, 0))
            wallRight = self.look((0, 1))
            wallLeft = self.look((0, -1))
        elif self.snake.direction == (-1, 0):
            if self.snack.pos[1] == self.snake.head.pos[1] and self.snake.head.pos[0] > self.snack.pos[0]:
                snackAhead = 1
            else:
                if self.snack.pos[1] < self.snake.head.pos[1]:
                    snackRight = 1
                else:
                    snackLeft = 1
                snackAhead = 0
            wallAhead = self.look((-1, 0))
            wallRight = self.look((0, -1))
            wallLeft = self.look((0, 1))
        elif self.snake.direction == (0, -1):
            if self.snack.pos[0] == self.snake.head.pos[0] and self.snake.head.pos[1] > self.snack.pos[1]:
                snackAhead = 1
            else:
                if self.snack.pos[0] > self.snake.head.pos[0]:
                    snackRight = 1
                else:
                    snackLeft = 1
                snackAhead = 0
            wallAhead = self.look((0, -1))
            wallRight = self.look((1, 0))
            wallLeft = self.look((-1, 0))
        else:
            if self.snack.pos[0] == self.snake.head.pos[0] and self.snake.head.pos[1] < self.snack.pos[1]:
                snackAhead = 1
            else:
                if self.snack.pos[1] < self.snake.head.pos[1]:
                    snackRight = 1
                else:
                    snackLeft = 1
                snackAhead = 0
            wallAhead = self.look((0, 1))
            wallRight = self.look((-1, 0))
            wallLeft = self.look((1, 0))
        return snackAhead, snackRight, snackLeft, wallAhead, wallRight, wallLeft

    def look(self, direction):
        ''' Check a single direction until collapse on wall '''
        distance = 1
        cube = (self.snake.head.pos[0]+direction[0], self.snake.head.pos[1]+direction[1])
        while cube not in list(map(lambda x: x.pos, self.snake.body[1:])) and 0 < cube[0] < self.rows -1 and 0 < cube[1] < self.rows-1:
            distance += 1
            cube = (cube[0] + direction[0], cube[1] + direction[1])
        return 1 / distance

    def moveUp(self):
        return self.move((0, -1))

    def moveDown(self):
        return self.move((0, 1))

    def moveRight(self):
        return self.move((1, 0))

    def moveLeft(self):
        return self.move((-1, 0))

    def innit_snack(self, is_random=True):
        ''' Re-innitialize the snack to a new position '''
        positions = self.snake.body

        while True:
            if is_random:
                x = random.randrange(1, self.rows-1)
                y = random.randrange(1, self.rows-1)
                if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
                    continue
                else:
                    break
            else:
                return Cube((15,15), cube_type='snack')
        return Cube((x, y), cube_type='snack')

    def move(self, dire):
        ''' Move to a new square or eat a snack'''
        newpos = (self.snake.head.pos[0] + dire[0], self.snake.head.pos[1] + dire[1])
        if newpos == self.snack.pos:
            self.snake.eat_snack(dire)
            self.snack = self.innit_snack()
            self.fitness += 20
            self.score += 1
            self.allowedSteps += 100
            self.redraw_window()
            return False
        else:
            self.snake.move(dire)
            self.redraw_window()
            if newpos[0] == 0 or newpos[0] == self.rows - 1 or newpos[1] == 0 or newpos[1] == self.rows - 1:
                return True
            elif newpos in list(map(lambda x: x.pos, self.snake.body[1:])):
                return True
            return False


    # Used to redraw the window each turn
    def draw_grid(self):
        size_btwn = self.width // self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x = x + size_btwn
            y = y + size_btwn
            pygame.draw.line(self.surface, (255, 255, 255), (x, 0), (x, self.width))
            pygame.draw.line(self.surface, (255, 255, 255), (0, y), (self.width, y))

    def redraw_window(self):
        self.surface.fill((0, 0, 0))  # fill the backround with black color
        self.draw_grid()  # draw lines to seperate the squares
        self.snake.body[0].draw(self.surface, True)  # draw the head of snake
        # draw the rest of the snake
        for cube in self.snake.body[1:]:
            cube.draw(self.surface)
        self.snack.draw(self.surface)  # draw the snack
        pygame.display.update()
