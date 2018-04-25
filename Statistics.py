import os  
import math  
#import matplotlib.pyplot as plt
from tkinter import *

class Stats(object):
    path = "Plant_Data"
    def __init__(self,species):
        self.species = species #call for every species, ex: Basil
        self.indivPlantVals = dict() #stores specific values for each plant
        self.allSensorVals = dict() #stores all sensor values
        self.valueChanges = dict() #stores rate of change of all values
        self.groupedPlants = dict()
        self.valueTypes = ["x","y","Day","Temp","Bright","Moist","Size"]
        self.numVals = len(self.valueTypes)
        self.medVals = [0]*self.numVals #[day,medTemp,medBright,medMoist,medSize]
        self.optTemp = self.optBright = self.optMoist = 0  
    
    def getData(self):
        filePath = Stats.path+os.sep+self.species #Plant_Data/Basil
        for plant in os.listdir(filePath): #every plant instance
            if plant.startswith('.'): continue #ignore .DS_Store
            plantFolder = filePath+os.sep+plant
            contents = Stats.readFile(plantFolder+os.sep+"Data.csv")#read contents
            #sort data, calculate rates of change
            self.sortData(contents,plant)
            self.storeValueRates(plant)
            self.findAnomalies(plant)
            
    def sortData(self,contents,plant):
        #store every sensor value into self.allSensorVals for collective median calc
        #store each plant instance's sensor values into self.indivPlantVals
        self.indivPlantVals[plant] = [[0] for species in range(self.numVals)]
        lines = contents.split(";") #sorts data from csv file
        lines = lines[:-1]
        for line in lines:
            sepVals = line.split(",")
            #x,y,day,temp,light,moist,size = sepVals
            for valueInc in range(len(sepVals)):
                infoType = self.valueTypes[valueInc] #name of info
                value = float(sepVals[valueInc])
                if self.allSensorVals.get(infoType,0) != 0: #if not empty
                    self.allSensorVals[infoType].append(value)
                else:
                    self.allSensorVals[infoType] = [value]
                #every plant has dict of sensors with datapoints in a list
                self.indivPlantVals[plant][valueInc].append(value)
                
    def storeValueRates(self,plant):
        #stores rate of change of all sensor values, including size
        self.valueChanges[plant] = [[] for species in range(self.numVals)]
        for sensorInc in range(self.numVals):
            allVals = self.indivPlantVals[plant][sensorInc] #grab data values
            for valInc in range(1,len(allVals)): 
                changePerDay = float(allVals[valInc])-float(allVals[valInc-1])
                self.valueChanges[plant][sensorInc].append(changePerDay)
                #includes change in day, just ignore this

    def findAnomalies(self,plant):
        #find anomalies in sensor data, look at growth at each instance
        for sensorInc in range(self.numVals-1): #don't include growth rate
            allData = self.valueChanges[plant][sensorInc]
            mean = Stats.calcMean(allData)
            stdDev = Stats.calcStdDev(allData,mean)
            lowerOutliers = [x for x in allData if (x < mean-2*stdDev)]
            highOutliers = [x for x in allData if (x > mean+2*stdDev)]
            allOutliers = lowerOutliers + highOutliers
            
            for outlier in allOutliers:
                index = self.valueChanges[plant][sensorInc].index(outlier)
                growthRate = self.valueChanges[plant][-1][index]
                #diffGrowth is percent change in growth rate 
                diffGrowth = (growthRate-self.medVals[-1])/(self.medVals[-1])
                diffSensor = outlier - self.medVals[sensorInc]
                #update optimal value by weighted difference in sensor value
                self.optVals[sensorInc] += diffSensor*diffGrowth
                
    def calcCollectiveMed(self):#calculate collective median for each sensor
        for sensorInc in range(self.numVals):
            sensor = self.valueTypes[sensorInc]
            #sort list of each sensor to calculate median
            medVal = Stats.calcMedian(self.allSensorVals[sensor])
            self.medVals[sensorInc] = medVal
            
    def compareEachSensor(self):
        for sensorInc in range(3,self.numVals):
            #won't contain the first three values: x,y,day
            self.groupedPlants[sensorInc] = dict()
            #sort plants into two groups of sensor values below and above median
            lowerVals, higherVals = self.compareEachPlant(sensorInc)
            avgDiffHigh,avgGrowthRateHigh = self.calcGrowthStats(higherVals)
            avgDiffLow,avgGrowthRateLow = self.calcGrowthStats(lowerVals)
            self.groupedPlants[sensorInc]["High"] = (len(higherVals),avgDiffHigh)
            self.groupedPlants[sensorInc]["Low"] = (len(lowerVals),avgDiffLow)
            if avgGrowthRateHigh > avgGrowthRateLow:
                self.groupedPlants[sensorInc]["Result"] = "High"
            else:
                self.groupedPlants[sensorInc]["Result"] = "Low"
    #HOW TO BEST ANALYZE THIS DATA??????

    def compareEachPlant(self,sensorInc):
        #compare every median sensor value for every plant with collective median
        #higherVals and lowerVals constantly reset for each sensor
        higherVals = dict() #contain plants with sensor value higher than median
        lowerVals = dict()
        for plant in self.indivPlantVals:
            medVal = Stats.calcMedian(self.indivPlantVals[plant][sensorInc])
            #compare individual and collective median
            difference = medVal-self.medVals[sensorInc]
            weight = abs(difference)/self.medVals[sensorInc]
            if difference >= 0:
            #get % difference for weighing
                higherVals[plant]= difference*weight
            else: 
                lowerVals[plant] = difference*weight
        return lowerVals,higherVals

    def calcGrowthStats(self,group):
        #calc avg diff sensor value and growth rate for every plant in group
        growthTotal = sumGrowthRates = 0
        avgDiff = 0
        count = 0
        for plant in group:
            growthVals = self.valueChanges[plant][-1]
            growthMed = Stats.calcMedian(growthVals)
            sumGrowthRates += growthMed
            avgDiff += group[plant]
            startGrowth = growthVals[0]
            endGrowth = growthVals[-1]
            growthTotal += (endGrowth - startGrowth)
            count+=1
        return avgDiff/count,growthTotal/count
                
    def getOptimalVals(self):
        #grabs previously stored values if they exist
        #if they don't, just set them to the median and store
        optFolder = Stats.path+os.sep+self.species+"Optimal"
        optFile = optFolder+os.sep+"optValues.txt"
        if os.path.exists(optFolder):
            if os.path.exists(optFile):
                values = Stats.readFile(optFile)
                self.optTemp, self.optBright, self.optMoist = values.split(",")
                self.optVals  = [float(self.optTemp),float(self.optBright),
                            float(self.optMoist)]
            else:
                self.storeOptValue(optFile)
                self.getOptimalVals()
        else:
            os.path.makedirs(optFolder)
            self.storeOptValue(optFile)
            self.getOptimalVals()
            
    def generateOptString(self):
        #convert optimal values into a string csv format
        values =""
        for inc in range(self.numVals-1):
            values += str(self.medVals[inc])
            values += ","
        return values[:-1]
        
    def storeOptValue(self,file):
        with open(file, "wt") as f:
            values = self.generateOptString()
            f.write(values)  
            
    
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()
    def calcMean(numList):
        return sum(numList)/len(numList)
        
    def calcStdDev(numList,mean):
        variance = []
        for value in numList:
            variance.append((value-mean)**2)
        return sum(variance)**0.5
        
    def calcMedian(curList): #takes in sorted list, doesn't modify original
        midIndex = len(curList)//2
        curList = sorted(curList)
        if len(curList)%2 == 0:
            #take average of two middle values
            medVal = (curList[midIndex]+curList[midIndex-1])/2
        else:
            medVal = curList[midIndex]
        return medVal
    def main(self):
        self.getData()
        self.calcCollectiveMed()
        self.compareEachSensor()
        self.getOptimalVals()
        #self.plotData()
        
    # def plotData(self):
    #     for plant in self.indivPlantVals:
    #         days = self.indivPlantVals[plant][2]
    #         for valueInc in range(len(3,self.indivPlantVals[plant])):
    #             #Temperature --> size
    #             values = self.indivPlantVals[plant][valueInc]
    #             plt.plot(days,temps,label="Temperature(F)",color="red")
    #             plt.plot(days,moists,label="Moisture(m^3/m^3)",color="blue")
    #             plt.plot(days,brights,label="Brightness",color="gold")
    #             plt.plot(days,sizes,label="Plant Size",color="green")
    #     plt.xlabel('Time')
    #     plt.ylabel('Plant Growth, Sensor Values')
    #     plt.legend(bbox_to_anchor=(1, 0.5), loc=1, borderaxespad=0.)
    #     plt.show()

