from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
from PIL import ImageTk,Image 
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from GeneratePseudoData import *
# import serial
# ser = serial.Serial('/dev/tty.usbmodem14541', 9600)
from PlantDetection import *
from Statistics import *

#/dev/tty.usbmodem14541 for mac
#/dev/ttyACM0 or 1 for rpi

def init(data):
    data.type = ""
    data.mode = "startScreen"
    data.updates = ""
    data.screenDelay = 5
    data.textBoxHeight=10
    data.timerCalled = 0
    data.margin = 20
    data.butLine = 3
    data.buttonH = 20
    data.imgSpan = 10
    #Temporary
    data.options = ["Week","Next Two Weeks","Month"]
    data.genDataButton = "Generate Data!"
    data.plantLocs = dict()#keys are plant coordinates, values are functions
    #setPlantLocs(data)
    data.timeMode = ""
    #data.getImages = plantDetection()
    data.stats = Stats("Basil")
    data.stats.main()
    data.lineWidth = 4
    data.ticHeight = 8
    data.startInc = data.stats.valueTypes.index("Temp")
    data.pointRadius = 2
    data.colors = {"Temp":"red","Bright":"yellow","Moist":"blue"}
    data.valueTypes = ["Temp","Bright","Moist"]
    data.magFactor = 18
    data.pointLocs = dict()
    data.font = "Arial 20 bold"
    data.buttonColor = "yellow"
    data.buttons = dict()
    data.buttons["mainScreen"]=[["UPDATES:"],["See Garden","Simulate Garden"],
                            ["See Weather Forecast","See Overall Data"]]
    
# def setPlantLocs(data):
#     data.plantLocs.add(plant) for plant in data.getImage.foundPlants

####################################
# mode dispatcher
####################################

def keyPressed(event, data):
    if (data.mode == "showStats"): showStatsKeyPressed(event, data)
    elif (data.mode == "showGarden"): showGardenKeyPressed(event, data)
    elif (data.mode == "genRand"):      genRandKeyPressed(event,data)
    elif (data.mode == "showStats"):       showStatsMousePressed(event, data)

def mousePressed(event, data):
    if (data.mode == "mainScreen"):   mainScreenMousePressed(event, data)
    elif (data.mode == "showGarden"):    showGardenMousePressed(event, data)
    elif (data.mode == "showStats"):       showStatsMousePressed(event, data)
    elif (data.mode == "genRand"):           genRandMousePressed(event,data)

def timerFired(data):
    # try:data.getImages.main()
    # except:pass
    if (data.mode == "startScreen"): startScreenTimerFired(data)
    elif (data.mode == "showGarden"):   showGardenTimerFired(data)
    elif (data.mode == "showStats"):       showStatsTimerFired(data)
    elif (data.mode == "genRand"):           genRandTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "startScreen"): startScreenRedrawAll(canvas, data)
    elif (data.mode == "mainScreen"):   mainScreenRedrawAll(canvas, data)
    elif (data.mode == "showGarden"):     showGardenRedrawAll(canvas, data)
    elif (data.mode == "showStats"):        showStatsRedrawAll(canvas, data)
    elif (data.mode == "genRand"):            genRandRedrawAll(canvas,data)

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
                       text="Educating Gardeners for More Sustainable Agriculture", font="Arial 15 bold",fill="grey")
    

####################################
# showGarden mode
####################################

def showGardenMousePressed(event, data):
    for (x,y,area) in data.plantLocs:
        if (event.x-data.imgSpan <= x <= event.x+data.imgSpan) and \
            (event.y-data.imgSpan <= y <= event.y+data.imgSpan):
            #ser.write("(%d,%d)"%(x,y))
            data.mode="showStats"
            data.timerCalled = 0
            data.type = data.plantLocs[(x,y)]

def showGardenTimerFired(data):
    pass
    
def showGardenKeyPressed(event, data):
    print(event.char)
    if event.char =="q":
        data.mode = "mainScreen"

def showGardenRedrawAll(canvas, data):
    gardenRows = gardenCols = 5
    gridSize = data.width - data.margin*2-data.buttonH
    cellSize = gridSize/gardenRows
    for row in range(gardenRows):
        for col in range(gardenCols):
            x0 = col*data.cellSize + data.margin
            y0 = row*data.cellSize+data.buttonH
            x1 = x0 + data.cellSize
            y1 = y0 + data.cellSize
            canvas.create_rectangle(x0,y0,x1,y1)
    canvas.create_text(data.width/2, 0,
                       text="Click on a plant to see its stats",anchor=N, 
                                                        font="Arial 26 bold")
    loadImages(data)
                       
####################################
# showStats mode
####################################

def showStatsMousePressed(event, data):
    for plant in data.stats.indivPlantVals:
        for dedd
        
        
    
def showStatsKeyPressed(event, data):
    if event.char == "q":
        data.mode = "showGarden"

def showStatsTimerFired(data):
    #data.timerCalled += 1
    pass

