import torch
import pygame
import Snake
import random
import Cube
import numpy as np


class Game:

    def __init__(self, surface, width, rows, num_of_models, num_of_inputs):
        self.surface = surface
        self.width = width
        self.rows = rows
        self.num_of_models = num_of_models
        self.num_of_inputs = num_of_inputs
        self.snake = Snake.snake((10, 10))
        self.snack = self.randomSnack()
        self.allowedSteps = 40
        self.delay = 20
        self.fitness = 0

    def playTurn(self, model):
        if self.allowedSteps > 0:
            self.allowedSteps -= 1

            pygame.time.delay(self.delay)

            up = self.seeForward(1, 0)
            down = self.seeForward(-1, 0)
            right = self.seeForward(0, 1)
            left = self.seeForward(0, -1)

            snack_right, snack_left, snack_front, snack_back = self.snackVector()

            inputs = np.array([up, down, left, right, snack_right, snack_left, snack_front, snack_back])
            inputs_torch = torch.from_numpy(inputs).float().cuda()
            direction = model(inputs_torch).max(0)[1].item()

            if direction == 0:
                dir_s = 'UP'
            elif direction == 1:
                dir_s = 'DOWN'
            elif direction == 2:
                dir_s = 'RIGHT'
            else:
                dir_s = 'LEFT'
            crashed = self.move(dir_s)

            for x in range(len(self.snake.body)):
                if self.snake.head.pos in list(map(lambda z: z.pos, self.snake.body[x + 1:])) or crashed:
                    if len(self.snake.body) < self.rows * self.rows:
                        crashed = True
                        self.snake.reset((10, 10))
                        break
            # else redraw the window with the new position of the snake
            self.redrawWindow()

            # if the snake has crushed we clear the cache of the gpu
            if crashed:
                self.fitness -= 1
                return False

            return True
        else:
            print('DID NOT DIE!')
            self.fitness += 1
            return False

    def randomSnack(self):
        positions = self.snake.body

        while True:
            x = random.randrange(self.rows)
            y = random.randrange(self.rows)
            if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
                continue
            else:
                break
        return Cube.cube((x, y), cubeType='snack')

    def seeForward(self, vert, hor):
        x = list(self.snake.head.pos)
        x[0] += vert
        x[1] += hor
        if 0 > x[0] or 0 > x[1] or self.rows-1 < x[0] or self.rows-1 < x[1]:
            return -1
        elif self.snake.body[0].pos in list(map(lambda z: z.pos, self.snake.body[1:])):
            return -1
        elif self.snake.head.pos == list(self.snack.pos):
                return 1
        return 0

    def snackVector(self):
        if self.snake.direction == 'RIGHT':
            front = 1 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 0
            back = 0 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 1
            right = 1 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 0
            left = 0 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 1
            return front, back, right, left
        elif self.snake.direction == 'LEFT':
            front = 1 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 0
            back = 0 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 1
            left = 1 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 0
            right = 0 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 1
            return front, back, right, left
        elif self.snake.direction == 'UP':
            left = 1 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 0
            right = 0 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 1
            back = 1 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 0
            front = 0 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 1
            return front, back, right, left
        else:
            left = 1 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 0
            right = 0 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 1
            front = 1 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 0
            back = 0 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 1
            return front, back, right, left

    def move(self, direction):
        self.snake.changeDirection(direction)
        lastCube = self.snake.move()
        if self.snake.head.pos[0] < 0 or self.snake.head.pos[0] > self.rows - 1 \
                or self.snake.head.pos[1] < 0 or self.snake.head.pos[1] > self.rows - 1:
            return True
        else:
            if self.snake.head.pos == self.snack.pos:
                self.snake.body.append(lastCube)
                self.snack = self.randomSnack()
                self.fitness += 1
                print('SNACK!')
                self.allowedSteps += 40
            return False

    def drawGrid(self):
        sizeBtwn = self.width // self.rows
        x = 0
        y = 0
        for l in range(self.rows):
            x = x + sizeBtwn
            y = y + sizeBtwn
            pygame.draw.line(self.surface, (255, 255, 255), (x, 0), (x, self.width))
            pygame.draw.line(self.surface, (255, 255, 255), (0, y), (self.width, y))

    def redrawWindow(self):
        self.surface.fill((0, 0, 0))  # fill the backround with black color
        self.drawGrid()  # draw lines to seperate the squares
        self.snake.body[0].draw(self.surface, True)  # draw the head of snake
        # draw the rest of the snake
        for cube in self.snake.body[1:]:
            cube.draw(self.surface)
        self.snack.draw(self.surface)  # draw the snack
        pygame.display.update()
