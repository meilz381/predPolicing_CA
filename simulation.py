from tkinter import *
from zellulärer_automat import *
import configparser
import time

def grid(canvas, line_distance, canvas_breite, canvas_hoehe):
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
        
def zellen(canvas, line_distance, canvas_breite, canvas_hoehe, breite, hoehe, automat):
    """
    Input:
            canvas       : Canvas-objekt
            line_distance: Größe einer Zelle
            canvas_breite: Canvas-Breite(u)
            canvas_hoehe : Canvas-Höhe(u)
            breite       : Breite der Stadt
            hoehe        : Höhe der Stadt
            automat      : zu zeichnender Zellulärer Automat
    """
    
    m = automat.Matrix
    ld = line_distance
    for i in range(hoehe):
        for j in range(breite):
            if (m[i][j].isHaus()):
                canvas.create_rectangle(ld * i +ld + 1 , ld * j + ld + 1, ld * i + ld*2,  ld * j + ld*2, fill=m[i][j].getStatus(), outline="")
            else:
                canvas.create_rectangle(ld * i +ld + 1 , ld * j + ld + 1, ld * i + ld*2,  ld * j + ld*2, fill="gray", outline="")

def drawAutomat(canvas, breite, hoehe, line_distance, automat):
    canvas_breite = breite * line_distance
    canvas_hoehe = hoehe * line_distance
    
    grid(canvas, line_distance, canvas_breite + 2*line_distance, canvas_hoehe + 2*line_distance)
    zellen(canvas, line_distance, canvas_breite, canvas_hoehe, breite, hoehe, automat)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    breite = int(config['STADT']['breite'])
    hoehe = int(config['STADT']['hoehe'])
    line_distance = int(config['VISUALISIERUNG']['line_distance'])
    anzahlMobilePolizei = int(config['SIMULATION']['anzahlMobilePolizei'])
    anzahlEinbrecher = int(config['STADT']['anzahlEinbrecher'])
    automat = zellulaererAutomat(breite, hoehe, anzahlMobilePolizei, anzahlEinbrecher)

    master = Tk()
    
    canvas_breite = breite * line_distance
    canvas_hoehe = hoehe * line_distance
    w = Canvas(master, 
                width = canvas_breite + 2*line_distance,
                height = canvas_hoehe + 2*line_distance)
    #w.configure(background="#fff")
    w.pack()


    for t in range(0,100):
        automat.step()
        if (t % 10 == 0):
            master.title("Zellulärer Automat t={}".format(t))
            drawAutomat(w, breite, hoehe, line_distance, automat)   
            

main()
