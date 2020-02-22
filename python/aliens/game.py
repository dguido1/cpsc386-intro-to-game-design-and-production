import pygame as pg

from pygame.locals import *
from pygame.sprite import Sprite
from vector import Vector


class Laser(Sprite):
    SPEED = 5
    WIDTH = 400
    HEIGHT = 15
    COLOR = (200, 0, 0)
    horizontal_grid = WIDTH / 8
    vertical_grid = HEIGHT / 8

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.color = Laser.COLOR
        self.rect = pg.Rect(0, 0, Laser.WIDTH, Laser.HEIGHT)
        self.rect.midtop = self.game.ship.rect.midtop
        self.velocity = Vector(0, -Laser.SPEED)
        self.y = float(self.rect.y)

    def move(self):
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y

    def draw(self): pg.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        print("The horizontal grid is made up of: " + self.horizontal_grid)
        print("The vertical grid is made up of: " + self.vertical)
        self.move()
        self.draw()


class Alien(Sprite):
    SPEED = 3

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.velocity = Alien.SPEED * Vector(1, 0)

        self.image = pg.image.load('alien.png')
        self.rect = self.image.get_rect()

        self.rect.left = self.rect.width
        self.rect.top = self.rect.height
        self.x = float(self.rect.x)

    def width(self): return self.rect.width

    def height(self): return self.rect.height

    def check_edges(self):
        r = self.rect
        s_r = self.screen.get_rect()
        return r.right >= s_r.right or r.left <= 0

    def draw(self): self.screen.blit(self.image, self.rect)

    def width(self): return self.rect.width

    def move(self):
        if self.velocity == Vector():
            return
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)

    def update(self):
        self.move()
        self.draw()


class Ship:
    def __init__(self, game, vector=Vector()):
        self.game = game
        self.screen = game.screen
        self.velocity = vector

        self.screen_rect = game.screen.get_rect()
        self.image = pg.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.lasers = pg.sprite.Group()

    def __repr__(self):
        r = self.rect
        return 'Ship({},{}),v={}'.format(r.x, r.y, self.velocity)

    def fire(self):
        laser = Laser(game=self.game)
        self.lasers.add(laser)

    def remove_lasers(self): self.lasers.remove()

    def center(self): self.rect.midbottom = self.screen_rect.midbottom

    def draw(self): self.screen.blit(self.image, self.rect)

    def move_to_node(self):

        # Move ship 4 directions, toward a new node
        if self.velocity == Vector(-1, 0):  # Move left ==> We want to move lefr one s

            print("turn left")
        if self.velocity == Vector(1, 0):   # Move right
            print("turn right")
        if self.velocity == Vector(0, -1):  # Move down
            print("turn down")
        if self.velocity == Vector(0, 1):   # Move up
            print("turn up")
        return

    def move(self):
        if self.velocity == Vector():
            return
        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.game.limit_on_screen(self.rect)

    def update(self):
        fleet = self.game.fleet
        self.move()
        self.draw()
        for laser in self.lasers.sprites():
            laser.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        pg.sprite.groupcollide(self.lasers, fleet.aliens, True, True)
        if not fleet.aliens:
            self.game.restart()


class Fleet:
    SPEED = 2

    def __init__(self, game):
        self.aliens = pg.sprite.Group()
        self.game = game

        alien = Alien(game=self.game)
        self.velocity = Fleet.SPEED * Vector(1, 0)
        w, h = alien.width(), alien.height()
        available_space_x = self.game.WIDTH - (2 * w)
        number_aliens_x = available_space_x // (2 * w)

        s_h = self.game.ship.rect.height
        available_space_y = self.game.HEIGHT - (3 * h) - s_h
        number_rows = available_space_y // (2 * h)

        for row in range(number_rows):
            for i in range(number_aliens_x):
                self.create_alien(n=i, row=row)

    def create_alien(self, n, row):
        alien = Alien(game=self.game)
        rect = alien.rect
        width, height = rect.size
        alien.x = width + 2 * n * width
        rect.x = alien.x
        rect.y = rect.height + 2 * height * row
        self.aliens.add(alien)

    def check_sides(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.game.HEIGHT:
                self.game.restart()

    def check_ship_hit(self):
        if pg.sprite.spritecollideany(self.game.ship, self.aliens):
            print('Ship HIT!')
            self.game.restart()
            return

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += Game.FLEET_DROP
            alien.velocity.x *= -1.2

    def update(self):
        self.check_sides()
        self.check_bottom()
        self.check_ship_hit()
        self.aliens.update()


class Game:
    SHIP_SPEED = 8
    WIDTH = 1200
    HEIGHT = 650
    SHIPS = 3
    FLEET_DROP = 10

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((Game.WIDTH, Game.HEIGHT))
        pg.display.set_caption('Aliens')
        self.bg_color = (40, 40, 40)   # dark grey
        self.finished: bool = False

        self.ships_left = 3
        self.ship = Ship(self)   # create ship before aliens
        self.fleet = Fleet(self)

    def limit_on_screen(self, rect):
        rect.left = max(0, rect.left)
        rect.right = min(rect.right, self.WIDTH)
        rect.top = max(0, rect.top)
        rect.bottom = min(rect.bottom, self.HEIGHT)

    def process_events(self):
        key_up_down = [pg.KEYDOWN, pg.KEYUP]
        movement = {K_RIGHT: Vector(1, 0), K_LEFT: Vector(-1, 0), K_UP: Vector(0, -1), K_DOWN: Vector(0, 1)}
        translate = {K_d: K_RIGHT, K_a: K_LEFT, K_w: K_UP, K_s: K_DOWN}
        for event in pg.event.get():
            e_type = event.type
            if e_type in key_up_down:
                k = event.key
                if k in translate.keys() or k in translate.values():     # movement
                    if k in translate.keys():
                        k = translate[k]
                    self.ship.velocity = Game.SHIP_SPEED * movement[k]
                    self.ship.move_to_node()
                elif k == pg.K_SPACE and e_type == pg.KEYDOWN:           # shoot laser
                    self.ship.fire()
                    return
            elif e_type == QUIT:                                         # quit
                self.finished = True

    def restart(self):
        self.ships_left -= 1
        print('{} ship{} left, Admiral.'.format(self.ships_left,
                                                "s" if self.ships_left > 1 else ""))
        if self.ships_left == 0:
            self.game_over()

        self.ship.center()
        self.ship.remove_lasers()
        self.fleet = Fleet(self)

    def game_over(self):
        print("GAME OVER.")
        quit()

    def update(self):
        self.screen.fill(self.bg_color)
        self.fleet.update()    # fleet controls aliens
        self.ship.update()     # ship controls lasers

    def play(self):
        while not self.finished:
            self.process_events()
            self.update()
            pg.display.update()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
