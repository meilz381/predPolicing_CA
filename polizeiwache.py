from Zelle import *


class Polizeiwache(Zelle):

    def __init__(self):
        self.typ = "polizeiwache"
        
        random.seed()

    def setErreichbarkeit(self, value):
        pass
    
    def setPolizeiwacheEntfernung(self, value):
        pass

    def setRepeatRisiko(self, value):
        pass
    
    def updateScore(self):
        pass

    def step(self):
        pass
    
    def einbruch(self):
        pass

    def updateSicherheit(self, amount):
        pass

    def updateRepeatRisiko(self, amount):
        pass

    def updateInteresse(self, amount):
        pass
            
    def getScore(self):
        pass
