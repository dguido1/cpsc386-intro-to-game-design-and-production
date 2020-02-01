import pygame
from random import randint

# Dictionary of colors
colors = {'black': (0, 0, 0), 'white': (255, 255, 255)}


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()  # Call parent class constructor (Sprite)

        self.image = pygame.Surface([width, height])
        self.image.fill(colors['black'])
        self.image.set_colorkey(colors['black'])

        pygame.draw.rect(self.image, color, [0, 0, width, height])  # Draw ball
        self.velocity = [randint(4, 8), randint(-8, 8)]             # Random velocity
        self.rect = self.image.get_rect()                           # Get rect object matching image dimensions

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = randint(-8, 8)
