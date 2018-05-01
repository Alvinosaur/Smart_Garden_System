# Updated Animation Starter Code
# import pandas as pd
# import numpy as np
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")
from sklearn import linear_model
import numpy as np
import pandas as pd
#from Statistics import *
#from GeneratePseudoData import *
from tkinter import *
import os
from scipy.stats import norm
import random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import math


####################################################################################
################################## InitFunctions ###################################
def init(data):
    data.mode = "login"
    data.plantFolder = "plantImages"
    data.selectedPlant = data.username = ""
    data.usernameFilePath = "Usernames"
    data.entry = ""
    initUI(data)
    initStorages(data)
    trackSliderBalls(data)
    initColors(data)
    initCoreObjects(data)
    initPlants(data)
    collectUsernames(data)
    calcWeatherProb(data)
    setResistances(data)
    data.clicked = False
    data.paused = False
    data.simRunning = False
    data.simEnd = False
    data.userRepeatFlag = False
    data.noneEntered = False
    data.loginBoxSelected = False
    data.monthSelected = False

def initStorages(data):
    data.controlVals = dict()
    data.allPlants = dict() 
    data.plantImages = dict()
    data.userValues = [70,70,70]
    data.valueTypes = ["Temp","Bright","Moist"]
    data.plantSpecies = ["Strawberry","Pumpkin","Corn","Broccoli","Kale","Dill"]
    data.allPlantSizes = dict()
    data.allTimes = [0]
    data.allDrops = []
    data.bugLocs = []
    data.spreadedPlants = []
    data.allUsernames = dict()
    data.optimalFactors = [80,70,45]
    data.optimalSizes = [0]
    data.infectedPlants = []
    data.allScores = set()
    data.infectProbs = dict()
    data.weatherEvent = [False]*len(data.valueTypes)
    data.factorWeights = [.4,.2,.4] #adjustable, just hardcoded for now
    data.monthBoxLoc = (8, data.cols//2)
    

def initUI(data):
    data.rows = data.cols = 100
    data.timerCalled = 1
    data.baseGrowthRate = 0
    data.resultProb = 0
    data.month = "7"
    data.endSize = 0
    data.endTime = 50
    data.timeFactor = 3
    data.weatherTime = 5
    data.growthTime = 2
    data.optGrowth = 0
    data.plantCount = 0
    data.buttonH = data.rows//30
    data.buttonL = data.buttonH*5
    data.sliderL = data.buttonH*8
    data.sliderH = data.buttonH
    data.buttonX = data.cols*3/4
    data.cellSize = data.width/data.rows
    data.slideR = data.buttonH #one cell
    data.sliderLocs = [(data.buttonH,data.buttonX),(data.buttonH*2,data.buttonX),(data.buttonH*3,data.buttonX)]
    data.plantSize = 5
    data.textH = 15
    data.butLine = 2
    data.imageSide = data.cols//4
    data.runButLoc = data.rows*9/10,data.cols*7/10
    
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
    data.colors["bug"] = "orange"
    data.colors["leaderBoard"] = "black"
    
def initPlants(data):
    for inc in range(len(data.plantSpecies)):
        plant = data.plantSpecies[inc]
        (col,row),colSpan,rowSpan = data.coreObjects["selectTable"]
        row = (row-rowSpan/2)+((inc+1)*rowSpan/(len(data.plantSpecies)+1))
        data.plantImages[plant] = [(row,col,data.plantSize,data.baseGrowthRate)]
        data.allPlantSizes[plant] = dict()
        
################################## InitFunctions ###################################
####################################################################################

####################################################################################
################################## updateValues ###################################
    
def setResistances(data):
    data.plantRes = dict()
    data.plantDist = dict()
    data.plantRes["Kale"] = .2
    data.plantDist["Kale"] = 5
    data.plantRes["Strawberry"] = .8
    data.plantDist["Strawberry"] = 4
    data.plantRes["Pumpkin"] = .3
    data.plantDist["Pumpkin"] = 7
    data.plantRes["Corn"] = .4
    data.plantDist["Corn"] = 7
    data.plantRes["Broccoli"] = .4
    data.plantDist["Broccoli"] = 6
    data.plantRes["Dill"] = 0
    data.plantDist["Dill"] = 5
    
def trackSliderBalls(data):
    data.sliderBallLocs = dict()
    for inc in range(len(data.sliderLocs)):
        (row,col) = data.sliderLocs[inc]
        cx = (col+data.sliderL/2)*data.cellSize
        cy = (row+data.sliderH/2)*data.cellSize
        #sliderBallLocs uses rows, cols for key, actual location for value
        data.sliderBallLocs[(row,col)]=(cx,cy)
        data.controlVals[(row,col)]=[data.userValues[inc],data.valueTypes[inc]]
    
def linReg(data):
    if data.simRunning: return
    for plant in data.plantSpecies:
        opt = []
        result = []
        inc = 0
        for (row,col) in data.controlVals: #for each of the sensors
            factorValue,factor = data.controlVals[(row,col)]
            dataTrain = pd.read_csv(plant+"Data"+os.sep+"Train%s.csv"%factor)
            userEntry = np.array([[factorValue]])
            optimal = np.array([[data.optimalFactors[inc]]])
            xTrain = dataTrain[factor].values.reshape(-1,1)
            yTrain = dataTrain['sizeChange']
            linRegModel = linear_model.LinearRegression()
            predictedModel = linRegModel.fit(xTrain,yTrain)
            yPredictUser = predictedModel.predict(userEntry)
            yPredictOpt = predictedModel.predict(optimal)
            result.append(yPredictUser.item(0))
            opt.append(yPredictOpt.item(0))
            inc+=1
        growthRate = (result[0]+result[1])*result[2]/data.timeFactor
        data.optGrowth = (opt[0]+opt[1])*opt[2]/data.timeFactor
        for inc in range(1,len(data.plantImages[plant])):
            #range(1,len) to not include first plant in selecTable
            (row,col,size,rate) = data.plantImages[plant][inc]
            data.plantImages[plant][inc] = (row,col,size,growthRate)
    
def checkRunButton(event,data):
    row,col= data.runButLoc
    x0,y0,x1,y1 = calcBoxDimen(data,row,col,data.buttonL,data.buttonH)
    if (x0<event.x<x1) and (y0<event.y<y1):
        return True
    else: return False
        
def checkPlantBounds(event,data,row,col,radius):
    x0 = (col-radius/2)*data.cellSize
    x1 = (col+radius/2)*data.cellSize
    y0 = (row-radius/2)*data.cellSize
    y1 = (row+radius/2)*data.cellSize
    if (x0<event.x<x1) and (y0<event.y<y1):
        return True
    
def calcBoxDimen(data,row,col,colSpan,rowSpan):
    x0 = col*data.cellSize
    y0 = row*data.cellSize
    x1 = x0+colSpan*data.cellSize
    y1 = y0+rowSpan*data.cellSize
    return x0,y0,x1,y1
    
def selectPlants(event,data):
    for plant in data.plantImages:
        (row,col,size,growthRate) = data.plantImages[plant][0]
        if checkPlantBounds(event,data,row,col,size):
            data.selectedPlant = plant
            
   ##       cx,cy = data.sliderBallLocs[slider]
    #     if checkSliderBounds(data,cx,cy,event,slider):
    #         difference = (event.x-cx)//(data.sliderL/2)
    #         data.controlVals[slider] += difference
    #         cx = event.x
    #         data.sliderBallLocs[slider] = (cx,cy)

def updateSlider(data,event):
    for slider in data.sliderBallLocs:
        cx,cy = data.sliderBallLocs[slider]
        if checkSliderBounds(data,cx,cy,event,slider):
            difference = (event.x-cx)//(data.sliderL/2)
            if difference >0:
                difference*=1.75
            data.controlVals[slider][0] += difference
            cx = event.x
            data.sliderBallLocs[slider] = (cx,cy)

def updatePlants(data):
    data.allTimes.append(data.timerCalled//data.growthTime)
    for species in data.plantImages:
        if len(data.plantImages[species]) == 1: continue
        for inc in range(1,len(data.plantImages[species])):
        #range(1,len) to not include first species in selecTable
            
            try:(row,col,size,rate) = data.plantImages[species][inc]
            except:
                print(inc)
                print(len(data.plantImages[species]))
                print(data.plantImages[species])
                print(data.plantImages[species][-1])
            if len(data.infectedPlants)!=0:
                for (values,species,probInfect) in data.infectedPlants:
                    (checkRow,checkCol,checkSize,checkRate) = values
                    if row == checkRow and col == checkCol:
                        change = infectChange(data)
                        rate -= change
            size += rate
            if size <= 0: size = 0
            data.plantImages[species][inc] =(row,col,size,rate)
            try:
                data.allPlantSizes[species][(row,col)].append(size+rate)
            except: pass
            prevSize = data.optimalSizes[-1]
            data.optimalSizes.append(data.optGrowth+prevSize)
            
def infectChange(data):
    day = data.timerCalled//20
    return math.e**(0.5*(day-5))
    
def moveObjects(data,event):
    #these all have built-in checks for location
    updateSlider(data,event)
    
def checkSliderBounds(data,cx,cy,event,slider):
    #if clicking in the slider box
    row,col = slider
    x0 = col*data.cellSize
    x1 = (col+data.sliderL)*data.cellSize
    y0 = row*data.cellSize
    y1 = (row+data.sliderH)*data.cellSize
    if (x0<event.x<x1) and (y0<event.y<y1):
        return True
    return False
    
def clickGarden(event,data):
    (col,row),colSpan,rowSpan = data.coreObjects["gardenBed"]
    x0,y0,x1,y1 = calcBoxDimen(data,row-rowSpan/2,col-colSpan/2,colSpan,rowSpan)
    if (x0<event.x<x1) and (y0<event.y<y1):
        return True
    
def createPlant(event,data):
    (row,col,size,rate) = data.plantImages[data.selectedPlant][0]
    row = event.y/data.cellSize
    col = event.x/data.cellSize
    data.plantImages[data.selectedPlant].append((row,col,size,rate))
    data.allPlantSizes[data.selectedPlant][(row,col)]= [size]
    data.plantCount +=1
    calcInfectedProb(data)
    
def checkBounds(data,event):
    pass
    
def calcWeatherProb(data):
    month = int(data.month)
    heatDistribution = norm(6.5,2)
    heatFactor = heatDistribution.pdf(month)*4
    
    if month >= 7: #July-Dec
        rainMonth = abs(month-13)
        brightMonth = month-13
    else: rainMonth = month
    rainDistribution = norm(0,5)
    moistFactor = rainDistribution.pdf(rainMonth)*7.5
    
    brightDistribution1 = norm(4,2)
    brightDistribution2 = norm(-4,2)
    brightFactor = (brightDistribution1.pdf(brightMonth)+\
                                    brightDistribution2.pdf(brightMonth))*4
    data.weatherProbs = [heatFactor,brightFactor,moistFactor]
    
    
def randomWeather(data):
    randomChance = random.randint(0,100)/100
    for inc in range(len(data.weatherProbs)):
        factor = data.weatherProbs[inc] #factors already generated at start
        if randomChance <= factor: #the higher the prob, more likely under the curve
            data.weatherEvent[inc] = True
            #already updates here
            data.userValues[inc] += 10
            linReg(data)
        else:data.weatherEvent[inc] = False
            
def rainEvent(data):
    for col in range(data.cols):
        spawnRain = random.randint(0,1)
        vx = random.randint(0,3)
        vy = random.randint(4,7)
        if spawnRain:
            data.allDrops.append((0,col,vx,vy))
    
    
def moveRain(data):
    newDrops = []
    for inc in range(len(data.allDrops)):
        (row,col,vx,vy) = data.allDrops[inc]
        row += vy
        col += vx
        if row <= data.rows or col <= data.cols: #if in bounds 
            newDrops.append((row,col,vx,vy))
    data.allDrops = newDrops
        
def hotEvent(data):
    data.background = "navajo white"
    
    
def brightEvent(data):
    #have the sun get brighter or the clouds disappear
    pass
    
            
def callWeatherEvents(data):
    #called every 100ms
    if data.weatherEvent[0]: hotEvent(data)
    else: data.background = "white"
    if data.weatherEvent[1]: brightEvent(data)
    if data.weatherEvent[2]: rainEvent(data)
            
def recordUsername(data):
    line = "%s,%.1f;"%(data.username,data.endSize)
    filePath = data.usernameFilePath + os.sep + "Collection.txt"
    with open(filePath, "wt") as f:
        f.write(line)  
    
def collectUsernames(data):
    if not os.path.exists(data.usernameFilePath):
        os.mkdir(data.usernameFilePath)
    filePath = data.usernameFilePath + os.sep + "Collection.txt"
    if not os.path.exists(filePath): return
    with open(filePath, "rt") as f:
        contents = f.read()
    for user in contents.split(";"):
        if user == "": continue
        values = user.split(",")
        if values[0] == "":
            username = "Player"
            score = user.split(",")[1]
        else: username, score = user.split(",")
        data.allUsernames[float(score)] = data.allUsernames.get(float(score),
                [])+[username]
        data.allScores.add(float(score))
    
def storeUsername(data):
    if data.username == "": data.noneEntered = True
    for score in data.allUsernames:
        if data.username in data.allUsernames[score]:
            data.userRepeatFlag = True
            return
    data.mode = "setupGarden"
        
def calcEndSize(data):
    for plant in data.plantImages:
        for (row,col) in data.allPlantSizes[plant]:
            size = data.allPlantSizes[plant][(row,col)][-1]
            data.endSize += size
    data.endSize /= data.plantCount
    
def calcBugs(data):
    data.resultProb = 0
    for inc in range(len(data.weatherEvent)):
        factor = int(data.weatherEvent[inc])
        weight = data.factorWeights[inc]
        data.resultProb += factor*weight
    data.resultProb*= 100 #make a distribution 0 to 100
    
def checkInfected(data,plant,species):
    (curRow,curCol,curSize,curRate) = plant
    probInfect = data.infectProbs[(curRow,curCol)]
    if random.randint(0,40) <= probInfect*100:
        data.infectedPlants.append((plant,species,probInfect))
        
def calcInfectedProb(data):
    for species in data.plantSpecies:
        #skip species if no plants in garden
        if len(data.plantImages[species]) == 1:
            continue
        for selfInc in range(1,len(data.plantImages[species])):
            probInfect = data.plantRes[species]
            plant = data.plantImages[species][selfInc]
            (curRow,curCol,curSize,curRate) = plant
            #check neighbors
            for speciesType in data.plantSpecies:
                neighborProb = data.plantRes[speciesType]
                #skip species if no neighbors in garden
                if len(data.plantImages[speciesType])==1:
                    continue
                for neighborInc in range(1,len(data.plantImages[speciesType])):
                    neighborPlant = data.plantImages[speciesType][neighborInc]
                    (neighborRow,neighborCol,size,rate) = neighborPlant
                    if curRow == neighborRow and curCol == neighborCol:
                        #don't double count the plant itself as a neighbor
                        continue
                    distance = math.sqrt((curRow-neighborRow)**2+(curCol-neighborCol)**2)
                    weight = 1-probSpect(distance,data.plantDist[speciesType])
                    #weighted sum of the two based on distance and 
                    #the neighbor's likelihood of infecting a nearby plant
                    probInfect = (probInfect*(1-weight))+(neighborProb*weight)
            data.infectProbs[(curRow,curCol)]=probInfect
        
def spreadInfection(data):
    for plant,species,probInfect in data.infectedPlants:
        curRow,curCol,curSize,curRate = plant
        for speciesType in data.plantSpecies:
            neighborProb = data.plantRes[speciesType]
            #skip species if no neighbors in garden
            if len(data.plantImages[speciesType]) == 1: continue 
            #1,len() to not include the first plants in selectTable
            for inc in range(1,len(data.plantImages[speciesType])):
                (row,col,size,rate) = newPlant = data.plantImages[speciesType][inc]
                distance = math.sqrt((curRow-row)**2+(curCol-col)**2)
                weight = 1-probSpect(distance,data.plantDist[speciesType])
                infectNewProb = (probInfect*(1-weight))+(neighborProb*weight)
                print("donezo")
                if random.randint(0,100) <= infectNewProb*100:
                    #row,col are bug's loc, store target loc in plant
                    data.spreadedPlants.append((plant,newPlant,species,infectNewProb))
                    #DEAL WITH data.infectedPlants's ((plant,species,probInfect))
                    #How to deal with probInfect
                    #Then deal with plant color and growth rate change from bug
                    
                    
def spazzBug(data):
    for inc in range(len(data.bugLocs)):
        #(row,col,bugLoc,species) = data.bugLocs[inc]
        (row,col,plant,species) = data.bugLocs[inc]
        #cx,cy are new possible location of bug
        plantRow,plantCol,size,rate = plant
        cx = col*data.cellSize
        cy= row*data.cellSize
        bounds = int(size/2*data.cellSize)
        cx += random.randint(-bounds,bounds)
        cy += random.randint(-bounds,bounds)
        
        #if newPosLegal(data,cx,cy,plantRow,plantCol,size):
        newCol = cx/data.cellSize
        newRow = cy/data.cellSize
        data.bugLocs[inc] = (newRow,newCol,plant,species)
        
def newPosLegal(data,cx,cy,row,col,size):
    plantY = row*data.cellSize
    plantX = col*data.cellSize
    distance = math.sqrt((plantY-cy)**2+(plantX-cx)**2)
    if distance < size/2:
        return True
    else: return False
    
def probSpect(value,z,M = 1,k = .2):
    deno = 1+math.e**(-k*(value-z))
    result = (M/deno)
    return result
    
def spreadBugs(data):
    newSpreadPlants = []
    if len(data.spreadedPlants)==0: return
    for inc in range(len(data.spreadedPlants)):
        #row, col are the target plant
        #curRow and curCol are the plant that just spread the infection
        (infPlant,newPlant,species,probInfect) = data.spreadedPlants[inc]
        curRow,curCol,size,rate = infPlant
        row,col,newSize,newRate = newPlant
        distanceY = curRow - row
        distanceX = curCol - col
        curRow+= distanceY/3
        curCol+= distanceX/3
        infPlant =  curRow,curCol,size,rate
        #basically, update location of bug(infPlant), keep new plant's loc
        netDistance = math.sqrt((curRow-row)**2+(curCol-col)**2)
        if netDistance < size/2:
            data.infectedPlants.append((newPlant,species,probInfect))
            data.bugLocs.append((row,col,newPlant,species))
        else:
            newSpreadPlants.append((infPlant,newPlant,species,probInfect))
    #get rid of bugs that reached their end goal
    data.spreadedPlants = newSpreadPlants
        
################################## updateValues ###################################
##################################################################################  
        
####################################################################################        
################################## drawObjects ##################################
            
def drawPlants(canvas,data):
    for plant in data.plantSpecies:
        for inc in range(len(data.plantImages[plant])):
            (row,col,size,rate) = data.plantImages[plant][inc]
            canvas.create_oval((col-size/2)*data.cellSize,
            (row-size/2)*data.cellSize,(col+size/2)*data.cellSize,
            (row+size/2)*data.cellSize,fill=data.colors["healthyLeaf"])
            if inc >0:
                drawText(canvas,data,row+1,col,"%.1f"%size)
    for (row,col) in data.infectProbs:
        prob = data.infectProbs[(row,col)]
        drawText(canvas,data,row-1,col,"%.2f"%prob,fill="red")

def drawSlider(canvas,data,slider):
    (row,col) = slider
    x0=col*data.cellSize
    x1=(col+data.sliderL)*data.cellSize
    y0=row*data.cellSize
    y1=(row+data.sliderH)*data.cellSize
    canvas.create_rectangle(x0,y0,x1,y1,fill="red")
    
    cx,cy = data.sliderBallLocs[(row,col)]
    left = cx-(data.slideR/2*data.cellSize)
    right = left+data.slideR*data.cellSize
    top = cy-(data.slideR/2*data.cellSize)
    bot = top+data.slideR*data.cellSize
    canvas.create_oval(left,top,right,bot,fill="yellow")
    
def drawLeaderBoard(canvas,data):
    canvas.create_rectangle(data.width/4,data.height/4,data.width*3/4,
                data.height*3/4,fill=data.colors["leaderBoard"])
    scores = sorted(list(data.allScores))
    names = ""
    count = 0
    for score in scores:
        userList = data.allUsernames[score]
        for name in userList:
            count+=3
            drawText(canvas,data,data.rows/4+count,data.cols/2,"%s:%.1f"%(name,score),fill="white")
    
def createButton(canvas,data,loc,text):
    (row,col) = loc
    x0,y0,x1,y1 = calcBoxDimen(data,row,col,data.buttonL,data.buttonH)
    cx = (x0+x1)/2
    cy = (y0+y1)/2
    textH = (y1-y0)*3/4
    canvas.create_rectangle(x0,y0,x1,y1,fill="green",width=data.butLine)
    canvas.create_text(cx,cy,text=text,font="Arial %d bold "%data.textH)
    
def drawRainDrops(canvas,data):
    if data.allDrops == []: return
    for [row,col,vx,vy] in data.allDrops:
        canvas.create_line(row*data.cellSize,col*data.cellSize,
                    row*data.cellSize+vy,col*data.cellSize+vx,fill="blue")
    
def spawnBug(data):
    for species in data.plantSpecies:
        #skip species if no plants in garden
        if len(data.plantImages[species]) == 1: continue
        for inc in range(1,len(data.plantImages[species])):
            #plant = (curRow,curCol,curSize,curRate)
            plant = data.plantImages[species][inc]
            checkInfected(data,plant,species)
    
def drawBugs(canvas,data):
    if len(data.infectedPlants)==0: return
    for plant,species,probInfect in data.infectedPlants:
        (row,col,size,rate) = plant
       # data.bugLocs.append((row,col,(row,col),species))
        data.bugLocs.append((row,col,plant,species))
    for inc in range(len(data.bugLocs)):
        bugInfo = data.bugLocs[inc]
       # (row,col,plant,species) = bugInfo
        (row,col,plant,species) = bugInfo
        cx = col*data.cellSize
        cy = row*data.cellSize
        r = data.cellSize/2
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=data.colors["bug"])    
    for inc in range(len(data.spreadedPlants)):
        infPlant,newPlant,species,probInfect = data.spreadedPlants[inc]
        row,col,size,rate = infPlant
        cx = col*data.cellSize
        cy = row*data.cellSize
        r = data.cellSize/2
        canvas.create_rectangle(cx-data.cellSize,cy-data.cellSize,
                        cx+data.cellSize,cy+data.cellSize,fill+"orange")
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=data.colors["bug"])   

