import numpy as np

import Objects
import Constants
def point_distance(x1, x2, y1, y2) -> float:
    return (((x2 - x1)**2) + ((y2 - y1)**2))**0.5

def electric_field(e:Objects.Vector = 0, f:Objects.Vector = 0, q:Objects.Charge = 0) -> Objects.Vector:
    if e.module == 0:
        return f/q.charge
    if f.module == 0:
        return e * q.charge
    if q == 0:
        return f/e.module

def coloumb_formula(q1:Objects.Charge = 0, q2:Objects.Charge = 0, d:float = 0, e:Objects.Vector = 0):
    if e.module == 0:
        return (Constants.couloumb_constant * np.abs(q1.charge)) / (d**2)
    if d == 0:
        return ((Constants.couloumb_constant * np.abs(q1.charge)) / e.module)**0.5
    if (q2.charge == 0) and e.module != 0 and d != 0:
        return (e.module * (d**2)) / Constants.couloumb_constant

def balance(fx:Objects.Vector = 1, fy:Objects.Vector = 1, fp:Objects.Vector = 1, angle = 0) -> Objects.Vector:
    if fy.module == 0:
        fy.module = -fp.module(angle)
        return fy
    if fx.module == 0:
        fx.module = -fp.module(angle)
        return fx

def hooke_law(f:Objects.Vector, s:float, k:float):
    if s == 0:
        return -f/k

def total_e(e:[Objects.Vector]):
    for vector in range(len(e)):
        if vector >= 1:
            if (e[vector].direction == e[vector - 1].direction) and (e[vector].towards == -e[vector-1].towards):
                return e[vector].module + e[vector - 1].module
def calc_triangle_sides(hypotenuse:float = 0, cathetus:float = 0, angle:int = 0):
    if hypotenuse == 0:
        return cathetus/np.cos(np.deg2rad(angle))
    if angle == 0:
        return hypotenuse/cathetus
    if cathetus == 0:
        return hypotenuse * np.cos(np.deg2rad(angle))