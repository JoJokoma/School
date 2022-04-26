from Tkinter import *
from Canvas import *
import sys

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 2 # half of point size (must be integer)
CCOLOR = "#0000FF" # blue

elementList = [] # list of elements (used by Canvas.delete(...))

firstPolygon = "polygonA.dat"
secondPolygon = "polygonZ.dat"

time = 0
dt = 0.001

def drawObjekts():
    """ draw polygon and points """

    polygon = getMorphedPolygon()
    
    for (p,q) in zip(polygon,polygon[1:]):
        elementList.append(can.create_line(p[0], p[1], q[0], q[1],
                                           fill=CCOLOR))
        elementList.append(can.create_oval(p[0]-HPSIZE, p[1]-HPSIZE,
                                           p[0]+HPSIZE, p[1]+HPSIZE,
                                           fill=CCOLOR, outline=CCOLOR))
            

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw elements """
    can.delete(*elementList)
    del elementList[:]
    drawObjekts()
    can.update()


def forward():
    global time
    while(time<1):
        time += dt
        print time
        draw()


def backward():
    global time
    while(time>0):
        time -= dt
        print time
        draw()

def pointToGlobal(point):
    """rechnet Punkt der Form [x,y] in Globalkoodinaten um"""
    return [point[0]*WIDTH, -point[1]*HEIGHT+HEIGHT]

def readPolygonDat(name):
    """liest die Datei ein und gibt eine Liste von Punkten der Form [x,y] zurück"""
    points = [map(float, line.split()) for line in file(name)]
    return map(pointToGlobal, points)

def getMorphedPoint(points):
    """Nimmt ein Tupel zweier Punkte an und gibt den gemorphten Punkt zurück"""
    x = (1-time)*points[0][0] + time*points[1][0]
    y = (1-time)*points[0][1] + time*points[1][1]
    return [x,y]

def getMorphedPolygon():
    """erzeugt das passend zur Zeit gemorphte Polygon"""
    return [getMorphedPoint(points) for points in zip(firstPolygon, secondPolygon)]

if __name__ == "__main__":
    # check parameters
    if len(sys.argv) == 3:
       (firstPolygon, secondPolygon) = tuple(sys.argv[1:])

    # read Polygons
    firstPolygon = readPolygonDat(firstPolygon)
    secondPolygon = readPolygonDat(secondPolygon)

    # make both polygons contain same number of points
    while len(firstPolygon) != len(secondPolygon):
        if len(firstPolygon) < len(secondPolygon):
            firstPolygon.append(firstPolygon[-1])
        else:
            secondPolygon.append(secondPolygon[-1])
    
    # create main window
    mw = Tk()
    mw._root().wm_title("Morphing")

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    cFr = Frame(mw)
    cFr.pack(side="left")
    bClear = Button(cFr, text="backward", command=backward)
    bClear.pack(side="left")
    bClear = Button(cFr, text="forward", command=forward)
    bClear.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()
    draw()
    
    # start
    mw.mainloop()
    