def drawTextAndBut(canvas,data):
    createButton(canvas,data,data.runButLoc,"Run Simulation")
    drawText(canvas,data,1,data.cols/4,"Test Your Knowledge of Plants")
    drawText(canvas,data,2.5,data.cols/4,"by Choosing the Optimal Growth Parameters!")
    
    temp, bright, moist = list(data.controlVals.values())
    drawText(canvas,data,1,data.cols*3/4,"Temperature: %d Brightness: %d Moisture: %d"%(temp[0],bright[0],moist[0]))
    drawText(canvas,data,data.rows/2,data.cols*3/4,"Press 'd' to delete last plant")
    if data.noneEntered:
        drawText(canvas,data,data.rows/2,data.cols/2,"Don't Leave It Blank!","red")
    for plant in data.plantImages:
        row,col,size,rate = data.plantImages[plant][0]
        drawText(canvas,data,row-size*3/4,col,plant)
    
def drawMonth(canvas,data):
    if data.monthSelected: boxFill = "grey"
    else: boxFill = "white"
    row, col = data.monthBoxLoc
    y,x = row*data.cellSize-data.textH, col*data.cellSize-20
    #month textbox
    canvas.create_rectangle(x,y,x+40,y+data.textH*2,fill=boxFill)
    drawText(canvas,data,row,col,str(data.month))
    drawText(canvas,data,row-2.75,data.cols/2,"Current Month: %s"%data.month)
    
