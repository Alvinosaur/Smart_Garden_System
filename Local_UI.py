from tkinter import *

def init(data):
    data.mode = "startScreen"
    data.textBoxHeight=10
    data.timerCalled = 0
    data.margin = 20
    data.butLine = 3
    data.buttonH = 5

####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if (data.mode == "startScreen"): startScreenMousePressed(event, data)
    elif (data.mode == "mainScreen"):   mainScreenMousePressed(event, data)
    elif (data.mode == "showGarden"):       showGardenMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "startScreen"): startScreenKeyPressed(event, data)
    elif (data.mode == "mainScreen"):   mainScreenKeyPressed(event, data)
    elif (data.mode == "showGarden"):       showGardenKeyPressed(event, data)

def timerFired(data):
    if (data.mode == "startScreen"): startScreenTimerFired(data)
    elif (data.mode == "showGarden"):       showGardenTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "startScreen"): startScreenRedrawAll(canvas, data)
    elif (data.mode == "mainScreen"):   mainScreenRedrawAll(canvas, data)
    elif (data.mode == "showGarden"):       showGardenRedrawAll(canvas, data)

####################################
# startScreen mode
####################################

def startScreenMousePressed(event, data):
    pass

def startScreenKeyPressed(event, data):
    data.mode = "mainScreen"

def startScreenTimerFired(data):
    data.timerCalled += 1
    if data.timerCalled ==30:
        data.mode="mainScreen"

def startScreenRedrawAll(canvas, data):
    
    canvas.create_text(data.width/2, data.height/2-data.height//4,
                       text="Grow Mellon", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2,
                       text="Educating Gardeners for More Sustainable Agriculture", font="Arial 15",fill="grey")

####################################
# showGarden mode
####################################

def showGardenMousePressed(event, data):
    pass

def showGardenKeyPressed(event, data):
    data.mode = "mainScreen"

def showGardenTimerFired(data):
    pass

def showGardenRedrawAll(canvas, data):
    canvas.create_rectangle(
    canvas.create_text(data.width/2, data.height/2-40,
                       text="This is showGarden mode!", font="Arial 26 bold")

####################################
# mainScreen mode
####################################

def mainScreenMousePressed(event, data):
    if (data.margin < event.x < data.width-data.margin) and \
            (data.margin < event.y < data.margin+data.buttonH/2):
        data.mode = "showGarden"
        

def mainScreenKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.mode = "showGarden"
def mainScreenRedrawAll(canvas, data):
    canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,
            data.margin+data.buttonH,fill="pink",width=data.butLine)
    canvas.create_text(data.width//2,data.margin+data.buttonH/2,
            text="See Current Status of Garden",font="Arial 26 bold")
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

run(300, 300)