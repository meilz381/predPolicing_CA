from Zelle import *


class GewerblichesGebäude(Zelle):
    
    score = 0
    t = 0

    def __init__(self):
        self.typ = "gewerbliches_gebaeude"
        
        random.seed()
        self.sicherheitsausstattung = random.uniform(0, 1)           # (0)-hoch       (1)-niedrig
        self.interesse = random.uniform(0, 1)                        # (0)-niedrig    (1)-hoch
        self.repeatRisiko = 0                                        # (0)-niedrig    (1)-hoch

