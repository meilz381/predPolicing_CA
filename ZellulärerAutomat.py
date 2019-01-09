from Haus import *
from Straße import *
from GewerblichesGebäude import *
from Polizeiwache import *

import random
import math
import time
import numpy as np
import numba
from numba import jit


class ZellulärerAutomat:

    def __init__(self, breite, hoehe, anzahlEinbrecher, anzahlMobilePolizei,
                 cRepeat, cSicherheit, cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung, minScore, rangeScore):
        """
        Input:
            breite: Breite des Automats
            hoehe : Höhe des Automats
            anzahlEinbrecher : Anzahl der Einbrecher
            anzahlMobilePolizei : Anzahl mobiler Einheiten der Polizei
            cRepeat : Konstante Repeat-Risiko
            cSicherheit : Konstante Sicherheitsausstattung
            cInteresse : Konstante Interesse
            cErreichbarkeit : Konstante Erreichbarkeit
            cPolizeiAktivität : Konstante Polizeiaktivität
            cPolizeiEntfernung : Konstante Polizeiwachen-Entfernung
            minScore : minimaler Score
            rangeScore : Spanne des Scores
        """

        self.breite = breite
        self.hoehe = hoehe
        self.anzahlEinbrecher = anzahlEinbrecher
        self.anzahlMobilePolizei = anzahlMobilePolizei
        self.cRepeat = cRepeat
        self.cSicherheit = cSicherheit
        self.cInteresse = cInteresse
        self.cErreichbarkeit = cErreichbarkeit
        self.cPolizeiAktivität = cPolizeiAktivität
        self.cPolizeiEntfernung = cPolizeiEntfernung
        self.minScore = minScore
        self.rangeScore = rangeScore

        self.tag = True

        random.seed()

        # initialisieren der Matrix
        self.Matrix = [[0 for x in range(hoehe)] for y in range(breite)]     
        for i in range(hoehe):
            for j in range(breite):
                # Straßen
                if i % 6 == 0 or j % 6 == 0:
                    self.Matrix[i][j] = Straße()
                else:
                    r = random.randrange(0, 500)
                    if r < 250:
                        self.Matrix[i][j] = Haus()
                    elif r < 499:
                        self.Matrix[i][j] = GewerblichesGebäude()
                    elif r == 499:
                        self.Matrix[i][j] = Polizeiwache()

        # Erreichbarkeit,PolizeiDistanz berechnen
        for i in range(hoehe):
            for j in range(breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    # Erreichbarkeit
                    straßen = 0
                    dist = 2
                    for x in range(-dist, dist + 1):
                        for y in range(-dist, dist + 1):
                            if self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() == "straße":
                                straßen += 1 / max(abs(x),abs(y))
                    if straßen == 5:
                        self.Matrix[i][j].setErreichbarkeit(1)
                    elif straßen >= 3:
                        self.Matrix[i][j].setErreichbarkeit(1/2)
                    else:
                        self.Matrix[i][j].setErreichbarkeit(0)
                    # Polizeidistanz
                    dist = 10
                    entfernungWache = dist
                    for x in range(-dist, dist + 1):
                        for y in range(-dist, dist + 1):
                            if self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() == "polizeiwache":
                                if self.distanz(x,y) < entfernungWache:
                                    entfernungWache = self.distanz(x,y)
                    self.Matrix[i][j].setPolizeiwacheEntfernung(1/ entfernungWache)
        
        # akteure platzieren
        # einbrecher
        self.einbrecher = [(0,0) for x in range(anzahlEinbrecher)]
        for e in range(anzahlEinbrecher):
            xRand = random.randrange(0, breite)
            yRand = random.randrange(0, hoehe)
            self.einbrecher[e] = (xRand, yRand)

        # mobile Polizei
        self.mobilePolizei = [(0,0) for x in range(anzahlMobilePolizei)]
        for p in range(anzahlMobilePolizei):
            xRand = random.randrange(0, breite)
            yRand = random.randrange(0, hoehe)
            self.mobilePolizei[p] = (xRand, yRand)
        print("Initialisierung beendet")

    @staticmethod
    @jit(nopython=True)
    def distanz(x, y):
        dist = math.sqrt(x**2 + y**2)
        return dist

    def step(self):
        self.tag = not self.tag


        # polizeimobil entfernung
        for i in range(self.hoehe):
            for j in range(self.breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    # Polizeidistanz
                    entfernungMobil = 10
                    for m in range(len(self.mobilePolizei)):
                        (x,y) = self.mobilePolizei[m]
                        dist = self.distanz(x, y)
                        if dist < entfernungMobil:
                            entfernungMobil = dist
                    self.Matrix[i][j].setPolizeiMobilEntfernung(1/(1 + entfernungMobil))

        # update score
        for i in range(self.hoehe):
            for j in range(self.breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    z = self.Matrix[i][j]
                    z.step()
                    z.updateScore(self.cRepeat, self.cSicherheit, self.cInteresse, self.cErreichbarkeit, self.cPolizeiAktivität, self.cPolizeiEntfernung, self.minScore, self.tag)

        # akteur update/bewegung
        ### polizei
        ### suche nächstes Haus mit kürzlichem Einbruch
        for m in range(len(self.mobilePolizei)):
            dist = 6
            interesse = 0
            (a, b) = self.mobilePolizei[m]
            for x in range(-dist, dist + 1):
                for y in range(-dist, dist + 1):
                    c = (a + x) % self.hoehe
                    d = (b + y) % self.breite
                    if self.Matrix[c][d].getTyp() != "straße" and self.Matrix[c][d].getTyp() != "polizeiwache":
                        # RCT
                        if x != 0 and y != 0:
                            if interesse < (self.distanz(x , y) / (self.Matrix[c][d].t + 1)):
                                # normalvektor, nord-süd, west-ost
                                if x != 0:
                                    ns = int(x / abs(x))
                                else:
                                    ns = int(0)
                                if y != 0:
                                    wo = int(y / abs(y))
                                else:
                                    wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = self.distanz(x , y) / (self.Matrix[c][d].t + 1)
                        else:
                            if interesse < (0.75 / (self.Matrix[c][d].t + 1)):
                                # normalvektor, nord-süd, west-ost
                                ns = int(0)
                                wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = self.Matrix[c][d].getScore()

            # Schritt in Richtung Ziel, nord-süd, west-ost
            (ns, wo) = richtungsvektor
            self.mobilePolizei[m] = ((a + ns) % self.breite, (b + wo) % self.hoehe)

        ### einbrecher
        ### suche nächstes haus
        for e in range(len(self.einbrecher)):
            dist = 6
            interesse = 0
            richtungsvektor = (0,0)
            (a,b) = self.einbrecher[e]
            for x in range(-dist, dist + 1):
                for y in range(-dist, dist + 1):
                    c = (a + x) % self.hoehe
                    d = (b + y) % self.breite
                    if self.Matrix[c][d].getTyp() != "straße" and self.Matrix[c][d].getTyp() != "polizeiwache":
                        # entfernung berechnen und vergleichen
                        # RCT
                        if x != 0 and y != 0:
                            if interesse < (self.Matrix[c][d].getScore() / self.distanz(x , y)):
                                # normalvektor, nord-süd, west-ost
                                if x != 0:
                                    ns = int(x / abs(x))
                                else:
                                    ns = int(0)
                                if y != 0:
                                    wo = int(y / abs(y))
                                else:
                                    wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = self.Matrix[c][d].getScore() / self.distanz(x , y)
                        else:
                            if interesse < (self.Matrix[c][d].getScore() / 0.75):
                                # normalvektor, nord-süd, west-ost
                                ns = int(0)
                                wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = self.Matrix[c][d].getScore() / 0.75
            
            # Schritt in Richtung Ziel, nord-süd, west-ost
            (ns, wo) = richtungsvektor
            self.einbrecher[e] = ((a + ns) % self.hoehe, (b + wo) % self.breite)

            (a,b) = self.einbrecher[e]
            # einbruch
            if richtungsvektor == (0,0) and self.Matrix[a][b].getTyp() != "straße" and self.Matrix[a][b].getTyp() != "polizeiwache":
                if (self.Matrix[a][b].getScore() / self.rangeScore) > (random.uniform()):
                    self.Matrix[a][b].einbruch()
                    # doppelte moore nachberschaft
                    dist = 2
                    for i in range(-dist, dist + 1):
                        for j in range(-dist, dist + 1):
                            c = (i + a) % self.hoehe
                            d = (j + b) % self.breite
                            z = self.Matrix[c][d]
                            x = self.distanz(i,j)
                            if z.getTyp() != "straße" and z.getTyp() != "polizeiwache":
                                if i != 0 and j != 0:
                                    # nearRepeat > TrueRepeat
                                    z.updateSicherheit(math.cos((x-1)/2))
                                    z.updateRepeatRisiko(math.cos((x-1)/2))
                                else:
                                    z.updateSicherheit(1)
                                    z.updateRepeatRisiko(math.cos((x-1)/2))
