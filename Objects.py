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

