from pyarrow.compute import scalar
import numpy as np
from enum import Enum, IntEnum


couloumb_constant = 8.99*(10**9)
epsilon = 8.854187e-12
pi = 3.1415
proton_mass = 1.67262192 * (10**-27)
proton_charge = 1.602 * (10**-19)
electron_mass = 9.10938327 * (10**-31)
electron_charge = 1.60217663 * (10**-19)
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
    def __iter__(self):
        return self.module
    def get_comp(self, angle):
        self.calc_dir(angle)
        return Vector(self.module * np.cos(np.deg2rad(angle)), self.direction - angle, self.towards)
    def calc_dir(self, angle):
        if self.direction - angle < 0: self.direction = self.direction + 360 - angle
        if self.direction + angle > 360: self.direction = self.direction - 360 + angle

    def fix_dir(self, point_x, charge):
        pos_x = charge.variabili.get("pos_x")
        if (type(charge) != Lastra) and (type(charge) != Filo):
            q = charge.variabili.get("q")
            if (q<0 and pos_x < point_x) or (q>0 and pos_x > point_x):
                self.module = -np.abs(self.module)
                return
        else:
            density = charge.variabili.get("density")
            if density < 0:
                self.module = -np.abs(self.module)
                return

class CampoElettrico:
    def __init__(self, formula, **kwargs):
        self.formula = formula
        self.variabili = {k: v for k, v in kwargs.items() if v is not None}
        self.incognita = [k for k, v in kwargs.items() if v is None]

    def calcola(self, pos_x = 0):
        variabili = self.variabili
        incognita = self.incognita

        incognita = incognita[0]
        return self.formula(incognita)

class CaricaGenerica(CampoElettrico):
    def __init__(self, k, **kwargs):
        super().__init__(self.formula, **kwargs)
        self.k = k
    def add_dist(self, dist):
        self.variabili.update({"r": dist})
    def formula(self, incognita):
        q = self.variabili.get("q")
        r = self.variabili.get("r")
        e = self.variabili.get("e")

        if incognita == "e":
            return {"e": self.k * q / r**2}
        if incognita == "r":
            return {"r":(self.k * q / e)**0.5}
        if incognita == "q":
            return {"q": e * r**2 / self.k}

class Lastra(CampoElettrico):
    def __init__(self, epsilon_0, **kwargs):
        super().__init__(self.formula, **kwargs)
        self.epsilon_0 = epsilon_0
    def formula(self, incognita):
        density = self.variabili.get("density")
        e = self.variabili.get("e")
        if incognita == "e":
            return {"e": density / (2 * self.epsilon_0)}
        if incognita == "density":
            return {"density": e * 2 * self.epsilon_0}
class Filo(CampoElettrico):
    def __init__(self, epsilon_0, pi, **kwargs):
        super().__init__(self.formula, **kwargs)
        self.pi = pi
        self.epsilon_0 = epsilon_0
    def add_dist(self, dist):
        self.variabili.update({"r": dist})
    def formula(self, incognita):
        e = self.variabili.get("e")
        r = self.variabili.get("r")
        density = self.variabili.get("density")
        print("e, r, d:", e, r, density)
        if incognita == "e":
            return {"e": np.abs(density) / (2 * self.pi * self.epsilon_0 * r)}
        if incognita == "r":
            return {"r": np.abs(density) / (e * (2 * self.pi * self.epsilon_0))}
        if incognita == "density":
            return {"density": e * (2 * self.pi * self.epsilon_0 * r)}
class Sfera(CampoElettrico):
    def __init__(self, k, **kwargs):
        super().__init__(self.formula, **kwargs)
        self.k = k
    def add_dist(self, dist):
        self.variabili.update({"d": dist})
    def formula(self, incognita):
        e = self.variabili.get("e")
        r = self.variabili.get("r")
        d = self.variabili.get("d")
        q = self.variabili.get("q")
        if d < r:
            print("sfera interna")
            if incognita == "e":
                return {"e": (self.k * q * d)/(r**3)}
            if incognita == "r":
                return {"r": ((self.k * q * d)/e)**1/3}
            if incognita == "d":
                return {"d": e*(r**3)/(self.k*q)}
            if incognita == "q":
                return {"q": e*(r**3)/(self.k*d)}
        elif d >= r:
            print("sfera esterna")
            if incognita == "e":
                return {"e": self.k * q / d ** 2}
            if incognita == "d":
                return {"d": (self.k * q / e) ** 0.5}
            if incognita == "q":
                return {"q": e * d ** 2 / self.k}






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

class Sheet(Charge):
    density = 0
    def __init__(self, charge=0, mass=0, pos_x=0, pos_y=0, density=0):
        super().__init__(charge, mass, pos_x, pos_y)
        self.density = density
