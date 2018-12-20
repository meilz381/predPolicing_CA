import random
from zelle import *

class gewerbliches_gebaeude(zelle):
    
    score = 0
    t = 0
	
    def __init__(self):     
        self.typ = "gewerbliches_gebaeude"
        
        random.seed()
        self.sicherheitsausstattung = random.randrange(0,4)         #(0)-hoch       (3)-niedrig
        self.interesse = random.randrange(0,4)                      #(0)-niedrig    (3)-hoch
        self.trueRepeatRisiko = 0                                   #(0)-niedrig    (2)-hoch
        self.nearRepeatRisiko = 0                                   #(0)-niedrig    (3)-hoch


        
