import pygame
import Snake
import random
import Cube
import numpy as np


class Game:
    def __init__(self, surface, width, rows):
        self.surface = surface
        self.width = width
        self.rows = rows
        self.snake = Snake.Snake((10, 10))
        self.allowedSteps = 40
        self.delay = 1000  # delay is necessary so that we can see what the snake does
        self.fitness = 0
        self.snack = self.innit_snack(is_random=False)

    def play_turn(self, model):

        if self.allowedSteps > 0:
            self.allowedSteps -= 1

            pygame.time.delay(self.delay)

            up = self.see_forward(0, -1)
            upright = self.see_forward(1, -1)
            right = self.see_forward(1, 0)
            downright = self.see_forward(1, 1)
            down = self.see_forward(0, 1)
            downleft = self.see_forward(-1, 1)
            left = self.see_forward(-1, 0)
            upleft = self.see_forward(-1, -1)

            # snack_right, snack_left, snack_front, snack_back = self.snack_vector()

            inputs = np.array([up, upleft, upright, right, left, down, downright, downleft]).reshape(-1)
            direction = np.argmax(model.feedforward(inputs))
            print(inputs)
            if direction == 0:
                dir_s = (0, -1)
            elif direction == 1:
                dir_s = (0, 1)
            elif direction == 2:
                dir_s = (1, 0)
            else:
                dir_s = (-1, 0)
            crashed = self.move(dir_s)

            if crashed:
                self.fitness -= 1
                return False

            self.redraw_window()
            return True
        else:
            print('DID NOT DIE!')
            return False

    def innit_snack(self, is_random=True):
        positions = self.snake.body

        while True:
            if is_random:
                x = random.randrange(self.rows)
                y = random.randrange(self.rows)
                if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
                    continue
                else:
                    break
            else:
                return Cube.Cube((15,15), cube_type='snack')
        return Cube.Cube((x, y), cube_type='snack')

    def see_forward(self, hor, vert):
        x = list(self.snake.head.pos)
        dist_snack, dist_wall, dist_body = 0, 0, 0
        distance = 0
        body_found = False
        snack_found = False
        while True:
            x[0] += hor
            x[1] += vert
            distance += 1
            if not (1 < x[0] < self.rows-2 and 1 < x[1] < self.rows-2):
                break
            if not body_found and tuple(x) in list(map(lambda z: z.pos, self.snake.body[1:])):
                dist_body = distance
            elif not snack_found and tuple(x) == self.snack.pos:
                dist_snack = distance
        dist_wall = distance
        return [dist_snack, dist_wall, dist_body]

    def snack_vector(self):
        if self.snake.direction == (1, 0):
            front = 1 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 0
            back = 0 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 1
            right = 1 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 0
            left = 0 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 1
            return front, back, right, left
        elif self.snake.direction == (-1, 0):
            front = 1 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 0
            back = 0 if self.snack.pos[0] - self.snake.head.pos[0] > 0 else 1
            left = 1 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 0
            right = 0 if self.snack.pos[1] - self.snake.head.pos[1] > 0 else 1
            return front, back, right, left
        elif self.snake.direction == (0, -1):
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

    def move(self, dire):
        newpos = (self.snake.head.pos[0] + dire[0], self.snake.head.pos[1] + dire[1])
        if newpos[0] < 0 or newpos[0] > self.rows - 1 or newpos[1] < 0 or newpos[1] > self.rows - 1:
            return True
        elif newpos in list(map(lambda x: x.pos, self.snake.body)):
            return True
        else:
            if newpos == self.snack.pos:
                self.snake.eat_snack(dire)
                self.snack = self.innit_snack()
                self.fitness += 1
                print('SNACK!')
                self.allowedSteps += 40
            else:
                self.snake.move(dire)
            return False

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
