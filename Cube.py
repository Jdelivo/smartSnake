import pygame


class Cube:
    ''' The snake and the snack consist of this class, used to draw the snake and the snack'''
    rows = 20
    w = 500

    def __init__(self, pos, cube_type="snake"):
        self.pos = pos
        if cube_type == "snake":
            self.color = (255, 0, 0)
        else:  # if type == snack
            self.color = (0, 255, 0)

    def draw(self, surface, head=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if head:
            centre = dis // 2
            radius = 3
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 50), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 50), circle_middle2, radius)
