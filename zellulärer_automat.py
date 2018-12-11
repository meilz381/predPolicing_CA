from zelle import *

import copy


class zellulaererAutomat:

    def __init__(self, width, height, theta1, theta2):
        self.width = width
        self.height = height

        self.Matrix = [[0 for x in range(height)] for y in range(width)]     
        for i in range(height):
            for j in range(width):
                self.Matrix[i][j] = zelle(theta1, theta2)


    def step(self):
        for i in range(self.height):
            for j in range(self.width):
                z = self.Matrix[i][j]
                z.step()
                z.updateScore()

        for i in range(self.height):
            for j in range(self.width):       
                if (z.getStatus() == "red"):
                    self.Matrix[i][j].einbruch()
                    #doppelte moore nachberschaft
                    dist = 2
                    for x in range(-dist,dist):
                        for y in range(-dist,dist):
                            if (x != 0 and y != 0):
                                self.Matrix[(i+x) % self.height][(j+y) % self.width].updateSicherheit(dist / max(abs(x),abs(y)))
                                self.Matrix[(i+x) % self.height][(j+y) % self.width].updatePolizeiaktivität(dist / max(abs(x),abs(y)))
                            else:
                                self.Matrix[i][j].updateSicherheit(dist)
                                self.Matrix[i][j].updatePolizeiaktivität(dist)
                                                                                                                
