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
print(monodim_force())