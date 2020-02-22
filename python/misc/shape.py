import math
from abc import ABC, abstractmethod


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({:.2f}, {:.2f})".format(self.x, self.y)

    def distance(self, other):
        delx = self.x - other.x
        dely = self.y - other.y
        return math.sqrt(delx * delx + dely * dely)

    @staticmethod
    def test():
        pt = Point()
        pt2 = Point(2, 3)
        print("pt is: {}, and pt2 is: {}".format(pt, pt2))
        print("distance from pt to pt2 is: {:.2f}".format(pt.distance(pt2)))


class Shape(ABC):
    def __init__(self, center=Point()):
        self.center = center

    def __repr__(self):
        return "area={:.2f},perimeter={:.2f}".format(self.area(), self.perimeter())

    @abstractmethod
    def area(self): pass

    @abstractmethod
    def perimeter(self): pass


class Circle(Shape):
    def __init__(self, radius, center=Point()):
        super().__init__(center)
        self.radius = radius

    def __repr__(self):
        return "Circle(r={},ctr={},{}".format(self.radius, self.center, super().__repr__())

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2.0 * math.pi * self.radius

    @staticmethod
    def test():
        c = Circle(radius=5.0)
        c2 = Circle(radius=10.0, center=Point(x=5.0, y=5.0))
        print("c is: {}".format(c))
        print("c2 is: {}".format(c2))


def main():
    Point.test()
    Circle.test()



if __name__ == '__main__':
    main()
