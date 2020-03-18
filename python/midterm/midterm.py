'''
    David Guido
    M/W: 11:30-12:45 | CPSC 386 | Intro to Game Design & Production

    Midterm Exam
    ------------

    Contains:
        1. class Ship
        2. class Vector

    Instructions:
        1. (25 pts) Write the code or pseudo-code in Python for the Ship class
        2. (25 pts) Write the code or pseudo-code in Python for the Vector class
'''


class Ship:
    def __init__(self, game, vector=Vector()):

        # Initialize (Ship) instance vars for single instance obj's game, screen & velocity
        self.game = game
        self.screen = game.screen
        self.velocity = vector

        # Initialize (Ship) instance vars for each element related to animation
        self.screen_rect = game.screen.get_rect()
        self.image = pg.image.load('ship.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.midbottom

        # Initialize the list of lazers
        self.lasers = pg.sprite.Group()

    def center_ship(self): 
        self.rect.center = self.screen_rect.midbottom   # Make sure the ship is in the correct positon

    def fire(self):
        laser = Laser(game=self.game)                   # Create new lazor to be fired shortly
        self.lasers.add(laser)                          # Add this lazer to the 'lazers' list

    def remove_lasers(self): 
        self.lasers.remove()                            # Remove this lazer to the 'lazers' list

    def move(self):
        if self.velocity == Vector():                   # If the len(Vector) == 0,
            return                                      # ==> Return
        self.rect.left += self.velocity.x               # Else, move the left side of the rect toward destination
        self.rect.top += self.velocity.y                # Move the top of the rect toward destination
        self.game.limit_on_screen(self.rect)

    def draw(self):
        self.screen.blit(self.image, self.rect)         # Use recently updated logic to the draw changes to the screen

    def update(self):
        fleet = self.game.fleet                         # Make this ship instance is part of the fleet
        self.move()
        self.draw()
        for laser in self.lasers.sprites():             # Update each lazer instance
            laser.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)                                   # Remove lazers that passed there respective experation
        pg.sprite.groupcollide(self.lasers, fleet.aliens, True, True)       # Return the lazers objs that participated in the recent collisions event with aliens
        if not fleet.aliens:                                                # If the alien isn't part of the fleet,
            self.game.restart()                                             # ==> Restart Game


class Vector:
    def __init__(self, x=0.0, y=0.0):                               # Initialize (x, y) velocity of vector
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)             # Return an easily understood (legible) representation of the vector

    def __add__(self, other):                                       # Return addition result of two vectors
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):                                       # Return subtraction result of two vectors
        return self.__add__(-1 * other)

    def __rmul__(self, k: float):                                   # Return scaler multiplication result on one vector
        return Vector(k * self.x, k * self.y)

    def __mul__(self, k: float):                                    # Return multiplication result of two vectors
        return self.__rmul__(k)

    def __truediv__(self, k: float):                                # Return division result of two vectors
        return self.__rmul__(1.0 / k)

    def __neg__(self):                                              # Negate vectors velocity
        self.x *= -1
        self.y *= -1

    def __eq__(self, other):                                        # Return equality result of two vectors
        return self.x == other.x and self.y == other.y

    @staticmethod
    def test():                                                     # Test the Vector class
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('uplusv is {}'.format(u + v))
        print('uminusv is {}'.format(u - v))
        print('ku is {}'.format(3 * u))
        print('-u is {}'.format(-1 * u))


def main():
    Vector.test()


if __name__ == '__main__':
    main()