class neuralNetwork(object):
    LEARNING_RATE = 0.5
    def __init__(self,species,indivPlantVals,valueTypes,optVals,valueChanges):
        self.species = species
        self.indivPlantVals = indivPlantVals
        self.valueTypes = valueTypes
        self.optVals = optVals
        self.valueChanges = valueChanges
        self.hiddenLayerNet = dict()
        self.hiddenLayerOut = dict()
        self.outputLayerNet = dict()
        self.outputLayerOut = dict()
        self.hiddenWeights = dict()
        self.outputWeights = dict()
        self.newOutputWeights = dict()
        self.newHiddenWeights = dict()
        startIndex = self.valueTypes.index("Temp")#skip the location and date values
        self.sensorVals = self.valueTypes[startIndex:-1]
        self.numNeurons = len(self.sensorVals)
        self.hiddenBias = .5
        self.outerBias = .5
        #not sure what weights to predefine
        self.optVals = [0]*(self.numNeurons)
        self.growthFactor = 5
        self.changeFactor = 2
        
    def initializeNeuralNetwork(self,plant):
        self.hiddenLayerNet[plant]= [self.hiddenBias]*(self.numNeurons)
        self.hiddenLayerOut[plant]= [0]*(self.numNeurons)
        self.outputLayerNet[plant]= self.outerBias
        self.outputLayerOut[plant]= 0
        self.errors = []
    def initializeWeights(self):
        filePath = "Plant_Data"+os.sep+self.species+"Optimal"+os.sep+"Weights.txt"
        if os.path.exists(filePath):
            contents = Stats.readFile(filePath)
            weightList = contents.split(";")
            for weightString in weightList:
                values = weightString.split(",")
                
        for plant in self.indivPlantVals:
            self.outputWeights[plant] = [.5]*self.numNeurons
            self.hiddenWeights[plant] = [[.5]*self.numNeurons for i in range(self.numNeurons)]
        
    def initializeNewWeights(self,plant):
        self.newOutputWeights[plant] = [] #need to append new weights
        self.newHiddenWeights[plant] = [[.5]*self.numNeurons for i in range(self.numNeurons)] #need to destructively modify values
        
    def calcHiddenNet(self,type,plant,day=0):
        #for each neuron, get each sensor input
        # plantCount = len(self.indivPlantVals)
        for neuronInc in range(self.numNeurons): #for every sensor input
            for sensorInc in range(self.numNeurons):
                if type == "endPredictSize":
                    input = Stats.calcMedian(self.indivPlantVals[plant][sensorInc])
                elif type == "dayPredictSize":
                    input = self.indivPlantVals[plant][sensorInc+3][day]
                input = input - self.optVals[sensorInc] #input is the diff from optimal
                #weight for every neuron and every input
                weight = self.hiddenWeights[plant][neuronInc][sensorInc]
                netInput = weight*input
                #every plant
                self.hiddenLayerNet[plant][neuronInc]+=netInput
            
    def calcHiddenOut(self,plant):
        for neuronInc in range(self.numNeurons):
            net = self.hiddenLayerNet[plant][neuronInc]
            self.hiddenLayerOut[plant][neuronInc]=self.activeFunc(net)
            
    def calcOuterNet(self,plant):
        for neuronInc in range(self.numNeurons):
            weight = self.outputWeights[plant][neuronInc]
            input = self.hiddenLayerOut[plant][neuronInc]
            netInput = weight*input
            #only one output node, so just add all the hidden layer outputs
            self.outputLayerNet[plant]+=netInput
        
    def calcOuterOut(self,plant):
        net = self.outputLayerNet[plant]
        self.outputLayerOut[plant]=self.activeFunc(net) #*50 ????
        
    def backProp(self,type,plant):
        #one output weight for one neuron
        #3 input weights for each neuron b/c 3 sensor inputs
        for neuronInc in range(self.numNeurons):
            if type =="endPredictSize":
                errorWrtOuterOut, outerOutWrtOuterNet=\
                    self.updateOutputWeights(type,plant,neuronInc)
                for sensorInc in range(self.numNeurons):
                    self.updateHiddenWeights(type,plant,neuronInc,sensorInc,
                                        errorWrtOuterOut,outerOutWrtOuterNet)
            elif type =="dayPredictSize":
                for day in range(len(self.valueChanges[plant])):
                    errorWrtOuterOut, outerOutWrtOuterNet=\
                        self.updateOutputWeights(type,plant,neuronInc,day)
                    for sensorInc in range(self.numNeurons):
                        self.updateHiddenWeights(type,plant,neuronInc,sensorInc,
                                    errorWrtOuterOut,outerOutWrtOuterNet,day)
        
    def updateOutputWeights(self,type,plant,neuronInc,day=0):
        #list of sizes is last
        #target is end size, so last value
        if type == "endPredictSize":
            target = self.indivPlantVals[plant][-1][-1]
            output = self.outputLayerOut[plant]*self.growthFactor
        elif type == "dayPredictSize":
            #day isn't 0-30, but instead is only 0-15 for changes
            target = self.valueChanges[plant][-1][day]
            #new target is change in plant growth for that day based on that day's factors
            output = self.outputLayerOut[plant]*self.changeFactor 
        error = .5*(target-output)**2 #not needed, only to see results
        self.errors.append(error)
        errorWrtOuterOut = -(target-output)
        
        outerOutWrtOuterNet = output*(1-output) #only for logistic sigmoid activation fx
        outerNetWrtWeight = self.hiddenLayerOut[plant][neuronInc]
        errorWrtWeight = errorWrtOuterOut* outerOutWrtOuterNet* outerNetWrtWeight
        newWeight = self.outputWeights[plant][neuronInc]-\
                            (neuralNetwork.LEARNING_RATE*errorWrtWeight)
        self.newOutputWeights[plant].append(newWeight)
        print(self.newOutputWeights[plant])
        return errorWrtOuterOut,outerOutWrtOuterNet
    
    def updateHiddenWeights(self,type,plant,neuronInc,sensorInc,
                                    errorWrtOuterOut,outerOutWrtOuterNet,day=0):
        if type == "endPredictSize":
            input = Stats.calcMedian(self.indivPlantVals[plant][sensorInc])
        elif type == "dayPredictSize":
            input = self.indivPlantVals[plant][sensorInc+3][day]
        input = input - self.optVals[sensorInc]
        errorWrtOuterNet = errorWrtOuterOut*outerOutWrtOuterNet
        #simply the weight connected to it
        outerNetWrtHiddenOut = self.outputWeights[plant][neuronInc]
        errorWrtHiddenOut = errorWrtOuterNet * outerNetWrtHiddenOut
        
        #neuronInc b/c calculating effects of sensor weights for each neuron
        hiddenOut = self.hiddenLayerOut[plant][neuronInc]
        hiddenOutWrtHiddenNet = hiddenOut*(1-hiddenOut)
        hiddenNetWrtWeight = input
        errorWrtWeight = errorWrtHiddenOut* hiddenOutWrtHiddenNet* hiddenNetWrtWeight
        newWeight = self.hiddenWeights[plant][neuronInc][sensorInc]-\
                        neuralNetwork.LEARNING_RATE*errorWrtWeight
        self.newHiddenWeights[plant][neuronInc][sensorInc] = newWeight
        
    def updateAllWeights(self,plant):
        self.hiddenWeights[plant] = self.newHiddenWeights[plant]
        self.outputWeights[plant] = self.newOutputWeights[plant]
        
    def storeWeights(self,plant):
        species = plant[:-1] #species + number of instance
        filePath = "Plant_Data"+os.sep+species+"Optimal"
        #Folder = Plant_Data/Tomato/Tomato1/month
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        txtFile = filePath+os.sep+"Weights.txt"
        with open(txtFile, "wt") as f:
            #REMEMBER: STORING outputs weights separated by "," then right 
            #after ";" to separate the hidden weights
            outWeightString = ",".join(self.outputWeights)
            hiddenWeightString = ""
            for neuronInc in range(self.numNeurons):
                hiddenWeightString+= ",".join(str(sub) for sub in self.hiddenWeights[neuronInc]
            allLines = outWeightString + ";" + hiddenWeightString
            #[[1,2,3],[4,5,6]] --> "1,2,3,4,5,6"
            f.close() #erase data already stored in there, replace with new data
            f.write(allLines)
            
    def activeFunc(self,net):
        neuronOutput = 1/(1+math.e**(-net))
        return neuronOutput
        
    def main(self,type):
        error = []
        for plant in self.indivPlantVals:
            self.initializeNeuralNetwork(plant)
            self.initializeNewWeights(plant)
            self.calcHiddenNet(type,plant)
            self.calcHiddenOut(plant)
            self.calcOuterNet(plant)
            self.calcOuterOut(plant)
            error.append(sum(self.errors))
        return error
            
            
# test = Stats("Basil")
# test.main()
# learning = neuralNetwork(test.indivPlantVals,test.valueTypes,test.optVals)


# Updated Animation Starter Code



####################################
# customize these functions
####################################

def init(data):
    data.neuronNum = 3
    data.inputNum = 3
    data.sep = data.width/data.neuronNum
    data.d = 50
    data.timerCalled = 0
    data.species = "Basil"
    data.test = Stats(data.species)
    data.type = "dayPredictSize" #or endPredictSize
    data.test.main()
    data.learning = neuralNetwork(data.species,data.test.indivPlantVals,
                data.test.valueTypes,data.test.optVals,data.test.valueChanges)
    data.learning.initializeWeights()
    data.error = data.learning.main(data.type)
    data.plant = "Basil3"

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if event.char =="n": #next
        data.learning.main(data.type)
        for plant in data.learning.indivPlantVals:
            data.learning.backProp(data.type,plant)
            data.learning.updateAllWeights(plant)

def timerFired(data):
    data.timerCalled+= 1

def redrawAll(canvas, data):
    for row in range(data.neuronNum):
        start = data.d/2,row*data.sep+data.d/2
        for secondRow in range(data.neuronNum):
            end = data.sep+data.d/2,secondRow*data.sep+data.d/2
            canvas.create_line(start,end)
        for col in range(data.neuronNum-1):
            y0 = row*data.sep
            x0 = col*data.sep
            x1 = x0+data.d
            y1 = y0 + data.d
            canvas.create_oval(x0,y0,x1,y1,fill="pink")
            
            if col == 0:
                input = Stats.calcMedian(data.test.indivPlantVals[data.plant][row])
                input = input - data.test.optVals[row]
                text = "%.1f"%input
                canvas.create_text(x0+data.d/2,y0+data.d/2,
                        text=text)
                canvas.create_text(x0+data.d,y0+data.d,
                        text=data.learning.hiddenWeights[data.plant][row][col])
                        
            elif col ==1:
                text = "N%d"%row
                canvas.create_text(x0+data.d,y0+data.d,
                                        text=data.learning.outputWeights[data.plant][row])
                canvas.create_text(x0+data.d/2,y0+data.d/2,text=text)
            
            
    x0,y0 = 2*data.sep,data.sep,
    x1,y1 = 2*data.sep+data.d,data.sep+data.d
    canvas.create_oval(x0,y0,x1,y1,fill="pink")
    canvas.create_text(x0+data.d/2,y0+data.d/2,text="Out")
    canvas.create_text(x0+data.d,y0+data.d,text="%.1f"%data.test.indivPlantVals[data.plant][-1][-1])
    error = sum(data.error)
    canvas.create_text(x0,y0,anchor=NE,text=str(error))
    
        
        

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

run(500, 500)