import numpy as np
import Constants as const

from Objects import *
import Constants
def point_distance(x1, x2, y1, y2) -> float:
    return (((x2 - x1)**2) + ((y2 - y1)**2))**0.5
def axis_distance(x1, x2):
    return np.abs(x1 - x2)

def electric_field(e:Vector = 0, f:Vector = 0, q:Charge = 0) -> Vector:
    if e.module == 0:
        return f/q.charge
    if f.module == 0:
        return e * q.charge
    if q == 0:
        return f/e.module
def sheet_electric_field(density:float = 0, e:Vector = 0):
    if e.module == 0:
        return np.abs(density)/(2*Constants.epsilon)
    if density == 0:
        return e.module * (2*Constants.epsilon)
def wire_electric_field(density:float = 0, d:float = 0, e:Vector() = 0):
    if e.module == 0:
        return np.abs(density)/(2*Constants.pi * Constants.epsilon * d)
    if density == 0:
        return e.module * (2*Constants.pi * Constants.epsilon * d)
    if d == 0:
        return density/(e.module * (2*Constants.pi * Constants.epsilon))
#LA SFERA ESTERNA USA LA FORMULA GENERICA DEL CAMPO ELETTRICO
def inner_sphere(e:Vector() = 0, q:Charge() = 0, d:float = 0, r:float = 0):
    if e.module == 0:
        return (Constants.couloumb_constant * q.charge * d)/(r**3)
    if q == 0:
        return (e*(r**3))/(Constants.couloumb_constant * d)
    if d == 0:
        return (e*(r**3))/(Constants.couloumb_constant * q.charge)
    if r == 0:
        return ((Constants.couloumb_constant * q.charge * d)/e.module)**(1/3)

def coloumb_formula(q1:Charge = 0, d:float = 0, e:Vector = 0):
    if e.module == 0:
        return (Constants.couloumb_constant * np.abs(q1.charge)) / (d**2)
    if d == 0:
        return ((Constants.couloumb_constant * np.abs(q1.charge)) / e.module)**0.5

def balance(fx:Vector = 1, fy:Vector = 1, fp:Vector = 1, angle = 0) -> Vector:
    if fy.module == 0:
        fy.module = -fp.module(angle)
        return fy
    if fx.module == 0:
        fx.module = -fp.module(angle)
        return fx

def equal_forces(q1:Charge() = Charge(2e-9), q2:Charge = Charge(-3e-9), x:float = 4):
    q2.charge = np.abs(q2.charge)
    num = (q1.charge * x) + (x * np.sqrt(np.abs(q1.charge*q2.charge)))
    den = q1.charge - q2.charge
    return num/den
equal_forces()
def hooke_law(f:Vector, s:float, k:float):
    if s == 0:
        return -f/k

def total_e(e:[Vector]):
    modules = []
    for i in e:
        print(f"force_n: {i.module}")
        modules.append(i.module)
    return sum(modules)
def calc_triangle_sides(hypotenuse:float = 0, cathetus:float = 0, angle:int = 0):
    if hypotenuse == 0:
        return cathetus/np.cos(np.deg2rad(angle))
    if angle == 0:
        return hypotenuse/cathetus
    if cathetus == 0:
        return hypotenuse * np.cos(np.deg2rad(angle))