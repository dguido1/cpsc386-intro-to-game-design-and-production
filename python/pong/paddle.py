import pygame

# Dictionary of colors
colors = {'black': (0, 0, 0), 'white': (255, 255, 255)}


class Paddle(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()  # Call parent class constructor (Sprite)

        self.image = pygame.Surface([width, height])
        self.image.fill(colors['black'])
        self.image.set_colorkey(colors['black'])

        pygame.draw.rect(self.image, color, [0, 0, width, height])  # Draw rectangle
        self.rect = self.image.get_rect()                           # Get rect object matching image dimensions

    def up(self, pixels):
        self.rect.y -= pixels

    def down(self, pixels):
        self.rect.y += pixels
