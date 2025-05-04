import numpy as np

class Beam:
    def __init__(self, length, load, E, I, load_type):
        self.L = length
        self.P = load
        self.E = E
        self.I = I
        self.type = load_type

    def max_deflection(self):
        if self.type == "point":
            return (self.P * self.L**3) / (48 * self.E * self.I)
        elif self.type == "uniform":
            return (5 * self.P * self.L**4) / (384 * self.E * self.I)
        elif self.type == "moment":
            return (self.P * self.L**2) / (2 * self.E * self.I)
        else:
            return 0

    def formula(self):
        if self.type == "point":
            return "δ_max = P·L³ / 48·E·I"
        elif self.type == "uniform":
            return "δ_max = 5·w·L⁴ / 384·E·I"
        elif self.type == "moment":
            return "δ_max = M·L² / 2·E·I"
        else:
            return "N/A"

    def explanation(self):
        if self.type == "point":
            return "For a simply supported beam with a center point load, the maximum deflection occurs at mid-span."
        elif self.type == "uniform":
            return "For a beam with a uniformly distributed load, deflection is spread smoothly across the span."
        elif self.type == "moment":
            return "For a cantilever beam with an end moment, the maximum deflection occurs at the free end."
        else:
            return "Unknown load type."

    def moment_array(self, x):
        if self.type == "point":
            return np.where(x <= self.L/2,
                            self.P * x / 2,
                            self.P * (self.L - x) / 2)
        elif self.type == "uniform":
            return (self.P * x / self.L) * (self.L - x / 2)
        elif self.type == "moment":
            return np.full_like(x, self.P)
        else:
            return np.zeros_like(x)

    def shear_array(self, x):
        if self.type == "point":
            return np.where(x < self.L/2, self.P / 2, -self.P / 2)
        elif self.type == "uniform":
            return self.P * (0.5 - x / self.L)
        elif self.type == "moment":
            return np.zeros_like(x)
        else:
            return np.zeros_like(x)


