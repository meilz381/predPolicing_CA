from ZellulärerAutomat import *

import configparser
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

class Simulation:

    def generateScoreMatrix(self):

        m = self.automat.Matrix
        scores = []
        for i in range(self.hoehe):
            for j in range(self.breite):
                if m[i][j].getTyp() == "haus" or m[i][j].getTyp() == "gewerbliches_gebaeude":
                    scores.append(m[i][j].getScore())
                elif m[i][j].getTyp() == "polizeiwache":
                    scores.append(0)
                elif m[i][j].getTyp() == "straße":
                    scores.append(0)

        Z = np.array(scores).reshape(self.breite, self.hoehe)

        return Z

    def generateScoreArray(self):

        m = self.automat.Matrix
        scores = []
        for i in range(self.hoehe):
            for j in range(self.breite):
                if m[i][j].getTyp() == "haus" or m[i][j].getTyp() == "gewerbliches_gebaeude":
                    scores.append(m[i][j].getScore())
                elif m[i][j].getTyp() == "polizeiwache":
                    scores.append(0)
                elif m[i][j].getTyp() == "straße":
                    scores.append(0)

        Z = np.array(scores)

        return Z


    def __init__(self):
        # config laden
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.breite = int(config['STADT']['breite'])
        self.hoehe = int(config['STADT']['hoehe'])
        anzahlMobilePolizei = int(config['SIMULATION']['anzahlMobilePolizei'])
        anzahlEinbrecher = int(config['SIMULATION']['anzahlEinbrecher'])
        cRepeat = float(config['SIMULATION']['cRepeat'])
        cSicherheit = float(config['SIMULATION']['cSicherheit'])
        cInteresse = float(config['SIMULATION']['cInteresse'])
        cErreichbarkeit = float(config['SIMULATION']['cErreichbarkeit'])
        cPolizeiAktivität = float(config['SIMULATION']['cPolizeiAktivitaet'])
        cPolizeiEntfernung = float(config['SIMULATION']['cPolizeiEntfernung'])

        self.maxScore = cRepeat + cInteresse + cErreichbarkeit
        self.minScore = 0 - cSicherheit - cPolizeiAktivität - cPolizeiEntfernung
        self.rangeScore = self.maxScore - self.minScore

        self.automat = ZellulärerAutomat(self.breite, self.hoehe, anzahlMobilePolizei, anzahlEinbrecher, cRepeat, cSicherheit,
                                    cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung, (-1)*self.minScore, self.rangeScore)

    def animate(self, i):
        #plt.title("ZellulärerAutomat t = {}".format(i))
        self.automat.step()
        Z = self.generateScoreArray()
        # Mesh flippen
        # Z = Z[::-1]
        #plt.pcolormesh(self.X, self.Y, Z)
        self.im.set_array(Z)
        self.im.set_clim(0, self.rangeScore)
        self.im.set_cmap(plt.cm.get_cmap('gnuplot'))
        self.title.set_text("t = {}".format(i))
        return self.im, self.title

    def main(self):
        durchläufe = 500

        # animation
        fig = plt.figure(figsize=(10, 10), dpi=80)

        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='#cfd98c')
        self.title = ax.text(0.5, 0.85, "", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                        transform=ax.transAxes, ha="center")

        x = np.arange(0, self.breite + 1)
        y = np.arange(0, self.hoehe + 1)
        self.X, self.Y = np.meshgrid(x, y)
        Z = self.generateScoreMatrix()

        self.im = plt.pcolormesh(self.X, self.Y, Z, vmin=0, vmax=self.rangeScore, cmap=plt.cm.get_cmap('gnuplot'))
        plt.axis('equal')
        plt.axis('off')

        fig.colorbar(self.im)

        ani = FuncAnimation(fig, self.animate, frames=range(0,durchläufe), blit=True, interval=1, repeat=False)

        plt.show()

        # funktioniert nicht atm
        # FFMpegWriter = animation.writers['ffmpeg']
        # metadata = dict(title='Simulation', artist='Matplotlib',
        #                 comment='')
        # writer = FFMpegWriter(fps=15, metadata=metadata)
        # ani.save('simulation.mp4', writer=writer)


s = Simulation()
s.main()