def drawCoreObjects(canvas,data):
    for object in data.coreObjects:
        (cX,cY),colSpan,rowSpan = data.coreObjects[object]
        color = data.colors[object]
        #cx,cy,width,height are rows and cols, not actualy sizes
        startX = cX-colSpan//2
        startY = cY-rowSpan//2
        endX = cX+colSpan//2
        endY = cY+rowSpan//2
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
    sideLeft = data.cellSize*col
    sideTop = data.cellSize*row
    canvas.create_rectangle(sideLeft,sideTop,sideLeft+data.cellSize,
            sideTop+data.cellSize,fill=fill,outline="")
            
def drawText(canvas,data,row,col,text,font="",fill="black"):
    if font == "": font = "Arial %d bold "%data.textH
    canvas.create_text(col*data.cellSize,row*data.cellSize,
                                                text=text,font=font,fill = fill)
         
def showGraph(data):
    # fig = Figure(figsize=(5,5), dpi=100)
    # sizeGraph = fig.add_subplot(111)
    # for plant in data.plantImages:
    #     for (row,col) in data.allPlantSizes[plant]:
    #         sizes = data.allPlantSizes[plant][(row,col)]
    #         sizeGraph.plot(np.array(data.allTimes),np.array(sizes),label="%s"%plant,color="blue")
    #         
    # sizeGraph.plot(np.array(data.allTimes),np.array(data.optimalSizes),label="Optimal",color="red")
    # sizeGraph.xlabel('Time')
    # sizeGraph.ylabel('Plant Growth, Sensor Values')
    # sizeGraph.legend(bbox_to_anchor=(self.graphLegend), loc=1, borderaxespad=0.)
    # sizeGraph.show()
    # plot = FigureCanvasTkAgg(fig)
    # plot.show()
    pass
    
   #    #   a = f.add_subplot(111)
        # a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

       ##   

       ##   canvas = FigureCanvasTkAgg(fig)
        # canvas.show()
    
            
