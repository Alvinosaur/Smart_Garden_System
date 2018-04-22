# Mode Demo
from tkinter import *

####################################
# init
####################################

def init(data):
    # There is only one init, not one-per-mode
    data.mode = "splashScreen"
    data.score = 0
    data.rows = data.cols = 100
    data.margin = data.width//20
    data.cellSize = (data.width-data.margin*2)//data.rows
    initColors(data)
    initCoreObjects(data)
    

def initCoreObjects(data):
    data.coreObjects = dict()
    data.coreObjects["gardenBed"]= ((data.cols//4,data.rows//2),data.cols//2,data.rows*3//4)
    data.coreObjects["selectTable"]= ((data.cols*7//8,data.rows//2),
                                                data.cols//4,data.rows*3//4)
    data.board = [[data.colors["board"]]*data.cols for i in range(data.rows)]
    
def initColors(data):
    data.colors = dict()
    data.colors["board"] = "white"
    data.colors["gardenBed"] = "saddle brown"
    data.colors["guideButton"] = "pink"
    data.colors["selectTable"] = "grey"
    data.colors["healthyLeaf"] = "dark green"
    data.colors["weakLeaf"] = "yellow green"
    data.colors["deadLeaf"] = "chocolate3"
    
    
    

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "help"):       helpRedrawAll(canvas, data)

####################################
# splashScreen mode
####################################

def splashScreenMousePressed(event, data):
    if (0<event.x<data.width) and (data.height/2<event.y<data.height/2+40):
        data.mode = "playGame"

def splashScreenKeyPressed(event, data):
    pass

def splashScreenTimerFired(data):
    pass

def splashScreenRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2-20,
                       text="No Garden? Make a Simulation!", font="Arial 26 bold")
    canvas.create_rectangle(0,data.height/2,data.width,data.height/2+40,
                                        fill=data.colors["guideButton"])
    canvas.create_text(data.width/2, data.height/2+20,
                       text="Click Here to Play!", font="Arial 20")

####################################
# help mode
####################################

def helpMousePressed(event, data):
    pass

def helpKeyPressed(event, data):
    data.mode = "playGame"

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2-40,
                       text="This is help mode!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2-10,
                       text="How to play:", font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+15,
                       text="Do nothing and score points!", font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+40,
                       text="Press any key to keep playing!", font="Arial 20")

####################################
# playGame mode
####################################

def playGameMousePressed(event, data):
    data.score = 0

def playGameKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.mode = "help"

def playGameTimerFired(data):
    data.score += 1

def playGameRedrawAll(canvas, data):
    drawBoard(canvas,data)
    drawCoreObjects(canvas,data)
    
    

####################################
# Core Functionality
####################################  

def drawCoreObjects(canvas,data):
    for object in data.coreObjects:
        (cX,cY),width,height = data.coreObjects[object]
        color = data.colors[object]
        startX = cX-width//2
        startY = cY-height//2
        endX = cX+width//2
        endY = cY+height//2
        for row in range(startY,endY):
            for col in range(startX,endX):
                drawCell(canvas,data,row,col,color)

def drawBoard(canvas,data):
    #draw basic background of the board, which can include pieces if locked in
    for row in range(len(data.board)):
        for col in range(len(data.board[row])):
            drawCell(canvas,data,row,col,data.colors["board"])

def drawCell(canvas,data,row,col,fill):
    #draw each individual cell of background
    sideLeft = data.margin+data.cellSize*col
    sideTop = data.margin+data.cellSize*row
    canvas.create_rectangle(sideLeft,sideTop,sideLeft+data.cellSize,
            sideTop+data.cellSize,fill=fill,outline="")

def draw(canvas, x, y, size, level):
    # (x,y) is the lower-left corner of the triangle
    # size is the length of a side
    if (level == 0):
        canvas.create_polygon(x, y,
                              x+size, y,
                              x+size/2, y-size*(3**0.5)/2,
                              fill="black")
    else:
        drawSierpinskyTriangle(canvas, x, y, size/2, level-1)
        drawSierpinskyTriangle(canvas, x+size/2, y, size/2, level-1)
        drawSierpinskyTriangle(canvas, x+size/4, y-size*(3**0.5)/4, size/2, level-1)
####################################
# Tkinter Stuff
####################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)