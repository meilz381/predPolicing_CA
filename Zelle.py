import random


class Zelle:
    
    score = 0
    t = 0

    def __init__(self):
        """
            festlegen des typs der Zelle
        """
        pass

    def setErreichbarkeit(self, value):
        self.erreichbarkeit = value

    def setPolizeiwacheEntfernung(self, value):
        self.polizeiwacheEntfernung = value

    def setPolizeiMobilEntfernung(self, value):
        self.polizeiaktivität = value

    def setRepeatRisiko(self, value):
        self.repeatRisiko = value

    def getTyp(self):
        """
        Returns:
            string: typ dieser Zelle
        """
        return self.typ

    def updateScore(self, cRepeat, cSicherheit, cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung, minScore, tag):
        """
        Input:
            cRepeat : Konstante Repeat-Risiko
            cSicherheit : Konstante Sicherheitsausstattung
            cInteresse : Konstante Interesse
            cErreichbarkeit : Konstante Erreichbarkeit
            cPolizeiAktivität : Konstante Polizeiaktivität
            cPolizeiEntfernung : Konstante Polizeiwachen-Entfernung
            minScore : minimaler Score
            tag : boolean Value ob Tag ist
        """
        self.score = minScore \
                     + cRepeat * self.repeatRisiko + cInteresse * self.interesse + cErreichbarkeit * self.erreichbarkeit \
                     - (cSicherheit * self.sicherheitsausstattung + cPolizeiAktivität * self.polizeiaktivität + cPolizeiEntfernung * self.polizeiwacheEntfernung)

    def step(self):
        self.t += 1
        if (self.repeatRisiko > 0):
            if (random.uniform(0,1) < 0.2):
                self.updateRepeatRisiko(-0.15)
        if (random.uniform(0,1) < 0.01):
            self.updateInteresse(0.1)
        if (self.t > 7):
            if (random.uniform(0,1) < 0.2):
                self.updateSicherheit(-0.15)
            
    def einbruch(self):
        self.t = 0
        self.updateInteresse(-1)

    def updateSicherheit(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert
        """
        self.sicherheitsausstattung += amount
        if self.sicherheitsausstattung >= 1:
            self.sicherheitsausstattung = 1
        elif self.sicherheitsausstattung <= 0:
            self.sicherheitsausstattung = 0

    def updateRepeatRisiko(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert(positiv)
        """
        self.repeatRisiko += amount
        if self.repeatRisiko >= 1:
            self.repeatRisiko = 1
        elif self.repeatRisiko <= 0:
            self.repeatRisiko = 0

    def updateInteresse(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert
        """
        self.interesse += amount
        if self.interesse >= 1:
            self.interesse = 1
        elif self.interesse <= 0:
            self.interesse = 0

    def updateSicherheit(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert
        """
        self.sicherheitsausstattung += amount
        if self.sicherheitsausstattung >= 1:
            self.sicherheitsausstattung = 1
        elif self.sicherheitsausstattung <= 0:
            self.sicherheitsausstattung = 0
            
    def getScore(self):
        return self.score
