import Cube


class snake:
    cantGo = ''
    direction = 'LEFT'

    def __init__(self, pos):
        self.body = []
        self.head = Cube.cube(pos)
        self.body.append(self.head)

    def reset(self, pos):
        self.head = Cube.cube(pos)
        self.body = []
        self.body.append(self.head)
        self.cantGo = ''
        self.direction = 'LEFT'

    def eatSnack(self, pos):
        if self.body[0].pos == pos:
            return True
        else:
            return False

    def changeDirection(self, direction):
        if self.canGo(direction):
            self.direction = direction

    def move(self):
        if self.direction == 'UP':
            self.body = [Cube.cube((self.body[0].pos[0], self.body[0].pos[1]-1))] + self.body
            self.head = self.body[0]
            if len(self.body) > 1:
                self.cantGo = 'DOWN'
        elif self.direction == 'DOWN':
            self.body = [Cube.cube((self.body[0].pos[0], self.body[0].pos[1]+1))] + self.body
            self.head = self.body[0]
            if len(self.body) > 1:
                self.cantGo = 'UP'
        elif self.direction == 'RIGHT':
            self.body = [Cube.cube((self.body[0].pos[0]+1, self.body[0].pos[1]))] + self.body
            self.head = self.body[0]
            if len(self.body) > 1:
                self.cantGo = 'LEFT'
        elif self.direction == 'LEFT':
            self.body = [Cube.cube((self.body[0].pos[0]-1, self.body[0].pos[1]))] + self.body
            self.head = self.body[0]
            if len(self.body) > 1:
                self.cantGo = 'RIGHT'
        return self.body.pop()

    def canGo(self, direction):
        if self.cantGo == direction:
            return False
        else:
            return True
