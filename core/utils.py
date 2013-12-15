import math
from operator import add, mul
from collections import Sequence
from numbers import Complex

class Vector(tuple):

    def __new__(cls, *args):
        if len(args) <= 1 and isinstance(args[0], Sequence):
            return tuple.__new__(cls, args[0])
        return tuple.__new__(cls, args)

    def __len__(self):
        """Returns the magnitude of the vector."""
        return math.sqrt(sum(n*n for n in self))

    def __invert__(self):
        """Returns a normalized version of the vector"""
        return Vector(map(lambda n: n/float(len(self)), self))

    def __add__(self, other):
        """Adds one vector to another"""
        return Vector(map(add, self, other))

    def __mul__(self, other):
        if isinstance(other, Sequence):
            return sum(map(mul, self, other))
        elif isinstance(other, Complex):
            return Vector(n * other for n in self)
        raise TypeError("Multiplication of a vector with a non-sequence/scalar")