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
#from PlantDetection import *
from Statistics import *

#/dev/tty.usbmodem14541 for mac
#/dev/ttyACM0 or 1 for rpi

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
    data.gardenRows = data.gardenCols = 5
    data.imageSide = data.width//data.gardenCols
    #Temporary
    data.rows = data.cols = 6
    data.gridSize = data.width - data.margin*2
    data.cellSize = data.gridSize/6
    data.options = ["Week","Next Two Weeks","Month"]
    data.genDataButton = "Generate Data!"
    data.plantLocs = dict()#keys are plant coordinates, values are functions
    setPlantLocs(data)
    data.timeMode = ""
    data.getImages = plantDetection()
    data.stats = Stats("Basil")
    data.lineWidth = 4
    data.ticHeight = 8
    data.startInc = data.stats.valueTypes.index("Temp")
    
# def setPlantLocs(data):
#     data.plantLocs.add(plant) for plant in data.getImage.foundPlants

####################################
# mode dispatcher
####################################

def keyPressed(event, data):
    if (data.mode == "showStats"): showStatsKeyPressed(event, data)

def mousePressed(event, data):
    if (data.mode == "mainScreen"):   mainScreenMousePressed(event, data)
    elif (data.mode == "showGarden"):    showGardenMousePressed(event, data)
    elif (data.mode == "showStats"):       showStatsMousePressed(event, data)
    elif (data.mode == "genRand"):           genRandMousePressed(event,data)

def timerFired(data):
    try:data.getImages.main()
    except:pass
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
            ser.write("(%d,%d)"%(x,y))
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
    loadImages(data)            
                       
####################################
# showStats mode
####################################

def showStatsMousePressed(event, data):
    if (data.margin <= event.x <= data.width-data.margin) and \
        (data.margin < event.y < data.margin+data.buttonH):
        data.mode = "showGarden"
    
def showStatsKeyPressed(event, data):
    if event.char == "q":
        data.mode = "showGarden"

def showStatsTimerFired(data):
    #data.timerCalled += 1
    pass

def showStatsRedrawAll(canvas, data):
    if data.type != "":
        canvas.create_rectangle(data.margin,data.margin,data.width-data.margin,
                data.margin+data.buttonH,fill="pink",width=data.butLine)
        canvas.create_text(data.width//2,data.margin+data.buttonH/2,
                text="See Current Status of Garden",font="Arial 20 bold")
        plt.plot([1,2,3,4],[1,2,3,4])
        plt.show()
    else:
        pass 
     
        
####################################
# genRand mode
####################################
def genRandMousePressed(event, data):
    if event.char == "q":
        data.mode = "mainScreen"

def genRandTimerFired(data):
    #show some weather animations
    pass

def genRandRedrawAll(canvas, data):
    if data.timeMode == "Month": duration = 31
    elif data.timeMode == "Week": duration = 8
    test = GenData(duration)
    test.plotData()
        
def visitGenData(data,label):
    data.timeMode = label.get()
    data.mode = "genRand"
        
####################################
# mainScreen mode
####################################

def mainScreenMousePressed(event, data):
    if (data.margin <= event.x <= data.width-data.margin) and \
            (data.margin < event.y < data.margin+data.buttonH):
        data.mode = "showGarden"
    elif (data.margin <= event.x <= data.width-data.margin) and \
        (data.margin+data.buttonH*2 < event.y < data.margin+data.buttonH*3):
        data.mode="genRand"
        data.timeMode = "Month"

def mainScreenRedrawAll(canvas, data):
    createButton(canvas,data,data.width//2,data.margin+data.buttonH//2,
                data.width*3//4,data.buttonH,"pink","See Current Status of Garden")
    createButton(canvas,data,data.width//2,data.margin+data.buttonH*5/2,
                data.width*3//4,data.buttonH,"pink","See Predicted Growth")       
    # label = StringVar(data.root)
    # label.set(data.options[0])
    # w = OptionMenu(data.root, label, *data.options)
    # w.pack()
    # selectButton = Button(data.root,text=data.genDataButton,command=visitGenData)
    #canvas.create_rectangle(data.margin,data.margin+data.buttonH,data.width-data.margin,data.margin+data.buttonH*2,fill="pink",width=data.butLine)
    
####################################
# Core Functionality
####################################  
def createButton(canvas,data,cx,cy,width,height,color,text,font="Arial 20 bold"):
    x0 = cx-width/2+data.margin
    y0 = cy-height/2+data.margin
    x1 = cx+width/2+data.margin
    y1 = cy+height/2+data.margin
    canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=data.butLine)
    canvas.create_text(cx,cy,text=text,font=font)
    
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
    medianY = y0+height-medianGrowth
    canvas.create_line(x0,y0,x0,y0+height,width=data.lineWidth)
    canvas.create_line(x0,y0+height,x0+length,y0+height,width=data.lineWidth)
    canvas.create_line(x0,medianY,x0+length,medianY)
    
    
def drawScatterFeats(canvas,data,x0,y0,values,medianY):
    numTics = len(values)
    distTics = length/(numTicks-1)
    for inc in range(len(values)):
        label = values[inc] #Temp, Bright, Moist
        x = x0+distTics*(inc+1)
        topTic = y0+height-data.ticHeight/2
        botTic = y0+height+data.ticHeight/2
        canvas.create_line(x,topTic,x,botTic)
        canvas.create_text(x,botTic,text=label,anchor=N)
        lowY = data.stats.groupedPlants[inc+data.startInc]["High"] = (len(higherVals),avgDiffHigh)
        canvas.create_oval(x,medianY
    
        

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