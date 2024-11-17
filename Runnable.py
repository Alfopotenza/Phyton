import numpy as np

# Constants
class Constants:
    couloumb_constant = 8.99*(10**9)
    epsilon = 8.854187e-12
    pi = 3.1415
    proton_mass = 1.67262192 * (10**-27)
    proton_charge = 1.602 * (10**-19)
    electron_mass = 9.10938327 * (10**-31)
    electron_charge = 1.60217663 * (10**-19)

# Vector class
class Vector:
    def __init__(self, module = 0.0, direction = 0, towards = 0):
        self.module = module
        self.direction = direction
        self.towards = towards  #1: right, 2: up, -1: left, -2: down
    
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
        if self.direction - angle < 0: 
            self.direction = self.direction + 360 - angle
        if self.direction + angle > 360: 
            self.direction = self.direction - 360 + angle

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

# Base Classes
class CampoElettrico:
    def __init__(self, formula, **kwargs):
        self.formula = formula
        self.variabili = {k: v for k, v in kwargs.items() if v is not None}
        self.incognita = [k for k, v in kwargs.items() if v is None]

    def calcola(self, pos_x = 0):
        incognita = self.incognita[0]
        return self.formula(incognita)

class Charge:
    def __init__(self, charge = 0, mass = 0.0, pos_x = 0, pos_y = 0):
        self.charge = charge
        self.mass = mass
        self.pos_x, self.pos_y = pos_x, pos_y
    
    def weight(self):
        return Vector(self.mass * 9.81, 270, -2)

# Derived Classes
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
            if incognita == "e":
                return {"e": (self.k * q * d)/(r**3)}
            if incognita == "r":
                return {"r": ((self.k * q * d)/e)**(1/3)}
            if incognita == "d":
                return {"d": e*(r**3)/(self.k*q)}
            if incognita == "q":
                return {"q": e*(r**3)/(self.k*d)}
        else:
            if incognita == "e":
                return {"e": self.k * q / d ** 2}
            if incognita == "d":
                return {"d": (self.k * q / e) ** 0.5}
            if incognita == "q":
                return {"q": e * d ** 2 / self.k}

# Utility Functions
def point_distance(x1, x2, y1, y2):
    return (((x2 - x1)**2) + ((y2 - y1)**2))**0.5

def axis_distance(x1, x2):
    return np.abs(x1 - x2)

def electric_field(e=0, f=0, q=0):
    if e == 0:
        return f/q.charge
    if f == 0:
        return e * q.charge
    if q == 0:
        return f/e.module

def total_e(e):
    modules = []
    for i in e:
        print("force_n:", i.module)
        modules.append(i.module)
    return sum(modules)

def calc_triangle_sides(hypotenuse=0, cathetus=0, angle=0):
    if hypotenuse == 0:
        return cathetus/np.cos(np.deg2rad(angle))
    if angle == 0:
        return hypotenuse/cathetus
    if cathetus == 0:
        return hypotenuse * np.cos(np.deg2rad(angle))

# Input Functions
def create_sheet():
    print("densità?")
    sigma = input()
    try: sigma = float(sigma)
    except ValueError: sigma = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    sigma = float(sigma) if isinstance(sigma, float) else None
    e = float(e) if isinstance(e, float) else None
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
    return Filo(Constants.epsilon, Constants.pi, **{"density": density, "pos_x": pos_x, "e": e})

def create_generic():
    print("Carica?")
    charge = input()
    try: charge = float(charge)
    except ValueError: charge = None
    print("posizione x?")
    pos_x = input()
    try: pos_x = float(pos_x)
    except ValueError: pos_x = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    return CaricaGenerica(Constants.couloumb_constant, **{"q": charge, "pos_x": pos_x, "e": e})

def create_sphere():
    print("raggio sfera?")
    r = input()
    try: r = float(r)
    except ValueError: r = None
    print("posizione x?")
    pos_x = input()
    try: pos_x = float(pos_x)
    except ValueError: pos_x = None
    print("carica?")
    charge = input()
    try: charge = float(charge)
    except ValueError: charge = None
    print("campo elettrico?")
    e = input()
    try: e = float(e)
    except ValueError: e = None
    return Sfera(Constants.couloumb_constant, **{"q": charge, "pos_x": pos_x, "e": e, "r": r})

def monodim_force():
    print("quante cariche ci sono?")
    try:
        iters = int(input())
    except ValueError:
        print("Inserire un numero valido")
        return
    
    charges = []
    for i in range(iters):
        print("che tipo di carica è? \n[1]: Lastra \n[2]: Filo \n[3]: Sfera \n[4]: carica generica")
        try:
            choice = int(input())
        except ValueError:
            print("Scelta non valida")
            continue
            
        if choice == 1: charges.append(create_sheet())
        elif choice == 2: charges.append(create_wire())
        elif choice == 3: charges.append(create_sphere())
        elif choice == 4: charges.append(create_generic())
    return calc_forces(charges)

def calc_forces(charges):
    print("Cariche:", charges)
    print("vuoi trovare \n[1] E \n[2] dist data dall'equilibrio")
    try:
        choice = int(input())
    except ValueError:
        print("Scelta non valida")
        return
        
    if choice == 1:
        print("posizione x del punto?")
        try:
            x_pos = float(input())
        except ValueError:
            print("Posizione non valida")
            return
            
        forces = []
        for charge in charges:
            if type(charge) != Lastra:
                dist = axis_distance(x_pos, charge.variabili.get("pos_x"))
                charge.add_dist(dist)
            incognita = charge.calcola()
            print("Incognita:", incognita)
            if incognita == {"e": incognita["e"]}:
                e_force = Vector(incognita["e"])
                e_force.fix_dir(x_pos, charge)
                forces.append(e_force)
            else:
                return incognita
        return total_e(forces)

if __name__ == "__main__":
    print(monodim_force())
