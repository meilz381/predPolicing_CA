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

    def __init__(self, breite, hoehe, anzahlMobilePolizei, anzahlEinbrecher,
                 cRepeat, cSicherheit, cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung,
                 cBewohner, cTagDauer,
                 cAttraktivitaetDistanzEinbrecher, cAttraktivitaetDistanzPolizei,
                 cSichtreichweiteEinbrecher, cSichtreichweitePolizei, cReichweiteEinbruch,
                 minScore, rangeScore):
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
            cBewohner : Konstante Bewohner
            cTagDauer : Länge eines Tages
            cAttraktivitaetDistanzEinbrecher : Stärke der Berücksichtigung in Attraktivitätsberechnung
            cAttraktivitaetDistanzPolizei : Stärke der Berücksichtigung in Attraktivitätsberechnung
            cSichtreichweiteEinbrecher :  Sichtreichweite der Einbrecher
            cSichtreichweitePolizei : Sichtreichweite der Polizei
            cReichweiteEinbruch : Auswirkungsreichweite von Einbrüchen
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
        self.cBewohner = cBewohner

        self.cTagDauer = cTagDauer

        self.cAttraktivitaetDistanzEinbrecher = cAttraktivitaetDistanzEinbrecher
        self.cAttraktivitaetDistanzPolizei = cAttraktivitaetDistanzPolizei

        self.cSichtreichweiteEinbrecher = cSichtreichweiteEinbrecher
        self.cSichtreichweitePolizei = cSichtreichweitePolizei
        self.cReichweiteEinbruch = cReichweiteEinbruch

        self.minScore = minScore
        self.rangeScore = rangeScore

        self.tag = 0

        random.seed()

        # initialisieren der Matrix
        self.Matrix = [[0 for x in range(hoehe)] for y in range(breite)]

        toggle = -1  # haus = -1, gewerbe = 1
        sizeBigTiles = 6
        countBigTilesHoehe = int(hoehe / sizeBigTiles)
        countBigTilesBreite = int(breite / sizeBigTiles)

        streak = 0
        for i in range(countBigTilesHoehe):
            for j in range(countBigTilesBreite):
                change = math.exp(-(0.15 * (streak - 12)) ** 2)
                stay = math.exp(-(0.15 * (streak)) ** 2)
                value = random.uniform(0, 1) * stay - random.uniform(0, 1) * change
                # stay
                if value >= 0:
                    streak += 1
                else:
                    streak = 0
                    toggle = toggle * (-1)

                for x in range(sizeBigTiles):
                    for y in range(sizeBigTiles):
                        if (x % 6 != 0) and (y % 6 != 0):
                            if (random.uniform(0,1) > 0.0005):
                                if toggle == -1:
                                    self.Matrix[i * sizeBigTiles + x][j * sizeBigTiles + y] = Haus()
                                else:
                                    self.Matrix[i * sizeBigTiles + x][j * sizeBigTiles + y] = GewerblichesGebäude()
                            else:
                                self.Matrix[i * sizeBigTiles + x][j * sizeBigTiles + y] = Polizeiwache()
                        else:
                            self.Matrix[i * sizeBigTiles + x][j * sizeBigTiles + y] = Straße()

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
                    if straßen >= 5:
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

        self.sicherheitsgesetz = 0

        print("Initialisierung beendet")

    @staticmethod
    @jit(nopython=True)
    def distanz(x, y):
        #dist = math.sqrt(x**2 + y**2)
        dist = max(abs(x), abs(y))
        return dist

    # Zentrale Funktion des Zelluläreren Automaten
    def step(self):
        self.tag = (self.tag + 1) % self.cTagDauer

        # gesetzte
        if (self.tag % self.cTagDauer == 0):
            sum = 0
            for i in range(self.hoehe):
                for j in range(self.breite):
                    sum += self.Matrix[i][j].score
            average = (sum / (self.hoehe * self.breite)) / self.rangeScore
            if average > 3/4:
                print("da")
                self.sicherheitsgesetz = 3
            elif average > 1/2:
                print ("hier")
                self.sicherheitsgesetz = 1.5
            else:
                self.sicherheitsgesetz = 0

        # polizeimobil entfernung
        for i in range(self.hoehe):
            for j in range(self.breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    # Polizeidistanz
                    entfernungMobil = 10
                    for m in range(len(self.mobilePolizei)):
                        (x,y) = self.mobilePolizei[m]
                        min_ns = min((i - x) % self.hoehe, (x - i) % self.hoehe)
                        min_wo = min((j - y) % self.breite, (y - j) % self.breite)
                        dist = self.distanz(min_ns, min_wo)
                        if dist < entfernungMobil:
                            entfernungMobil = dist
                    self.Matrix[i][j].setPolizeiMobilEntfernung(1/(1 + entfernungMobil * self.cAttraktivitaetDistanzPolizei))

        # update score
        for i in range(self.hoehe):
            for j in range(self.breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    z = self.Matrix[i][j]
                    z.step()
                    z.updateScore(self.cRepeat, self.cSicherheit + self.sicherheitsgesetz, self.cInteresse, self.cErreichbarkeit,
                                  self.cPolizeiAktivität, self.cPolizeiEntfernung, self.cBewohner, self.cTagDauer,
                                  self.tag, self.minScore)

        # akteur update/bewegung
        ### polizei
        ### suche nächstes Haus mit kürzlichem Einbruch
        for m in range(len(self.mobilePolizei)):
            dist = self.cSichtreichweitePolizei
            interesse = 0
            (a, b) = self.mobilePolizei[m]
            for x in range(-dist, dist + 1):
                for y in range(-dist, dist + 1):
                    c = (a + x) % self.hoehe
                    d = (b + y) % self.breite
                    if self.Matrix[c][d].getTyp() != "straße" and self.Matrix[c][d].getTyp() != "polizeiwache":
                        # RCT
                        if (self.distanz(x, y) != 0):
                            if interesse < (1 / (0.01 + (self.Matrix[c][d].t) - (self.distanz(x , y) * self.cAttraktivitaetDistanzPolizei))):

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
                                interesse = 1 / (0.01 + (self.Matrix[c][d].t ) - (self.distanz(x , y) * self.cAttraktivitaetDistanzPolizei))
                        else:
                            if interesse < (1 / (0.01 + (self.Matrix[c][d].t))):
                                # normalvektor, nord-süd, west-ost
                                ns = int(0)
                                wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = 1 / (0.01 + (self.Matrix[c][d].t))

            # Schritt in Richtung Ziel, nord-süd, west-ost
            (ns, wo) = richtungsvektor
            self.mobilePolizei[m] = ((a + ns) % self.breite, (b + wo) % self.hoehe)

        ### einbrecher
        ### suche nächstes haus
        for e in range(len(self.einbrecher)):
            dist = self.cSichtreichweiteEinbrecher
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
                        if (self.distanz(x, y) != 0):
                            if interesse < (self.Matrix[c][d].getScore() - (self.distanz(x , y) * self.cAttraktivitaetDistanzEinbrecher)):
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
                                interesse = self.Matrix[c][d].getScore() - (self.distanz(x , y) * self.cAttraktivitaetDistanzEinbrecher)
                        else:
                            if interesse < (self.Matrix[c][d].getScore()):
                                # normalvektor, nord-süd, west-ost
                                ns = int(0)
                                wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = self.Matrix[c][d].getScore()
            
            # Schritt in Richtung Ziel, nord-süd, west-ost
            (ns, wo) = richtungsvektor
            self.einbrecher[e] = ((a + ns) % self.hoehe, (b + wo) % self.breite)

            (a,b) = self.einbrecher[e]
            # einbruch
            if richtungsvektor == (0,0) and self.Matrix[a][b].getTyp() != "straße" and self.Matrix[a][b].getTyp() != "polizeiwache":
                if (self.Matrix[a][b].getScore() / self.rangeScore) > (random.uniform(0,1)):
                    self.Matrix[a][b].einbruch()
                    dist = self.cReichweiteEinbruch
                    for i in range(-dist, dist + 1):
                        for j in range(-dist, dist + 1):
                            c = (i + a) % self.hoehe
                            d = (j + b) % self.breite
                            z = self.Matrix[c][d]
                            x = self.distanz(i,j)
                            if z.getTyp() != "straße" and z.getTyp() != "polizeiwache":
                                if i != 0 and j != 0:
                                    z.updateSicherheit(math.cos(x * math.pi/(2 * dist)))
                                    z.updateRepeatRisiko(math.cos(x * math.pi/(2 * dist)))
                                else:
                                    z.updateSicherheit(1)
                                    z.updateRepeatRisiko(math.cos(x * math.pi/(2 * dist)))

