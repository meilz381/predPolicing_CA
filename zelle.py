import random

class zelle:
    
    score = 0
    t = 0
	
    def __init__(self, theta1, theta2, haus):     
        """
        Input:
            theta1: Einbruchsschwellwert
            theta2: Gefährdungsschwellwert
            isHaus: Haus oder Straße
        """
        self.theta1 = theta1
        self.theta2 = theta2
        self.haus = haus
        
        random.seed()
        self.einbruchVorXTagen = 100
        self.sicherheitsausstattung = random.randrange(-1,2)        #1-low      0-medium    (-1)-high
        self.optik = random.randrange(0,2)                          #0-hetero   1-homo
        self.hausnummer = random.randrange(0,2)                     #0-odd      1-even
##        self.erreichbarkeit = random.randrange(-1,2)                #1-high     0-medium    (-1)-low
        self.polizeiaktivität = random.randrange(-1,2)              #1-low      0-medium    (-1)-high

    def setErreichbarkeit(self, value):
        self.erreichbarkeit = value

    def isHaus(self):
        """
        Returns:
            bool: ist diese Zelle ein Haus
        """
        return self.haus

    def updateScore(self):
        self.score = 3.0/self.einbruchVorXTagen + self.sicherheitsausstattung + self.optik + self.erreichbarkeit + self.polizeiaktivität #+ self.hausnummer

    def step(self):
        self.t += 0 
        if (self.t == 5):
            updateSicherheit(-1)
            updatePolizeiaktivität(-1)
        if (self.t == 20):
            updateSicherheit(-1)
            updatePolizeiaktivität(-1)
            
    def einbruch(self):
        self.einbruchVorXTagen = 0
        self.t = 0

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
        

    def updatePolizeiaktivität(self, amount):
        """
        Input:
            amount: der um zu verändernde Wert
        """
        self.polizeiaktivität += amount
        if (self.polizeiaktivität >= 1):
            self.polizeiaktivität = 1
        elif (self.polizeiaktivität <= -1):
            self.polizeiaktivität = -1

    def getStatus(self):
        if (self.score >= self.theta1):
            return "red"
        elif (self.score >= self.theta2):
            return "yellow"
        else:
            return "green"
        