################################## drawObjects ###################################
##################################################################################  

####################################################################################        
################################## Tkinter ##################################
    
def mousePressed(event, data):
    if data.paused: return
    elif (data.mode == "login"): loginMousePressed(event,data)
    elif (data.mode == "setupGarden"): setupGardenMousePressed(event, data)
    elif (data.mode == "simGarden"):   simGardenMousePressed(event, data)
    
def keyPressed(event, data):
    if (data.mode == "setupGarden"): setupGardenKeyPressed(event, data)
    elif (data.mode == "login"): loginKeyPressed(event,data)
    elif (data.mode == "simGarden"):   simGardenKeyPressed(event, data)
    
def timerFired(data):
    if data.paused: return
    elif (data.mode == "setupGarden"): setupGardenTimerFired(data)
    elif (data.mode == "login"): loginTimerFired(data)
    elif (data.mode == "simGarden"):   simGardenTimerFired(data)
    
def redrawAll(canvas,data):
    if data.mode == "setupGarden": setupGardenRedrawAll(canvas, data)
    elif (data.mode == "login"): loginRedrawAll(canvas,data)
    elif data.mode == "simGarden": simGardenRedrawAll(canvas,data)
    
def loginMousePressed(event,data):
    data.noneEntered = False
    data.userRepeatFlag = False
    #login box
    row, col = 10, data.cols/2
    cx = col*data.cellSize
    cy = row*data.cellSize
    if (cx-50<event.x<cx+50) and (cy-data.textH/2<event.y<cy+data.textH/2):
        data.loginBoxSelected = True
    else: data.loginBoxSelected = False
    #login button
    row, col = 5,data.cols/2
    x0,y0,x1,y1 = calcBoxDimen(data,row,col,data.buttonL,data.buttonH)
    if (x0<event.x<x1) and (y0<event.y<y1):
        storeUsername(data)
    
