from tkinter import *
from ZellulärerAutomat import *

import configparser
import time


class Simulation:

    def drawAutomat(self, canvas, breite, hoehe, line_distance, automat):
        """
        Input:
                canvas       : Canvas-objekt
                breite       : Breite der Stadt
                hoehe        : Höhe der Stadt
                line_distance: Größe einer Zelle
                automat      : zu zeichnender Zellulärer Automat
        """
        
        m = automat.Matrix
        ld = line_distance
        for i in range(hoehe):
            for j in range(breite):
                if m[i][j].getTyp() == "haus" or m[i][j].getTyp() == "gewerbliches_gebaeude":
                    value = m[i][j].getScore()
                    r = [0, 255 - (255*(value/self.maxScore))][value >= self.maxScore/2]
                    g = [0, 255 - (255*(value/self.maxScore))][value >= self.maxScore/2]
                    b = [255 - (255*(value/self.maxScore)), 0][value >= self.maxScore/2]
                    canvas.create_rectangle(ld * i + ld, ld * j + ld, ld * i + ld*2,  ld * j + ld*2,
                                            fill='#%02x%02x%02x' % (int(r), int(g), int(b)), outline="")
                elif m[i][j].getTyp() == "polizeiwache":
                    canvas.create_rectangle(ld * i + ld, ld * j + ld, ld * i + ld*2,  ld * j + ld*2,
                                            fill="white", outline="")
                else:
                    canvas.create_rectangle(ld * i + ld, ld * j + ld, ld * i + ld*2,  ld * j + ld*2,
                                            fill="gray", outline="")

    def __init__(self):
        # config laden
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.breite = int(config['STADT']['breite'])
        self.hoehe = int(config['STADT']['hoehe'])
        self.line_distance = int(config['VISUALISIERUNG']['line_distance'])
        anzahlMobilePolizei = int(config['SIMULATION']['anzahlMobilePolizei'])
        anzahlEinbrecher = int(config['SIMULATION']['anzahlEinbrecher'])
        cRepeat = float(config['SIMULATION']['cRepeat'])
        cSicherheit = float(config['SIMULATION']['cSicherheit'])
        cInteresse = float(config['SIMULATION']['cInteresse'])
        cErreichbarkeit = float(config['SIMULATION']['cErreichbarkeit'])
        cPolizeiAktivität = float(config['SIMULATION']['cPolizeiAktivitaet'])
        cPolizeiEntfernung = float(config['SIMULATION']['cPolizeiEntfernung'])

        self.maxScore = cRepeat + cSicherheit + cInteresse + cErreichbarkeit + cPolizeiAktivität + cPolizeiEntfernung

        self.automat = ZellulärerAutomat(self.breite, self.hoehe, anzahlMobilePolizei, anzahlEinbrecher, cRepeat, cSicherheit,
                                    cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung)

        self.master = Tk()

        canvas_breite = self.breite * self.line_distance
        canvas_hoehe = self.hoehe * self.line_distance
        self.w = Canvas(
            self.master,
            width=canvas_breite + 2 * self.line_distance,
            height=canvas_hoehe + 2 * self.line_distance)
        # w.configure(background="#fff")
        self.w.pack()

    def main(self):
        durchläufe = 100
        for t in range(0,durchläufe):
            self.automat.step()
        self.master.title("Zellulärer Automat t={}".format(t))
        self.drawAutomat(self.w, self.breite, self.hoehe, self.line_distance, self.automat)
        self.master.mainloop()

# start_proc = time.process_time()
s = Simulation()
s.main()
# ende_proc = time.process_time()
# print('Systemzeit: {:5.3f}s'.format(ende_proc-start_proc))
