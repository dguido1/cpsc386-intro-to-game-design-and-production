import pygame as pg
from pygame.locals import *


class Game:

    # --- Window ----
    # Dimensions
    window_width = 1000
    window_height = 500
    window_size = (window_width, window_height)

    # --- PACMAN ----
    pac_x = 500
    pac_y = 250
    pac_center = (pac_x, pac_y)
    pac_radius = 25
    pac_velocity = 15
    pac_sprite = pg.image.load('pacman.png')

    # Dictionary of colors
    colors = {'black': (0, 0, 0), 'white': (255, 255, 255), 'grey': (40, 40, 40)}

    def __init__(self):
        # Initialize all imported pygame modules
        pg.init()

        # Open application
        self.window = pg.display.set_mode(Game.window_size)

        # Title of application
        pg.display.set_caption("Pacman Portal")

        self.bg_color = Game.colors['grey']
        self.is_finished: bool = False

    def play(self):
        while not self.is_finished:
            self.handle_input()
            self.update()
            pg.display.update()

    # Check for user input, move character (movement needs to be handled in its own method inside pac man class)
    def handle_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_finished = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_x:
                    self.is_finished = True

        # Store all recent events in 'keys'
        keys = pg.key.get_pressed()

        # Check for user input
        if keys[pg.K_LEFT]:
            Game.pac_x -= Game.pac_velocity
        if keys[pg.K_RIGHT]:
            Game.pac_x += Game.pac_velocity
        if keys[pg.K_UP]:
            Game.pac_y -= Game.pac_velocity
        if keys[pg.K_DOWN]:
            Game.pac_y += Game.pac_velocity

    def update(self):
        # Clear content to only grey BG before drawing
        self.window.fill(Game.colors['grey'])

        # Check left bounds
        if Game.pac_x < -20:
            Game.pac_x = Game.window_width
        # Check right bounds
        elif Game.pac_x > Game.window_width + 10:
            Game.pac_x = 0
        # Check top bounds
        elif Game.pac_y < -20:
            Game.pac_y = Game.window_height
        # Check bottom bounds
        elif Game.pac_y > Game.window_height + 10:
            Game.pac_y = 0

        # Update center of pac man, draw to screen (temporary)
        Game.pac_center = (Game.pac_x, Game.pac_y)
        self.window.blit(Game.pac_sprite, Game.pac_center)


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()