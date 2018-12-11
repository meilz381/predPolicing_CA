from tkinter import *
from zellulärer_automat import *
import configparser
import time

def grid(canvas, line_distance, canvas_width, canvas_height):
    # vertical lines at an interval of "line_distance" pixel
    for x in range(line_distance, canvas_width, line_distance):
        canvas.create_line(x, line_distance, x, canvas_height-line_distance, fill="#000000")
    # horizontal lines at an interval of "line_distance" pixel
    for y in range(line_distance, canvas_height, line_distance):
        canvas.create_line(line_distance, y, canvas_width-line_distance, y, fill="#000000")
        
def zellen(canvas, line_distance, canvas_width, canvas_height, width, height, automat):
    m = automat.Matrix
    ld = line_distance
    for i in range(height):
        for j in range(width):
            if (m[i][j].isHaus):
                canvas.create_rectangle(ld * i +ld + 1 , ld * j + ld + 1, ld * i + ld*2,  ld * j + ld*2, fill=m[i][j].getStatus(), outline="")
                

def drawAutomat(canvas, width,height,line_distance,automat):
    canvas_width = width * line_distance
    canvas_height = height * line_distance
    
    grid(canvas, line_distance, canvas_width + 2*line_distance, canvas_height + 2*line_distance)
    zellen(canvas, line_distance, canvas_width, canvas_height, width, height, automat)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    width = int(config['STADT']['WIDTH'])
    height = int(config['STADT']['HEIGHT'])
    line_distance = int(config['VISUALISIERUNG']['LINE_DISTANCE'])
    theta1 = int(config['SIMULATION']['THETA1'])
    theta2 = int(config['SIMULATION']['THETA2'])
    automat = zellulaererAutomat(width, height, theta1, theta2)

    master = Tk()
    master.title("Zellulärer Automat")
    canvas_width = width * line_distance
    canvas_height = height * line_distance
    w = Canvas(master, 
                width=canvas_width + 2*line_distance,
                height=canvas_height + 2*line_distance)
    #w.configure(background="#fff")
    w.pack()


    for t in range(0,50):
        automat.step()

    drawAutomat(w, width, height, line_distance, automat)    

main()