class Wire(Charge):
    density = 0
    def __init__(self, charge=0, mass=0, pos_x=0, pos_y=0, density=0):
        super().__init__(charge, mass, pos_x, pos_y)
        self.density = density
class Sphere(Charge):
    radius = 0
    def __init__(self, charge=0, mass=0, pos_x=0, pos_y=0, radius=0):
        super().__init__(charge, mass, pos_x, pos_y)
        self.radius = radius

import functions
from Objects import *
from functions import *
import numpy as np
import scipy.optimize as opt
def calc_vector_for_charge(v = Vector(), c = Charge(), d:float = 0):
    v.module = coloumb_formula(c.charge, d, Vector())

def create_sheet():
    print("densità?")
    sigma = input()
    try: sigma = float(sigma)
    except ValueError: sigma = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    sigma = float(sigma) if type(sigma) == float else None
    e = float(e) if type(e) == float else None
    return Lastra(Constants.epsilon, **{"density": sigma, "e": e})
def create_wire():
    print("densità?")
    density = input()
    try: density = float(density)
    except ValueError: density = None
    print("posizione x?")
    pos_x = input()
    try: pos_x = float(pos_x)
    except ValueError: pos_x = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    return Filo(Constants.epsilon, 3.14, **{"density": density, "pos_x": pos_x, "e": e})
def create_generic():
    print("Carica?")
    charge = float(input())
    try: charge = float(charge)
    except ValueError: charge = None
    print("posizione x?")
    pos_x = float(input())
    try: pos_x = float(pos_x)
    except ValueError: pos_x = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    return CaricaGenerica(Constants.couloumb_constant, **{"q": charge, "pos_x": pos_x, "e": e})
def create_sphere():
    print("raggio sfera?")
    r = float(input())
    try: r = float(r)
    except ValueError: r = None
    print("posizione x?")
    pos_x = float(input())
    try: pos_x = float(pos_x)
    except ValueError: pos_x = None
    print("carica?")
    charge = float(input())
    try: charge = float(charge)
    except ValueError: charge = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    return Sfera(Constants.couloumb_constant, **{"q": charge, "pos_x": pos_x, "e": e, "r": r})


def monodim_force():
    print("quante cariche ci sono?")
    iters = int(input())
    charges = []
    for i in range(iters):
        print("che tipo di carica è? \n[1]: Lastra \n[2]: Filo \n[3]: Sfera \n[4]: carica generica")
        choice = int(input())
        if choice == 1: charges.append(create_sheet())
        elif choice == 2: charges.append(create_wire())
        elif choice == 3: charges.append(create_sphere())
        elif choice == 4: charges.append(create_generic())
    return calc_forces(charges)


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


def calc_forces(charges:[Charge()]):
    print(charges)
    print("vuoi trovare \n[1] E \n[2] dist data dall'equilibrio")
    choice = int(input())
    if choice == 1:
        print("posizione x del punto?")
        x_pos = float(input())
        # creo una lista di forze
        forces = []
        # per ogni oggetto Carica()
        for charge in charges:
            #calcolo la distanza dal punto
            if type(charge) != Lastra:
                dist = axis_distance(x_pos, charge.variabili.get("pos_x"))
                charge.add_dist(dist)
            #se la distanza E la carica sono fornite
            incognita = charge.calcola()
            print(incognita)
            if incognita == {"e": incognita["e"]}:
                e_force = Vector(incognita["e"])
                e_force.fix_dir(x_pos, charge)
                forces.append(e_force)
            else:
                return incognita
        #calcolo la forza totale
        return total_e(forces)
    '''if choice == 2:
        r_eq = calc_equilibrio(charges[0], charges[1], variabile = "r")
        return r_eq'''

'''def calc_equilibrio(entita1, entita2, variabile = "r", tol = 1e-12, maxiter= 100):
    def field_difference(value):
        entita1.variabili[variabile] = value
        entita2.variabili[variabile] = value

        e1 = entita1.calcola()
        e2 = entita2.calcola()

        return e1 - e2

    stima_iniziale = 1 if variabile in ["r", "q", "density"] else 0

    lowlim = 1e-12
    highlim = 1e3

    try:
        result = opt.newton(
            field_difference, stima_iniziale, tol = tol, maxiter = maxiter)
        return result
    except RuntimeError as e:
        print(f"metodo Newton non funzionante: {e} Provo Brent")
        try:
            result = opt.brentq(field_difference, lowlim, highlim, xtol = tol)
            return result
        except ValueError as e:
            print(f"Brent fallito. {e}. Non c'è soluzione")
        return None
    except Exception as e:
        print(f"errore generico: {e}")
        return None'''
while True:
    print(monodim_force())

