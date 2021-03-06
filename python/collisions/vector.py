class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


    def __repr__(self):
        return "Vector ({}, {})".format(self.x, self.y)


    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return self.__add__(-1 * other)


    def __rmul__(self, k: float):
        return Vector(k * self.x, k * self.y)


    def __mul__(self, k: float):
        return self.__rmul__(k)


    def __truediv__(self, k: float):
        return self.__rmul__(1.0 / k)


    def __neg__(self):
        self.x *= -1
        self.y *= -1


    @staticmethod
    def test():
        v = Vector(x=5, y=5)
        u = Vector(x=4, y=4)
        print('v is {}'.format(v))
        print('u is {}'.format(u))
        print('uplusv is {}'.format(u + v))
        print('uminusv is {}'.format(u - v))
        print('ku is {}'.format(3 * u))
        print('-u is {}'.format(-1 * u))