def showStatsRedrawAll(canvas, data):
    drawScatterGraph(canvas,data,data.margin,data.margin,data.width//2,
                            data.height//2,data.valueTypes)
    
        
####################################
# genRand mode
####################################
def genRandMousePressed(event, data):
    pass

def genRandTimerFired(data):
    #show some weather animations
    pass

def genRandKeyPressed(event, data):
    if event.char =="q":
        data.mode = "mainScreen"

def genRandRedrawAll(canvas, data):
    if data.timeMode == "Month": duration = 31
    elif data.timeMode == "Week": duration = 8
    test = GenData(duration,"high")
    test.plotData()
        
####################################
# mainScreen mode
####################################

def mainScreenMousePressed(event, data):
    buttons = data.buttons["mainScreen"]
    cellHeight = (data.height-data.margin*2)/len(buttons)
    if (data.margin <= event.x < data.margin+data.width//2):
        if (data.margin+cellHeight<= event.y < data.margin+cellHeight*2):
            data.mode = "showGarden"
        elif(data.margin+cellHeight*2<= event.y < data.margin+cellHeight*3):
            data.mode = "seeWeather"
    elif (data.margin+data.width//2 <= event.x < data.margin+data.width)
        if (data.margin+cellHeight<= event.y < data.margin+cellHeight*2):
            data.mode = "simulateGarden"
        elif(data.margin+cellHeight*2<= event.y < data.margin+cellHeight*3):
            data.mode = "seeGenData"

def mainScreenRedrawAll(canvas, data):
    buttons = data.buttons["mainScreen"]
    rows = len(buttons)
    cols = max([len(row) for row in buttons]) 
    cellHeight = (data.height-data.margin*2)/len(buttons)
    for row in range(len(buttons)):
        for col in range(len(buttons[row])):
            cellWidth = data.width/len(buttons[row])
            y0 = data.margin + row*cellHeight
            x0 = data.margin + col*cellWidth
            y1 = y0+cellHeight
            x1 = x0 + cellWidth
            text = buttons[row][col]
            color = data.buttonColor
            canvas.create_rectangle(x0,y0,x1,y1,fill=color)
            canvas.create_text(x0,y0,anchor=NW,text=data.buttonColor,
                                                        font=data.font)
    
def showOptions(canvas,data):
    label = StringVar()
    textEntry.set(userResult)
    textBox = Entry(canvas,textvariable=textEntry)
    canvas.create_window(data.width//2, data.margin+data.buttonH*10/2, 
        window=textBox, width=data.width//4)
    textBox.bind('<Return>', lambda event, plant=userResult,
                                            data=data:seeStats(data,plant))

    # label = StringVar(data.root)
    # label.set(data.options[0])
    # w = OptionMenu(data.root, label, *data.options)
    # w.pack()
    # selectButton = Button(data.root,text=data.genDataButton,command=visitGenData)
    #canvas.create_rectangle(data.margin,data.margin+data.buttonH,data.width-data.margin,data.margin+data.buttonH*2,fill="pink",width=data.butLine)
    
####################################
# Core Functionality
####################################  
# def createButton(canvas,data,row,col,colSpan,rowSpan,color,text,font=):
#     x0 = data.margin+row*
#     y0 = cy-height/2
#     x1 = cx+width/2
#     y1 = cy+height/2
#     canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=data.butLine)
#     canvas.create_text(cx,cy,text=text,font=font)
    
def loadImages(data):
    for row in range(data.gardenRows):
        for col in range(data.gardenCols):
            load = Image.open("IMAGES"+os.sep+"(%d,%d).png"%(col,row))
            rotatedImage = load.rotate(180)
            image = rotatedImage.resize((data.imageSide,data.imageSide), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(image)
            img = Label(image=render)
            img.image = render
            img.place(x=row*data.imageSide, y=col*data.imageSide)
            
def drawScatterGraph(canvas,data,x0,y0,length,height,values):
    medianGrowth=data.stats.medVals[-1]
    medianY = y0+height-medianGrowth*data.magFactor
    canvas.create_line(x0,y0,x0,y0+height,width=data.lineWidth)
    canvas.create_line(x0,y0+height,x0+length,y0+height,width=data.lineWidth)
    canvas.create_line(x0,medianY,x0+length,medianY)
    drawScatterFeats(canvas,data,x0,y0,length,height,values,medianY)
    
def drawScatterFeats(canvas,data,x0,y0,length,height,values,medianY):
    numTics = len(values)
    distTics = length/(numTics)
    for inc in range(len(values)):
        label = values[inc] #Temp, Bright, Moist
        x = x0+distTics*(inc+1)#tic mark doesn't start at 0,0 but is spaced out
        topTic = y0+height-data.ticHeight/2
        botTic = y0+height+data.ticHeight/2
        canvas.create_line(x,topTic,x,botTic)
        canvas.create_text(x,botTic,text=label,anchor=N)
        numPlantsLow,lowY = data.stats.groupedPlants[inc+data.startInc]["Low"]
        numPlantsHigh,highY = data.stats.groupedPlants[inc+data.startInc]["High"]
        drawPoint(canvas,data,x,medianY+lowY*data.magFactor,data.colors[label])
        drawPoint(canvas,data,x,medianY+highY*data.magFactor,data.colors[label])
        
def drawPoint(canvas,data,cx,cy,color):
    canvas.create_oval(cx-data.pointRadius,cy-data.pointRadius,
            cx+data.pointRadius,cy+data.pointRadius,fill=color)
        
def seeStats(data,plant):
    
    

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
    data.root = Tk()
    data.root.title("Grow Mellon: Automated Gardening")
    init(data)
    # create the root and the canvas
    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    data.root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    data.root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    data.root.mainloop()  # blocks until window is closed
    print("bye!")
    
def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    
run(1000, 1000)