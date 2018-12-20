from haus import *
from straße import *
from gewerbliches_gebaeude import *
from polizeiwache import *

import random


class zellulaererAutomat:

    def __init__(self, breite, hoehe):
        """
        Input:
            breite: Breite des Automats
            hoehe : Höhe des Automats
            anzahlEinbrecher : Anzahl der Einbrecher
            anzahlMobilePolizei : Anzahl mobiler Einheiten der Polizei
        """
        self.breite = breite
        self.hoehe = hoehe

        #initialisieren der Matrix
        self.Matrix = [[0 for x in range(hoehe)] for y in range(breite)]     
        for i in range(hoehe):
            for j in range(breite):
                #Straßen
                if (i % 6 == 0 or j % 6 == 0):
                    self.Matrix[i][j] = straße()
                else:
                    r = random.randrange(0,100)
                    if(r < 50):
                        self.Matrix[i][j] = haus()
                    elif(r < 99):
                        self.Matrix[i][j] = gewerbliches_gebaeude()
                    elif(r == 99):
                        self.Matrix[i][j] = polizeistation()
                

        #Erreichbarkeit,PolizeiDistanz berechnen
        for i in range(hoehe):
            for j in range(breite):
                if (self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache"):
                    #Erreichbarkeit
                    straßen = 0
                    dist = 2
                    for x in range(-dist,dist + 1):
                        for y in range(-dist,dist + 1):
                            if (self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() == "straße"):
                                straßen += 1/dist
                    if (straßen == 5):
                        self.Matrix[i][j].setErreichbarkeit(2)
                    elif (straßen >= 3):
                        self.Matrix[i][j].setErreichbarkeit(1)
                    else:
                        self.Matrix[i][j].setErreichbarkeit(0)
                    #Polizweidistanz
                    dist = 10
                    entfernungWache = dist
                    for x in range(-dist,dist + 1):
                        for y in range(-dist,dist + 1):
                            if (self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() == "polizeiweache"):
                                if (sqrt(abs(x) + abs(y) < entfernungWache)):
                                    entfernungwache = sqrt(abs(x) + abs(y))
                    self.Matrix[i][j].setPolizeiwachenEntfernung(entfernungWache)

        
        #akteure platzieren
        #einbrecher
        self.einbrecher = [(0,0) for x in range(anzahlEinbrecher)]
        for e in range(anzahlEinbrecher):
            xRand = random.randrange(0, breite)
            yRand = random.randrange(0, hoehe)
            self.einbrecher[e] = (xRand, yRand)

        #mobile Polizei
        self.mobilePolizei = [(0,0) for x in range(anzahlMobilePolizei)]
        for p in range(anzahlMobilePolizei):
            xRand = random.randrange(0, breite)
            yRand = random.randrange(0, hoehe)
            self.mobilePolizei[p] = (xRand, yRand)
            
                    

    def step(self):
        #polizeimobil entfernung
        for i in range(hoehe):
            for j in range(breite):
                if (self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache"):
                    #Polizweidistanz
                    entfernungWache = 10
                    dist = 10
                    for x in range(-dist,dist + 1):
                        for y in range(-dist,dist + 1):
                            if (self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].getTyp() == "polizeiweache"):
                                if (math.sqrt(abs(x)**2 + abs(y)**2) < entfernungWache):
                                    entfernungwache = sqrt(abs(x) + abs(y))
                    self.Matrix[i][j].setPolizeiwachenEntfernung(10)

        #update score
        for i in range(self.hoehe):
            for j in range(self.breite):
                if (self.Matrix[i][j].getTyp() != "straße" and self.Matrix[i][j].getTyp() != "polizeiwache"):
                    z = self.Matrix[i][j]
                    z.step()
                    z.updateScore()

        #akteur update/bewegung
        ###polizei
        ###randomwalk
        for i in range(self.mobilePolizei.size):
            nordsued = random.randrange(-1,2)   # -1 süd, 1 nord
            ostwest = random.randrange(-1,2)    # -1 west 1 ost
            (x,y) = self.mobilePolizei[p]
            self.mobilePolizei[p] = (x + ostwest % self.breite, y + nordsued % self.hoehe)

        ###einbrecher
        ###suche nächstes haus mit genügend hohem score
        for i in range(self.einbrecher.size):
            dist = math.sqrt(abs(self.hoehe) + abs(self.breite))
            richtungsvektor = (0,0)
            for x in range(self.hoehe):
                for y in range(self.breite):
                    if (self.Matrix[x][y].getTyp() != "straße" and self.Matrix[x][y].getTyp() != "polizeiwache"):
                        if (self.Matrix[x][y].getScore() > 10):
                            #entfernung berechnen und vergleichen
                            (a,b) = self.einbrecher[i]
                            c = (a - x) % hoehe
                            d = (b - y) % breite
                            if (dist > math.sqrt(c**2 + d**2)):
                                #normalvektor, nord-sued, west-ost
                                ns = c / abs(c)
                                wo = d / abs(d)
                                richtungsvektor = (ns, wo)
            
            #schritt in Richtung interessantes Ziel
            (x,y) = self.einbrecher[i]
            (ns, wo) = richtungsvektor
            self.einbrecher[i] = ((x + ns) % hoehe, (y + wo) % breite)
                                

            #einbruch
            if (dist == 0):
                if ( (self.Matrix[x][y].getScore() / 16) > (1-abs(random.standard_normal(0,1))) ):
                    self.Matrix[i][j].einbruch()
                    #doppelte moore nachberschaft
                    dist = 2
                    for x in range(-dist,dist + 1):
                        for y in range(-dist,dist + 1):
                            if (x != 0 and y != 0):
                                self.Matrix[(i+x) % self.hoehe][(j+y) % self.breite].updateSicherheit(dist / max(abs(x),abs(y)))
                            else:
                                self.Matrix[i][j].updateSicherheit(dist)                                                                                                                
