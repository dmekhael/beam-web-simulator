import numpy as np

class Beam:
    def __init__(self, length, load, E, I):
        self.length = length
        self.load = load
        self.E = E
        self.I = I

    def deflection(self, x):
        L = self.length
        P = self.load
        E = self.E
        I = self.I
        return (P * x * (L**3 - 2*L*x**2 + x**3)) / (48 * E * I)

    def bending_moment(self, x):
        L = self.length
        P = self.load
        return (P / 2) * (L / 2 - abs(x - L/2))
