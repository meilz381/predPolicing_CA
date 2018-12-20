import random

class zelle:
    
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
        self.polizeiwache_entfernung = value

    def setTrueRepeatRisiko(self, value):
        self.trueRepeatRisiko = value

    def setNearRepeatRisiko(self, value):
        self.nearRepeatRisiko = value

    def getTyp(self):
        """
        Returns:
            string: typ dieser Zelle
        """
        return self.typ

    def updateScore(self):
        #max 16
        #2 + 3 + 3 + 3 + 2 + 3 + (10)/3.33
        #min 0.33
        #0 + 0 + 0 + 0 + 0 + 0 + 1/3.33
        self.score = self.trueRepeatRisiko + self.nearRepeatRisiko + self.sicherheitsausstattung + self.interesse + self.erreichbarkeit + self.polizeiaktivität + self.polizeiwache_entfernung/3.33

    def step(self):
        self.t += 0 
        if (self.trueRepeatRisiko > 0):
            setTrueRepeatRisiko(self, 2 * e^-((t-2)/10)^(2) )       #true - repeat
            
        if (self.neareRepeatRisiko > 0):
            if (random.uniform(0,1) > 0.2):
                updateNearRepeatRisiko(-0.5)                        #near - repeat
        if (random.uniform(0,1) > 0.01):
            updateInteresse(self, 0.5)
            
    def einbruch(self):
        self.t = 0
        updateInteresse(-2)

    def updateSicherheit(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert
        """
        self.sicherheitsausstattung += amount
        if (self.sicherheitsausstattung >= 1):
            self.sicherheitsausstattung = 1
        elif (self.sicherheitsausstattung <= -1):
            self.sicherheitsausstattung = -1

    def updateNearRepeatRisiko(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert(positiv)
        """
        self.repeatRisiko += amount
        if (self.sicherheitsausstattung >= 3):
            self.sicherheitsausstattung = 3
        elif (self.sicherheitsausstattung <= 0):
            self.sicherheitsausstattung = 0

    def updateInteresse(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert
        """
        self.interesse += amount
        if (self.interesse >= 3):
            self.interesse = 3
        elif (self.interesse <= 0):
            self.interesse = 0
            
    def getScore(self):
        return self.score
        
