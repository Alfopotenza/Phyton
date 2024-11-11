from pyarrow.compute import scalar
import numpy as np

class Vector:
    module = 0.0
    direction = 0
    towards = 0 #1: right, 2: up, -1: left, -2: down
    def __init__(self, module = 0.0, direction = 0, towards = 0):
        self.module = module
        self.direction = direction
        self.towards = towards
    def __mul__(self, scalar):
        return self.module * scalar
    def __truediv__(self, other):
        return self.module / other
    def get_comp(self, angle):
        self.calc_dir(angle)
        return Vector(self.module * np.cos(np.deg2rad(angle)), self.direction - angle, self.towards)
    def calc_dir(self, angle):
        if self.direction - angle < 0: self.direction = self.direction + 360 - angle
        if self.direction + angle > 360: self.direction = self.direction - 360 + angle

class Charge:
    charge = 0
    mass = 0.0
    pos_x, pos_y = 0, 0
    def __init__(self, charge = 0, mass = 0.0, pos_x = 0, pos_y = 0):
        self.charge = charge
        self.mass = mass
        self.pos_x, self.pos_y = pos_x, pos_y
    def weight(self):
        return Vector(self.mass * 9.81, 270, -2)


