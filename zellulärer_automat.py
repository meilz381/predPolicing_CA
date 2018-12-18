from zelle import *

import copy


class zellulaererAutomat:

    def __init__(self, breite, hoehe, theta1, theta2):
        """
        Input:
            breite: Breite des Automats
            hoehe : Höhe des Automats
            theta1: einbruchsschwellwert
            theta2: gefährdungsschwellwert
        """
        self.breite = breite
        self.hoehe = hoehe

        #initialisieren der Matrix
        self.Matrix = [[0 for x in range(hoehe)] for y in range(breite)]     
        for i in range(hoehe):
            for j in range(breite):
                #Straßen
                if (i % 6 == 0 or j % 6 == 0):
                    isHaus = False
                else:
                   isHaus = True
                self.Matrix[i][j] = zelle(theta1, theta2, isHaus)
##                self.Matrix[i][j] = zelle(theta1, theta2, true)

        #Erreichbarkeit berechnen
        for i in range(hoehe):
            for j in range(breite):
                if (self.Matrix[i][j].isHaus()):
                    straßen = 0
                    dist = 2
                    for x in range(-dist,dist + 1):
                        for y in range(-dist,dist + 1):
                            if (self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].isHaus() == False):
                                straßen += 1/dist
                    if (straßen == 5):
                        self.Matrix[i][j].setErreichbarkeit(1)
                    elif (straßen >= 3):
                        self.Matrix[i][j].setErreichbarkeit(0)
                    else:
                        self.Matrix[i][j].setErreichbarkeit(-1)

    def step(self):
        for i in range(self.hoehe):
            for j in range(self.breite):
                if (self.Matrix[i][j].isHaus() == True):
                    z = self.Matrix[i][j]
                    z.step()
                    z.updateScore()

        for i in range(self.hoehe):
            for j in range(self.breite):       
                if (z.getStatus() == "red"):
                    self.Matrix[i][j].einbruch()
                    #doppelte moore nachberschaft
                    dist = 2
                    for x in range(-dist,dist + 1):
                        for y in range(-dist,dist + 1):
                            if (x != 0 and y != 0):
                                self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].updateSicherheit(dist / max(abs(x),abs(y)))
                                self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].updatePolizeiaktivität(dist / max(abs(x),abs(y)))
                            else:
                                self.Matrix[i][j].updateSicherheit(dist)
                                self.Matrix[i][j].updatePolizeiaktivität(dist)
                                                                                                                
