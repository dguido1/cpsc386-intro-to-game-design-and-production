import pygame as pg
import sys
import random
import time
from pygame.locals import *
from vector import Vector


# -------------------------------------------------------------------------------------
class Food:
    WIDTH = 20
    HEIGHT = 20

    def __init__(self, game, left=-1, top=-1, width=-1, height=-1):
        if left == -1 or top == -1 or width == -1 or height == -1:
            left = random.randint(0, game.WINDOW_WIDTH - Food.WIDTH)
            top = random.randint(0, game.WINDOW_HEIGHT - Food.HEIGHT)
            width, height = Food.WIDTH, Food.WIDTH
        self.left, self.top = left, top
        self.width, self.height = width, height
        self.rect = pg.Rect(left, top, width, height)
        self.image = pg.image.load(game.food_image_src)

    def __repr__(self):
        return "Food(rect={})".format(self.rect)

    def draw(self, game):
        game.surface.blit(self.image, self.rect)
        # pg.draw.rect(game.surface, game.GREEN, self.rect)


# -------------------------------------------------------------------------------------
class Foods:
    append_attempts = 0
    initial_foods = 20

    def __init__(self, game):
        self.food_list = []
        self.food_interval = 20
        for i in range(Foods.initial_foods):
            self.append(Food(game=game))

    def append(self, food):
        self.food_list.append(food)

    def append_food_sometimes(self, game):
        Foods.append_attempts += 1
        if Foods.append_attempts % self.food_interval == 0:
            self.append(Food(game=game))

    def update(self, game):
        self.append_food_sometimes(game=game)
        self.draw(game)

    def draw(self, game):
        for food in self.food_list:
            food.draw(game)


# -------------------------------------------------------------------------------------
class Player:
    def __init__(self, rect, velocity=Vector(), image_src='player.png'):
        self.rect = rect
        self.velocity = velocity
        self.player = pg.Rect(300, 100, 50, 50)
        self.image = pg.image.load(image_src)
        self.stretched_image = pg.transform.scale(self.image, (rect.width, rect.height))

    def __repr__(self):
        return "Player(rect={},velocity={})".format(self.rect, self.velocity)

    def limit_to_screen(self, game):
        self.rect.top = max(0, min(game.WINDOW_HEIGHT - self.rect.height, self.rect.top))
        self.rect.left = max(0, min(game.WINDOW_WIDTH - self.rect.width, self.rect.left))

    def move(self, game):
        if self.velocity == Vector():
            return

        self.rect.left += self.velocity.x
        self.rect.top += self.velocity.y
        self.limit_to_screen(game)

    def move_to_random(self, game):
        self.rect.top = random.randint(0, game.WINDOW_HEIGHT - self.rect.height)
        self.rect.left = random.randint(0, game.WINDOW_WIDTH - self.rect.width)

    def check_collisions(self, game):
        for food in game.foods.food_list:
            if food.rect.colliderect(self.rect):
                game.foods.food_list.remove(food)
                self.grow(game=game)
                game.audio.play_sound(game.PICKUP_SOUND)

    def grow(self, game):
        r = self.rect
        self.rect = pg.Rect(r.left, r.top, r.width + 2, r.height + 2)
        self.limit_to_screen(game)
        self.stretched_image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))

    def draw(self, game):
        game.surface.blit(self.stretched_image, self.rect)
        # pg.draw.rect(game.surface, game.BLACK, self.rect)

    def update(self, game):
        self.check_collisions(game=game)
        self.move(game=game)
        self.draw(game=game)


# -------------------------------------------------------------------------------------
class Audio:   # sound(s) and background music
    def __init__(self, sounds, background_src, playing):
        self.sounds = {}
        for sound in sounds:
            for k, v in sound.items():
                self.sounds[k] = pg.mixer.Sound(v)
        self.background_src = background_src

        self.playing = playing
        pg.mixer.music.load(self.background_src)
        if self.playing:
            pg.mixer.music.play(-1, 0.0)

    def play_sound(self, sound):
        if self.playing and sound in self.sounds.keys():
            self.sounds[sound].play()

    def toggle(self, game):
        self.playing = not self.playing
        pg.mixer.music.play(-1, 0.0) if self.playing else pg.mixer.music.stop()


# -------------------------------------------------------------------------------------
class Game:
    def __init__(self, title):
        pg.init()
        self.player_speed = 6
        self.WINDOW_WIDTH = self.WINDOW_HEIGHT = 400
        self.player_img_src = 'player.png'
        self.food_image_src = 'cherry.png'
        self.background_src = 'background.mid'
        self.PICKUP_SOUND = 0
        sounds = [{self.PICKUP_SOUND: 'pickup.wav'}]

        self.player = Player(pg.Rect(300, 100, 50, 50),
                             self.player_speed * Vector(), image_src=self.player_img_src)
        self.foods = Foods(game=self)
        self.audio = Audio(sounds=sounds, background_src=self.background_src, playing=True)

        self.finished = False
        self.WHITE = (255, 255, 255)
        pg.display.set_caption(title)
        self.surface = pg.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), 0, 32)
        self.mainClock = pg.time.Clock()

    def process_event_loop(self, event):
        speed = self.player_speed
        e_type = event.type
        movement = {K_a: Vector(-1, 0), K_d: Vector(1, 0), K_w: Vector(0, -1), K_s: Vector(0, 1)}
        translate = {K_LEFT: K_a, K_RIGHT: K_d, K_UP: K_w, K_DOWN: K_s}
        left_right_up_down = (K_LEFT, K_a, K_RIGHT, K_d, K_UP, K_w, K_DOWN, K_s)

        if e_type == KEYDOWN or e_type == KEYUP:
            k = event.key
            if k == K_m and e_type == KEYUP:
                self.audio.toggle(self)
            elif k in left_right_up_down:
                if k in translate.keys():
                    k = translate[k]
                self.player.velocity = speed * movement[k]
                # self.player.velocity = speed * movement[k] if e_type == KEYDOWN else Vector()
            elif k == K_x:
                self.player.move_to_random(game=self)
        elif e_type == QUIT or (e_type == KEYUP and event.key == K_ESCAPE):
            self.finished = True
        elif e_type == MOUSEBUTTONUP:
            self.foods.append(Food(event.left, event.top, Food.WIDTH, Food.HEIGHT))

    def update(self):
        self.surface.fill(self.WHITE)
        self.foods.update(game=self)
        self.player.update(game=self)
        pg.display.update()

    def play(self):
        while not self.finished:
            for event in pg.event.get():
                self.process_event_loop(event)

            self.update()
            time.sleep(0.02)
            self.mainClock.tick(40)

        pg.quit()   # when self.finished
        sys.exit()


# -------------------------------------------------------------------------------------
def main():
    game = Game(title='Sprites and Images')
    game.play()


# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
