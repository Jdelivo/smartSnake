import pygame
import tkinter as tk
from tkinter import messagebox
import random
import Cube
import Snake
import torch
import snakeModel

def drawGrid():
    global width, rows, surface
    sizeBtwn = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redrawWindow():
    global surface, width, rows, snake, snack
    surface.fill((0, 0, 0))  # fill the backround with black color
    drawGrid()  # draw lines to seperate the squares
    snake.body[0].draw(surface, True)  # draw the head of snake
    # draw the rest of the snake
    for cube in snake.body[1:]:
        cube.draw(surface)
    snack.draw(surface)  # draw the snack
    pygame.display.update()


def move(direction):
    global rows, snake, snack
    snake.changeDirection(direction)
    lastCube = snake.move()
    if snake.body[0].pos[0] < 0 or snake.body[0].pos[0] > rows-1 \
            or snake.body[0].pos[1] < 0 or snake.body[0].pos[1] > rows-1:
                return True
    else:
        if snake.body[0].pos == snack.pos:
            snake.body.append(lastCube)
            snack = randomSnack()
        return False


def randomSnack():
    global snake, rows
    positions = snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return Cube.cube((x, y), cubeType='snack')


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global surface, width, rows, snake, snack
    width = 500
    rows = 20
    pygame.init()
    surface = pygame.display.set_mode((width, width))
    snake = Snake.snake((10, 10))
    snack = randomSnack()
    # neural network model, H is hidden layers neurons
    hidden_neurons = 1024
    with torch.no_grad():
        # each generation has 10 models
        models = []
        for i in range(10):
            model = snakeModel.snakeModel(width * width * 3, hidden_neurons, 4)
            models.append(model)

            flag = True
            while flag:
                pygame.time.delay(100)
                inputs = pygame.surfarray.array3d(surface).reshape((-1))
                inputs_torch = torch.from_numpy(inputs)
                direction = models[i].model(inputs_torch)
                crashed = move(direction)

                for x in range(len(snake.body)):
                    if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])) or crashed:
                        print('Score: ', len(snake.body))
                        if len(snake.body) < rows * rows:
                            message_box('You Lost!', 'Play again...')
                        else:
                            message_box('You actually won the snake game!', 'Play again...')
                        snake.reset((10, 10))
                        break

                redrawWindow()


main()
