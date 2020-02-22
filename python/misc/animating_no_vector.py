import pygame as pg
import sys
import time
from pygame.locals import *


class Vector:    # fill in code here
    pass


class Game:
    def __init__(self):
        pg.init()

        self.finished = False
        self.WINDOWWIDTH = 400
        self.WINDOWHEIGHT = 400
        self.surface = pg.display.set_mode(
            (self.WINDOWWIDTH, self.WINDOWHEIGHT), 0, 32)
        pg.display.set_caption('Animation')

        self.MOVESPEED = 4

        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        b1 = {'rect': pg.Rect(300, 80, 50, 100), 'color': self.RED,
              'velocity': self.MOVESPEED * Vector(3.0, -7.0)}
        b2 = {'rect': pg.Rect(200, 200, 20, 20), 'color': self.GREEN,
              'velocity': self.MOVESPEED * Vector(-1.0, -1.0)}
        b3 = {'rect': pg.Rect(100, 150, 60, 60), 'color': self.BLUE,
              'velocity': self.MOVESPEED * Vector(-1.0, 1.0)}
        self.boxes = [b1, b2, b3]


def move_box(box):
    # g = game
    b = box

    b['rect'].left += b['velocity'].x
    b['rect'].top += b['velocity'].y


def check_collision(game, box):
    g = game
    b = box
    r = b['rect']
    if r.top < 0 or r.bottom > g.WINDOWHEIGHT:
        b['velocity'].y *= -1
    if r.left < 0 or r.right > g.WINDOWWIDTH:
        b['velocity'].x *= -1


def main():
    Vector.test_vectors()    # calls static method

    g = Game()

    while not g.finished:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        g.surface.fill(g.WHITE)
        for b in g.boxes:
            move_box(box=b)
            check_collision(game=g, box=b)
            pg.draw.rect(g.surface, b['color'], b['rect'])

        pg.display.update()
        time.sleep(0.02)


if __name__ == '__main__':
    main()