def setupGardenMousePressed(event, data):
    data.noneEntered = False
    if checkRunButton(event,data): 
        if data.plantCount ==0: 
            data.nonEntered = True
            return
        try:month = int(data.month)
        except:return
        linReg(data)
        data.simRunning = True
        data.timerCalled = 1
        data.mode = "simGarden"
        calcWeatherProb(data)
    selectPlants(event,data)
    if data.selectedPlant != "":
        if clickGarden(event,data):
            createPlant(event,data)
    row, col = data.monthBoxLoc
    y,x = row*data.cellSize, col*data.cellSize-20
    if (x<event.x<x+40) and (y<event.y<y+data.textH):
        data.monthSelected = True
    else: data.monthSelected = False
    
        
def simGardenMousePressed(event, data):
    pass


def loginKeyPressed(event,data):
    data.noneEntered = False
    data.userRepeatFlag = False
    if data.loginBoxSelected:
        data.username+= event.char
        if event.keysym == "BackSpace":
            data.username = data.username[:-5]

def setupGardenKeyPressed(event, data):
    if event.keysym == 'Escape':
        data.selectedPlant = ""
    elif data.monthSelected:
        data.month+= event.char
        if event.keysym == "BackSpace":
            data.month = data.month[:-1]
    
    
def simGardenKeyPressed(event, data):
    if event.char =="p": data.paused = not data.paused
    if event.char =="q":
        data.mode = "setupGarden"

