import Cube


class Snake:
    ''' Snake class, used to draw the snake and calculate its body position '''
    def __init__(self, pos):
        self.body = []
        self.head = Cube.Cube(pos)
        self.body.append(self.head)
        body1 = Cube.Cube((self.head.pos[0]+1, self.head.pos[1]))
        self.body.append(body1)
        body2 = Cube.Cube((self.head.pos[0] + 2, self.head.pos[1]))
        self.body.append(body2)
        self.direction = (-1, 0)

    def eat_snack(self, dire):
        self.head = Cube.Cube((self.head.pos[0] + dire[0], self.head.pos[1] + dire[1]))
        self.body.insert(0, self.head)

    def move(self, dire):
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].pos = self.body[i-1].pos
        self.head.pos = (self.head.pos[0] + dire[0], self.head.pos[1] + dire[1])
        self.direction = dire
