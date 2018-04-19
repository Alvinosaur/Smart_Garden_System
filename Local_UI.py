from tkinter import *
# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
#from GeneratePseudoData import *

def init(data):
    data.type = ""
    data.mode = "startScreen"
    data.updates = ""
    data.screenDelay = 30
    data.textBoxHeight=10
    data.timerCalled = 0
    data.margin = 20
    data.butLine = 3
    data.buttonH = 20
    data.imgSpan = 10
    
    #Temporary
    data.rows = data.cols = 6
    data.gridSize = data.width - data.margin*2
    data.cellSize = data.gridSize/6
    
    data.plantLocs = dict()#keys are plant coordinates, values are functions
    setPlantLocs(data)
    
def setPlantLocs(data):
    for i in range(data.rows):
        for j in range(data.cols):
            row = i*data.cellSize + 30
            col = j*data.cellSize + data.margin
            data.plantLocs[(row,col)]= "row,col"
            data.plantLocs[(row+data.cellSize,col+data.cellSize)]= "row,col"

####################################
# mode dispatcher
####################################

def keyPressed(event, data):
    if (data.mode == "showStats"): showStatsKeyPressed(event, data)

def mousePressed(event, data):
    if (data.mode == "mainScreen"):   mainScreenMousePressed(event, data)
    elif (data.mode == "showGarden"):    showGardenMousePressed(event, data)
    elif (data.mode == "showStats"):       showStatsMousePressed(event, data)

def timerFired(data):
    if (data.mode == "startScreen"): startScreenTimerFired(data)
    elif (data.mode == "showGarden"):   showGardenTimerFired(data)
    elif (data.mode == "showStats"):       showStatsTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "startScreen"): startScreenRedrawAll(canvas, data)
    elif (data.mode == "mainScreen"):   mainScreenRedrawAll(canvas, data)
    elif (data.mode == "showGarden"):       showGardenRedrawAll(canvas, data)
    elif (data.mode == "showStats"):       showStatsRedrawAll(canvas, data)

####################################
# startScreen mode
####################################

def startScreenTimerFired(data):
    data.timerCalled += 1
    #if receive detect any yields(fruits, veggies), then notify
    if data.timerCalled >= data.screenDelay:
        data.mode="mainScreen"

def startScreenRedrawAll(canvas, data):
    #canvas.create_text(data.width/2, data.height*3/4,text=data.updates,.......)
    canvas.create_text(data.width/2, data.height/2-data.height/4,
                       text="Grow Mellon", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2,
                       text="Educating Gardeners for More Sustainable Agriculture", font="Arial 15",fill="grey")
    

####################################
# showGarden mode
####################################

def showGardenMousePressed(event, data):
    for (x,y) in data.plantLocs.keys():
        if (event.x-data.imgSpan <= x <= event.x+data.imgSpan) and \
            (event.y-data.imgSpan <= y <= event.y+data.imgSpan):
            data.mode="showStats"
            data.timerCalled = 0
            data.type = data.plantLocs[(x,y)]

def showGardenTimerFired(data):
    pass

def showGardenRedrawAll(canvas, data):
    for i in range(data.rows):
        for j in range(data.cols):
            x0 = j*data.cellSize + data.margin
            y0 = i*data.cellSize+30
            x1 = x0 + data.cellSize
            y1 = y0 + data.cellSize
            canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text(data.width/2, 0,
                       text="This is showGarden mode!",anchor=N, font="Arial 26 bold")
                       
####################################
# showStats mode
####################################

def showStatsMousePressed(event, data):
    pass
    
def showStatsKeyPressed(event, data):
    if event.char == "q":
        data.mode = "showGarden"

def showStatsTimerFired(data):
    #data.timerCalled += 1
    pass

def showStatsRedrawAll(canvas, data):
    if data.type != "":
        #plt.plot(range(5),range(5))
        canvas.create_text(data.width/2,data.height/2,text="Loser")
    else:
        pass 

####################################
# mainScreen mode
####################################

def mainScreenMousePressed(event, data):
    if (data.margin <= event.x <= data.width-data.margin) and \
            (data.margin < event.y < data.margin+data.buttonH):
        data.mode = "showGarden"

def mainScreenRedrawAll(canvas, data):
    canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,
            data.margin+data.buttonH,fill="pink",width=data.butLine)
    canvas.create_text(data.width//2,data.margin+data.buttonH/2,
            text="See Current Status of Garden",font="Arial 20 bold")
    #canvas.create_rectangle(data.margin,data.margin+data.buttonH,data.width-data.margin,data.margin+data.buttonH*2,fill="pink",width=data.butLine)
    

####################################
# use the run function as-is
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

run(600, 600)