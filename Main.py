import Constants
import Objects
import functions
from Objects import Charge, Vector
from functions import electric_field, coloumb_formula
import numpy as np
def main(args = 0):
    print(f"che tipo di esercizio vuoi svolgere? "
          f"\n[1]: esercizi contenenti un punto P"
          f"\n[2]: esercizi contenenti molle"
          f"\n[3]: esercizi contenenti dinamica"
          f"\n[4]: esercizi contenenti cariche in posizioni particolari")
    choice = input()
    if choice == "1":
        print(f"cosa chiede l'esercizio?"
              f"\n[1]: la distanza"
              f"\n[2]: l'energia in un punto P"
              f"\n[3]: la forza in un punto P")
        question = int(input())

        print("quante cariche ci sono?")
        nQ = int(input())
        distances = []
        charges = []
        energies = []
        for i in range(nQ):
            print(f"come viene espressa la distanza tra P e Q{i}?"
                  f"\n[1] 2 punti vengono espressi"
                  f"\n[2] la distanza viene espressa"
                  f"\n[3] la relazione tra Q1, Q2 e PQ viene espressa")
            choice = input()
            if choice == "1":
                #TODO potrebbe chiedere più di  un punto, inserire for loop
                print("inserisci xp")
                x1 = float(input())
                print("inserisci xq")
                x2 = float(input())
                print("inserisci yp")
                y1 = float(input())
                print("inserisci yq")
                y2 = float(input())
                dist = functions.point_distance(x1, x2, y1, y2)
            if choice == "2":
                print("inserisci la distanza")
                dist = float(input())
            if choice == "3":
                print("inserisci la distanza tra Q1 e Q2")
                q1q2dist = float(input())
                print("inserisci la distanza tra Q1 e P")
                q1Pdist = float(input())
            distances.append(dist)
            print(f"Quanto vale la carica {i} in N/C?")
            value = input()
            if value != 0:
                charges.append(Charge(float(value)))
            print(f"quanto vale l'energia E della Q?")
            value = input()
            if value != 0:
                energies.append(Vector(float(value)))
        if len(distances) == 0:
            print("the distance is" + functions.coloumb_formula(charges[0], Charge(), 0, energies[0]))
        else:
            print("esistono distanze")
            if len(charges) != 0:
                for charge in charges:
                    energies[0] = functions.coloumb_formula(charge, Charge(), distances[0], Vector())
                    print(f"l'energia a Q{0} è {energies[0]}")
            if len(energies) != 0:
                for energy in energies:
                    charges[0] = functions.coloumb_formula(charges[0], Charge(), distances[0], Vector(energy))
                    print(f"la carica a Q{0} è {charges[0]}")
main()