import random
import math

class PVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return PVector(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        return PVector(self.x - v.x, self.y - v.y)

    def __mul__(self, s):
        return PVector(self.x * s, self.y * s)

    def __truediv__(self, s):
        return PVector(self.x / s, self.y / s)

    def __iadd__(self, v):
        self.x += v.x
        self.y += v.y
        return self

    def __isub__(self, v):
        self.x -= v.x
        self.y -= v.y
        return self

    def __imul__(self, s):
        self.x *= s
        self.y *= s
        return self

    def __itruediv__(self, s):
        self.x /= s
        self.y /= s
        return self

    def __str__(self):
        return f'({self.x},{self.y})'

    def set(self, x, y):
        self.x = x
        self.y = y

    def dot(self, v):
        return self.x*v.x + self.y*v.y

    def mag(self):
        return (self.x**2 + self.y**2) ** 0.5

    def normalize(self):
        mag = self.mag()
        if mag:
            self /= mag

    def limit(self, maxi):
        if self.mag() > maxi:
            self.normalize()
            self *= maxi

    def angle(self):
        return math.atan2(self.y, self.x)

    def angle_between(self, v):
        dot = self.dot(v)
        mag = self.mag() * v.mag()
        return math.acos(dot / mag)

    def xdirection(self):
        if self.x < 0.0:
            return -1
        elif self.x > 0.0:
            return 1
        else:
            return 0

    def ydirection(self):
        if self.y < 0.0:
            return -1
        elif self.y > 0.0:
            return 1
        else:
             return 0

    def zero(self):
        self.x = 0.0
        self.y = 0.0

    def xflat(self):
        self.y = 0.0

    def yflat(self):
        self.x = 0.0

    def repr(self):
        return self.x, self.y

    def copy(self):
        return PVector(self.x, self.y)

    @staticmethod
    def random():
        alpha = random.uniform(0, 2*math.pi)
        return PVector(math.sin(alpha), math.cos(alpha))

# TEST 1
# u = PVector(1, -1)
# print('1/2 pi = ', math.pi / 2)
# print('pi     = ', math.pi)
# print('3/2 pi = ', 3 * math.pi / 2)
# print()
# print(u)
# print(u.angle())

# TEST 2
# u = PVector(1,1)
# print(u.xdirection())
# print(u.ydirection())
