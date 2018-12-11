import random

class zelle:
    
    isHaus = True
    score = 0
    t = 0
	
    def __init__(self, theta1, theta2):
        self.theta1 = theta1
        self.theta2 = theta2
        random.seed()
        self.einbruchVorXTagen = 100
        self.sicherheitsausstattung = random.randrange(-1,1)        #1-low      0-medium    (-1)-high
        self.optik = random.randrange(0,1)                          #0-hetero   1-homo
        self.hausnummer = random.randrange(0,1)                     #0-odd      1-even
        self.erreichbarkeit = random.randrange(-1,1)                #1-high     0-medium    (-1)-low
        self.polizeiaktivität = random.randrange(-1,1)              #1-low      0-medium    (-1)-high


    def isHaus(self):
        return isHause

    def updateScore(self):
        self.score = 3.0/self.einbruchVorXTagen + self.sicherheitsausstattung + self.optik + self.erreichbarkeit + self.polizeiaktivität #+ self.hausnummer
        return self.score

    def step(self):
        self.t += 0
        if (self.t == 3):
            updateSicherheit(-1)
            updatePolizeiaktivität(-1)
        if (self.t == 6):
            updateSicherheit(-1)
            updatePolizeiaktivität(-1)
            
    def einbruch(self):
        self.einbruchVorXTagen = 0

    def updateSicherheit(self, amount):
        self.sicherheitsausstattung += amount
        if (self.sicherheitsausstattung >= 1):
            self.sicherheitsausstattung = 1
        elif (self.sicherheitsausstattung <= -1):
            self.sicherheitsausstattung = -1
        self.t = 0

    def updatePolizeiaktivität(self, amount):
        self.polizeiaktivität += amount
        if (self.polizeiaktivität >= 1):
            self.polizeiaktivität = 1
        elif (self.polizeiaktivität <= -1):
            self.polizeiaktivität = -1
        self.t = 0

    def getStatus(self):
        if (self.score >= self.theta2):
            return "red"
        elif (self.score >= self.theta1):
            return "yellow"
        else:
            return "green"
        
