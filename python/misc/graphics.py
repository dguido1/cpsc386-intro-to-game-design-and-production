import pygame as pg
import sys
import time
from pygame.locals import *


# pixArray = pg.PixelArray(windowSurface)
# pixArray[480][360] = pg.Black
# del pixArray


class game:
    def __init__(self):
        pg.init()
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        self.basicFont = pg.font.SysFont(None, 48)
        self.surface = pg.display.set_mode((500, 400), 0, 32)

        self.text = self.basicFont.render("Hello, world!", True,
                                     self.WHITE, self.BLUE)
        self.textRect = self.text.get_rect()
        self.textRect.centerx = self.surface.get_rect().centerx
        self.textRect.centery = self.surface.get_rect().centery


def draw_polygon(game, fill_color):
    pg.draw.polygon(game.surface, fill_color,
                    ((146, 0), (291, 106), (236, 277),
                    (56, 277), (0, 106)))


def draw_z(game, line_color):
    pg.draw.line(game.surface, line_color, (60, 60), (120, 60), 4)
    pg.draw.line(game.surface, line_color, (120, 60), (60, 120), 4)
    pg.draw.line(game.surface, line_color, (60, 120), (120, 120), 4)


def draw_circle(game, fill_color):
    pg.draw.circle(game.surface, fill_color, (300, 50), 20, 0)


def draw_ellipse(game, line_color):
    pg.draw.ellipse(game.surface, line_color, (300, 250, 40, 80), 1)


def draw_textrect(game, fill_color):
    g = game
    tr = g.textRect
    pg.draw.rect(g.surface, fill_color,
                 (tr.left - 20, tr.top - 20,
                  tr.width + 40, tr.height + 40))
    g.surface.blit(g.text, tr)


def update_screen(game, dropping):
    g = game
    tr = g.textRect
    tr.top += 2 if dropping else -2
    if dropping and tr.top > 350:
        dropping = False
    if not dropping and tr.top < 20:
        dropping = True

    draw_polygon(g, fill_color=g.GREEN)
    draw_z(g, line_color=g.BLUE)
    draw_circle(g, fill_color=g.BLUE)
    draw_ellipse(g, line_color=g.RED)
    draw_textrect(g, fill_color=g.RED)
    pg.display.update()

    return dropping


def main():
    g = game()
    tr = g.textRect

    game_finished = False
    dropping = True
    while not game_finished:
        g.surface.fill(g.WHITE)
        dropping = update_screen(g, dropping)
        time.sleep(0.01)

        for event in pg.event.get():
            if event.type == QUIT:
                game_finished = True
                break

    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
