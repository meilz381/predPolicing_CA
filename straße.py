import random
from zelle import *

class straße(zelle):
	
    def __init__(self):     
        self.typ = "straße"
        
        random.seed()

    def setErreichbarkeit(self, value):
        pass
    
    def setPolizeiwacheEntfernung(self, value):
        pass

    def setTrueRepeatRisiko(self, value):
        pass

    def setNearRepeatRisiko(self, value):
        pass
    
    def updateScore(self):
        pass

    def step(self):
        pass
    
    def einbruch(self):
        pass

    def updateSicherheit(self, amount):
        pass

    def updateNearRepeatRisiko(self, amount):
        pass

    def updateInteresse(self, amount):
        pass
            
    def getScore(self):
        pass
