from tkinter import *
from ZellulärerAutomat import *
import configparser


class Simulation:

    def grid(self, canvas, line_distance, canvas_breite, canvas_hoehe):
        """
        Input:
                canvas       : Canvas-objekt
                line_distance: Größe einer Zelle
                canvas_breite: Canvas-Breite
                canvas_hoehe : Canvas-Höhe
        """
        
        # vertikale linien im interval von "line_distance" pixel
        for x in range(line_distance, canvas_breite, line_distance):
            canvas.create_line(x, line_distance, x, canvas_hoehe-line_distance, fill="#000000")
        # horizontale linien im interval von "line_distance" pixel
        for y in range(line_distance, canvas_hoehe, line_distance):
            canvas.create_line(line_distance, y, canvas_breite-line_distance, y, fill="#000000")

    def zellen(self, canvas, line_distance, breite, hoehe, automat):
        """
        Input:
                canvas       : Canvas-objekt
                line_distance: Größe einer Zelle
                breite       : Breite der Stadt
                hoehe        : Höhe der Stadt
                automat      : zu zeichnender Zellulärer Automat
        """
        
        m = automat.Matrix
        ld = line_distance
        for i in range(hoehe):
            for j in range(breite):
                if m[i][j].getTyp() == "haus" or m[i][j].getTyp() == "gewerbliches_gebaeude":
                    value = m[i][j].getScore()
                    #print (m[i][j].repeatRisiko, m[i][j].sicherheitsausstattung, m[i][j].interesse, m[i][j].erreichbarkeit,
                    #       m[i][j].erreichbarkeit, m[i][j].polizeiaktivität, m[i][j].polizeiwacheEntfernung)
                    r = [0, 255 - (255*(value/self.maxScore))][value >= self.maxScore/2]
                    g = [0, 255 - (255*(value/self.maxScore))][value >= self.maxScore/2]
                    b = [255 - (255*(value/self.maxScore)), 0][value >= self.maxScore/2]
                    #print(r,g,b)
                    #print(value)
                    canvas.create_rectangle(ld * i + ld, ld * j + ld, ld * i + ld*2,  ld * j + ld*2,
                                            fill='#%02x%02x%02x' % (int(r), int(g), int(b)), outline="")
                elif m[i][j].getTyp() == "polizeiwache":
                    canvas.create_rectangle(ld * i + ld, ld * j + ld, ld * i + ld*2,  ld * j + ld*2,
                                            fill="white", outline="")
                else:
                    canvas.create_rectangle(ld * i + ld, ld * j + ld, ld * i + ld*2,  ld * j + ld*2,
                                            fill="gray", outline="")

    ## mit grid
    ##def zellen(self, canvas, line_distance, canvas_breite, canvas_hoehe, breite, hoehe, automat):
    ##    """
    ##    Input:
    ##            canvas       : Canvas-objekt
    ##            line_distance: Größe einer Zelle
    ##            canvas_breite: Canvas-Breite(u)
    ##            canvas_hoehe : Canvas-Höhe(u)
    ##            breite       : Breite der Stadt
    ##            hoehe        : Höhe der Stadt
    ##            automat      : zu zeichnender Zellulärer Automat
    ##    """
    ##    
    ##    m = automat.Matrix
    ##    ld = line_distance
    ##    for i in range(hoehe):
    ##        for j in range(breite):
    ##            if (m[i][j].getTyp() == "haus" or m[i][j].getTyp() == "gewerbliches_gebaeude"):
    ##                value = m[i][j].getScore()
    ##                #print (value)
    ##                r = [0, 255 - (255*(value/16))][value>=8]
    ##                g = [0, 255 - (255*(value/16))][value>=8]
    ##                b = [255 - (255*(value/16)), 0][value>=8] 
    ##                canvas.create_rectangle(ld * i +ld + 1 , ld * j + ld + 1, ld * i + ld*2,  ld * j + ld*2, fill='#%02x%02x%02x' % (int(r), int(g), int(b)), outline="")
    ##            elif (m[i][j].getTyp() == "polizeiwache"):
    ##                canvas.create_rectangle(ld * i +ld + 1 , ld * j + ld + 1, ld * i + ld*2,  ld * j + ld*2, fill="white", outline="")
    ##            else:
    ##                canvas.create_rectangle(ld * i +ld + 1 , ld * j + ld + 1, ld * i + ld*2,  ld * j + ld*2, fill="gray", outline="")

    def drawAutomat(self, canvas, breite, hoehe, line_distance, automat):
        canvas_breite = breite * line_distance
        canvas_hoehe = hoehe * line_distance
        
        # self.grid(canvas, line_distance, canvas_breite + 2*line_distance, canvas_hoehe + 2*line_distance)
        self.zellen(canvas, line_distance, breite, hoehe, automat)

    def main(self):
        # config laden
        config = configparser.ConfigParser()
        config.read('config.ini')

        breite = int(config['STADT']['breite'])
        hoehe = int(config['STADT']['hoehe'])
        line_distance = int(config['VISUALISIERUNG']['line_distance'])
        anzahlMobilePolizei = int(config['SIMULATION']['anzahlMobilePolizei'])
        anzahlEinbrecher = int(config['SIMULATION']['anzahlEinbrecher'])
        cRepeat = float(config['SIMULATION']['cRepeat'])
        cSicherheit = float(config['SIMULATION']['cSicherheit'])
        cInteresse = float(config['SIMULATION']['cInteresse'])
        cErreichbarkeit = float(config['SIMULATION']['cErreichbarkeit'])
        cPolizeiAktivität = float(config['SIMULATION']['cPolizeiAktivitaet'])
        cPolizeiEntfernung = float(config['SIMULATION']['cPolizeiEntfernung'])

        self.maxScore = cRepeat + cSicherheit + cInteresse + cErreichbarkeit + cPolizeiAktivität + cPolizeiEntfernung
        
        automat = ZellulärerAutomat(breite, hoehe, anzahlMobilePolizei, anzahlEinbrecher, cRepeat, cSicherheit, cInteresse, cErreichbarkeit, cPolizeiAktivität, cPolizeiEntfernung)

        master = Tk()
        
        canvas_breite = breite * line_distance
        canvas_hoehe = hoehe * line_distance
        w = Canvas(
            master,
            width=canvas_breite + 2*line_distance,
            height=canvas_hoehe + 2*line_distance)
        # w.configure(background="#fff")
        w.pack()

        for t in range(0,50):
            automat.step()
            if t % 10 == 0:
                master.title("Zellulärer Automat t={}".format(t))
                self.drawAutomat(w, breite, hoehe, line_distance, automat)   


s = Simulation()
s.main()