def setupGardenTimerFired(data):
    data.timerCalled+=1 

def simGardenTimerFired(data):
    if not data.simRunning: return 
    data.timerCalled+=1
    moveRain(data)
    spazzBug(data)
    if random.randint(0,100) <= data.resultProb:
        spawnBug(data)
    callWeatherEvents(data)
    if data.timerCalled%data.growthTime==0:
        updatePlants(data)
        spreadBugs(data)
    if data.timerCalled%data.weatherTime == 0:
        randomWeather(data)
        calcBugs(data)
    if data.timerCalled == data.endTime:
        data.simRunning = False
        data.simEnd = True
        calcEndSize(data)
        showGraph(data)

def loginTimerFired(data):
    pass

def setupGardenRedrawAll(canvas, data):
    drawBoard(canvas,data)
    drawSlider(canvas,data,data.sliderLocs[0])
    drawSlider(canvas,data,data.sliderLocs[1])
    drawSlider(canvas,data,data.sliderLocs[2])
    drawSlider(canvas,data,data.sliderLocs[2])
    drawCoreObjects(canvas,data)
    drawPlants(canvas,data)
    drawMonth(canvas,data)
    #instructions 
    drawTextAndBut(canvas,data)
    
def simGardenRedrawAll(canvas,data):
    drawBoard(canvas,data)
    drawCoreObjects(canvas,data)
    drawPlants(canvas,data)
    drawRainDrops(canvas,data)
    drawBugs(canvas,data)
    drawText(canvas,data,1,data.cols/2,"Bug Prob:%.2f"%data.resultProb)
    if data.simEnd:
        drawLeaderBoard(canvas,data)
        showGraph(data)
        recordUsername(data)
    #for all the factors, if random weather == True: drawRain(canvas,data)
        
