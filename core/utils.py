import math
from operator import add, mul
from collections import Iterable
from numbers import Complex
from decimal import Decimal

class Vector(tuple):

    def __new__(self, *args):
        if len(args) <= 1 and isinstance(args[0], Iterable):
            return tuple.__new__(self, args[0])
        return tuple.__new__(self, args)

    @property
    def length(self):
        """Returns the magnitude of the vector."""
        return math.sqrt(sum(n*n for n in self))

    @property
    def norm(self):
        """Returns a normalized version of the vector"""
        try:
            return Vector(map(lambda n: n/self.length, self))
        except ZeroDivisionError:
            print "shit"
            return self
    def __neg__(self):
        return self * -1

    def __add__(self, other):
        """Adds one vector to another"""
        return Vector(map(add, self, other))

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Iterable):
            return sum(map(mul, self, other))
        elif isinstance(other, Complex) or isinstance(other, Decimal):
            return Vector(n * other for n in self)
        raise TypeError("Multiplication of a vector with a non-Iterable/scalar")
    def __rmul__(self, other):
        return self * other

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]
