from Haus import *
from Straße import *
from GewerblichesGebäude import *
from Polizeiwache import *

import random
import math


class ZellulärerAutomat:

    def __init__(self, breite, hoehe, anzahlEinbrecher, anzahlMobilePolizei,
                 cRepeat, cSicherheit, cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung):
        """
        Input:
            breite: Breite des Automats
            hoehe : Höhe des Automats
            anzahlEinbrecher : Anzahl der Einbrecher
            anzahlMobilePolizei : Anzahl mobiler Einheiten der Polizei
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

        # initialisieren der Matrix
        self.Matrix = [[0 for x in range(hoehe)] for y in range(breite)]     
        for i in range(hoehe):
            for j in range(breite):
                # Straßen
                if i % 6 == 0 or j % 6 == 0:
                    self.Matrix[i][j] = Straße()
                else:
                    r = random.randrange(0, 100)
                    if r < 50:
                        self.Matrix[i][j] = Haus()
                    elif r < 99:
                        self.Matrix[i][j] = GewerblichesGebäude()
                    elif r == 99:
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
                                if math.sqrt(abs(x) + abs(y)) < entfernungWache:
                                    entfernungWache = math.sqrt(abs(x) + abs(y))
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

    def step(self):
        # polizeimobil entfernung
        for i in range(self.hoehe):
            for j in range(self.breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    # Polizeidistanz
                    entfernungMobil = 10
                    for m in range(len(self.mobilePolizei)):
                        (x,y) = self.mobilePolizei[m]
                        if math.sqrt(abs(x)**2 + abs(y)**2) < entfernungMobil:
                            entfernungMobil = math.sqrt(abs(x) + abs(y))
                    self.Matrix[i][j].setPolizeiMobilEntfernung(1/entfernungMobil)

        # update score
        for i in range(self.hoehe):
            for j in range(self.breite):
                if self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache":
                    z = self.Matrix[i][j]
                    z.step()
                    z.updateScore(self.cRepeat, self.cSicherheit, self.cInteresse, self.cErreichbarkeit, self.cPolizeiAktivität, self.cPolizeiEntfernung)
                    
        # akteur update/bewegung
        ### polizei
        ### randomwalk
        for m in range(len(self.mobilePolizei)):
            nordsued = random.randrange(-1,2)   # -1 süd, 1 nord
            ostwest = random.randrange(-1,2)    # -1 west 1 ost
            (x,y) = self.mobilePolizei[m]
            self.mobilePolizei[m] = (x + ostwest % self.breite, y + nordsued % self.hoehe)

        ### einbrecher
        ### suche nächstes haus
        for e in range(len(self.einbrecher)):
            dist = 6
            interesse = 0
            richtungsvektor = (0,0)
            (a,b) = self.einbrecher[e]
            for x in range(-dist, dist + 1):
                for y in range(-dist, dist + 1):
                    if self.Matrix[(a + x) % self.hoehe][(b + y) % self.breite].getTyp() != "straße" and self.Matrix[(a + x) % self.hoehe][(b + y) % self.breite].getTyp() != "polizeiwache":
                        if self.Matrix[(a + x) % self.hoehe][(b + y) % self.breite].getScore() > 10:
                            # entfernung berechnen und vergleichen
                            c = (a + x) % self.hoehe
                            d = (b + y) % self.breite
                            # RCT
                            if interesse < (self.Matrix[c][d].getScore() / math.sqrt(c**2 + d**2)):
                                # normalvektor, nord-sued, west-ost
                                if c != 0:
                                    ns = int(c / abs(c))
                                else:
                                    ns = int(0)
                                if d != 0:
                                    wo = int(d / abs(d))
                                else:
                                    wo = int(0)
                                richtungsvektor = (ns, wo)
                                interesse = self.Matrix[c][d].getScore() / math.sqrt(c**2 + d**2)
            
            # Schritt in Richtung Ziel
            (x,y) = self.einbrecher[e]
            (ns, wo) = richtungsvektor
            self.einbrecher[e] = ((x + ns) % self.hoehe, (y + wo) % self.breite)
                                
            ####xy ij fehler
            # einbruch
            if richtungsvektor == (0,0) and self.Matrix[x][y].getTyp() != "straße" and self.Matrix[x][y].getTyp() != "polizeiwache":
                # 16 max von score
                if (self.Matrix[x][y].getScore() / 14) > (abs(random.gauss(0,1))):
                    self.Matrix[x][y].einbruch()
                    # doppelte moore nachberschaft
                    dist = 2
                    for i in range(-dist,dist + 1):
                        for j in range(-dist,dist + 1):
                            if self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() != "straße" and self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() != "polizeiwache":
                                if x != 0 and y != 0:
                                    # nearRepeat > TrueRepeat
                                    self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].updateSicherheit(math.cos((x-1)/2))
                                    self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].updateRepeatRisiko(math.cos((x-1)/2))
                                else:
                                    self.Matrix[i][j].updateSicherheit(1)
                                    self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].updateRepeatRisiko(math.cos((x-1)/2))