def loginRedrawAll(canvas,data):
    drawText(canvas,data,3,data.cols/2,"Please Enter Your Username")
    row, col = 10, data.cols/2
    cx = col*data.cellSize
    cy = row*data.cellSize
    if data.loginBoxSelected: boxFill = "grey"
    else: boxFill = "white"
    canvas.create_rectangle(cx-50,cy-data.textH/2,cx+50,
                                    cy+data.textH/2,fill=boxFill)
    drawText(canvas,data,row,col,data.username)
    if data.userRepeatFlag:
        drawText(canvas,data,10,data.cols/2,"That username has been taken. Choose another one","red")
    if data.noneEntered:
        drawText(canvas,data,12,data.cols/2,"Don't Leave It Blank!","red")
    createButton(canvas,data,(5,data.cols/2),"Enter")
    
    
################################## Tkinter ##################################
####################################################################################  

####################################
##More Tkinter
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=data.background, width=0)
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
        
    def moveObjectsWrapper(canvas, data,event):
        moveObjects(data,event)
        redrawAllWrapper(canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.background = "white"
    data.timerDelay = 100 # milliseconds
    data.root = Tk()
    init(data)
    # create the data.root and the canvas
    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    data.root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    data.root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    data.root.bind("<B1-Motion>", lambda event: moveObjectsWrapper(canvas,data,event))
    data.root.bind("<ButtonRelease-1>", lambda event: checkBounds(data,event))
    
    timerFiredWrapper(canvas, data)
    # and launch the app
    data.root.mainloop()  # blocks until window is closed

run(800, 800)
