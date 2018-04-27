import os  
import math  
#import matplotlib.pyplot as plt
from tkinter import *
from scipy.stats import norm
import random

class Stats(object):
    path = "Plant_Data"
    def __init__(self,species):
        self.species = species #call for every species, ex: Basil
        self.indivPlantVals = dict() #stores specific values for each plant
        self.allSensorVals = dict() #stores all sensor values
        self.valueChanges = dict() #stores rate of change of all values
        self.groupedPlants = dict() #two plant groups: high/low sensor med
        self.valueTypes = ["x","y","Day","Temp","Bright","Moist","Size"]
        self.startIndex = self.valueTypes.index("Temp")
        self.endIndex = self.valueTypes.index("Size")
        self.indexRange = self.endIndex - self.startIndex
        self.numVals = len(self.valueTypes)
        self.meanVals = [0]*(self.indexRange+1) #[medTemp,medBright,medMoist,medSize]
        self.optTemp = self.optBright = self.optMoist = 60
        self.optVals = [self.optTemp,self.optBright,self.optMoist]
        self.endGrowth = 0 
        self.allOutliers = []
        
    
    def main(self):
        self.getData()
        for plant in self.indivPlantVals:
            self.findAnomalies(plant)
        self.compareEachSensor()
    
    def getData(self):
        filePath = Stats.path+os.sep+self.species #Plant_Data/Basil
        for plant in os.listdir(filePath): #every plant instance
            if plant.startswith('.'): continue #ignore .DS_Store
            plantFolder = filePath+os.sep+plant
            contents = Stats.readFile(plantFolder+os.sep+"Data.csv")#read contents
            #sort data, calculate rates of change
            self.sortData(contents,plant)
            self.storeValueRates(plant)
        self.calcCollectiveMed()
        self.getOptimalVals()
            
    def sortData(self,contents,plant):
        #store every sensor value into self.allSensorVals for collective Mean calc
        #store each plant instance's sensor values into self.indivPlantVals
        self.indivPlantVals[plant] = [[0] for species in range(self.numVals)]
        lines = contents.split(";") #sorts data from csv file
        self.endYield = lines[-1]
        lines = lines[:-1] #don't include the end growth
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
        self.valueChanges[plant] = [[],[],[],[]]
        for sensorInc in range(self.indexRange+1): #difference+1 b/c include size
            allVals = self.indivPlantVals[plant][sensorInc+self.startIndex] 
            #grab data values
            for valInc in range(1,len(allVals)): 
                changePerDay = float(allVals[valInc])-float(allVals[valInc-1])
                
                #valueChanges only includes temp --> size
                self.valueChanges[plant][sensorInc].append(changePerDay)
                
    def calcCollectiveMed(self):#calculate collective Mean for each sensor
        #Temp --> 
        for sensorInc in range(self.indexRange+1):
            sensor = self.valueTypes[sensorInc+self.startIndex]
            #sort list of each sensor to calculate Mean
            meanVal = Stats.calcMean(self.allSensorVals[sensor])
            #self.meanVals only contains temp --> size
            self.meanVals[sensorInc] = meanVal
            
    def compareEachSensor(self):
        for sensorInc in range(self.indexRange):
            self.groupedPlants[sensorInc] = dict()
            
            #sort plants into two groups of sensor values below and above Mean
            lowerValPlants, higherValPlants = self.compareEachPlant(sensorInc)
            
            #for plants with higher than normal sensor value
            avgGrowthRate,avgEndSize = self.calcGrowthStats(higherValPlants)
            self.groupedPlants[sensorInc]["High"] = (higherValPlants,avgGrowthRate,avgEndSize)
            
            #plants with lower than normal sensor value
            avgGrowthRate,avgEndSize = self.calcGrowthStats(lowerValPlants)
            self.groupedPlants[sensorInc]["Low"] = (lowerValPlants,avgGrowthRate,avgEndSize)

    def compareEachPlant(self,sensorInc):
        #compare every Mean sensor value for every plant with collective Mean
        #higherVals and lowerVals constantly reset for each sensor
        higherValPlants = dict() #contain plants with sensor value higher than Mean
        lowerValPlants = dict()
        #sensor inc = 0,1,2
        for plant in self.indivPlantVals:
            
            #compare individual and collective meanVal
            meanVal = Stats.calcMean(self.indivPlantVals[plant][sensorInc+self.startIndex])
            difference = meanVal-self.meanVals[sensorInc]
            endSize = self.indivPlantVals[plant][-1][-1]
            if difference >= 0:
            #get % difference for weighing
                higherValPlants[plant] = (difference,endSize)
            else: 
                lowerValPlants[plant] = (difference,endSize)
        return lowerValPlants, higherValPlants

    def calcGrowthStats(self,group):
        #calc avg diff sensor value and growth rate for every plant in group
        sumGrowthRates = endGrowthSizes = 0
        avgDiff = 0
        count = 1
        for plant in group:
            #self.valueChanges: [[dtemps],....[dsizes]]
            
            allGrowthRates = self.valueChanges[plant][-1]
            growthRateMean = Stats.calcMean(allGrowthRates)
            
            sumGrowthRates += growthRateMean
            endGrowthSizes += self.indivPlantVals[plant][-1][-1]
            count+=1
        
        #get average growth rate and end size
        return sumGrowthRates/count, endGrowthSizes/count
    
    def findAnomalies(self,plant):
        #find anomalies in sensor data, look at growth at each instance
        startIndex = self.valueTypes.index("Temp")
        endIndex = self.valueTypes.index("Moist")
        difference = endIndex - startIndex
        for sensorInc in range(difference+1): 
        #Watch out, valueChanges contains not just sensor values, but unwanted things
            allData = self.valueChanges[plant][sensorInc]
            mean = Stats.calcMean(allData)
            stdDev = Stats.calcStdDev(allData,mean)
            lowerOutliers = [x for x in allData if (x < mean-2*stdDev)]
            highOutliers = [x for x in allData if (x > mean+2*stdDev)]
            self.allOutliers = lowerOutliers + highOutliers
            name = self.valueTypes[sensorInc+startIndex]
            for outlier in self.allOutliers:
                index = self.valueChanges[plant][sensorInc].index(outlier)
                growthRate = self.valueChanges[plant][-1][index]
                #diffGrowth is percent change in growth rate 
                diffGrowth = (growthRate-self.meanVals[-1])/(self.meanVals[-1])
                diffSensor = outlier - self.meanVals[sensorInc]
                #update optimal value by weighted difference in sensor value
                
                if outlier in lowerOutliers:
                    weight = len(lowerOutliers)/len(self.allOutliers)
                elif outlier in highOutliers:
                    weight = len(highOutliers)/len(self.allOutliers)
                # self.optVals[sensorInc] += diffSensor*diffGrowth*weight
                #print(plant,name,self.optVals[sensorInc])
            
            
                
                #Keep track of the day so you can circle it in red on a graph
                #Also keep track when growth of plant = 0, showing anomaly too
                
                
                
                
                
                
                
                
                
                
                
    
                
    def getOptimalVals(self):
        #grabs previously stored values if they exist
        #if they don't, just set them to the meanVal and store
        optFolder = Stats.path+os.sep+self.species+"Optimal"
        optFile = optFolder+os.sep+"optValues.txt"
        if os.path.exists(optFolder):
            if os.path.exists(optFile):
                values = Stats.readFile(optFile)
                if len(values.split(","))!=3: self.storeOptValue(optFile)
                self.optTemp, self.optBright, self.optMoist = values.split(",")
                self.optVals  = [float(self.optTemp),float(self.optBright),
                            float(self.optMoist)]
                self.storeOptValue(optFile)            
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
        startIndex = self.valueTypes.index("Temp")
        endIndex = self.valueTypes.index("Moist")
        difference = endIndex - startIndex
        for inc in range(difference+1):
            values += str(self.optVals[inc])
            values += ","
        return values[:-1]
        
    def storeOptValue(self,file):
        with open(file, "wt") as f:
            values = self.generateOptString()
            f.truncate()
            f.write(values)  
            
    
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()
    def calcMean(numList):
        return sum(numList)/len(numList)
        
    def calcStdDev(numList,mean):
        variance = 0
        for value in numList:
            variance+=(value-mean)**2
        return (variance/len(numList)-1)**0.5
        
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
    def __init__(self,species,indivPlantVals,valueTypes,optVals,valueChanges,meanVals):
        self.species = species
        self.indivPlantVals = indivPlantVals
        self.valueTypes = valueTypes
        self.optVals = optVals
        self.valueChanges = valueChanges
        self.meanVals = meanVals
        self.startIndex = self.valueTypes.index("Temp")#skip the location and date values
        self.sensorVals = self.valueTypes[self.startIndex:-1]
        self.numNeurons = len(self.sensorVals)
        self.hiddenBias = .5
        self.outerBias = .5
        #not sure what weights to predefine
        self.growthFactor = 5
        self.changeFactor = 2
        
    def initializeNeuralNetwork(self):
        self.hiddenLayerNet = [self.hiddenBias]*(self.numNeurons)
        self.hiddenLayerOut = [0]*(self.numNeurons) #result of active function of net
        self.outputLayerNet = self.outerBias #only one output, so no need for list
        self.outputLayerOut = 0
        self.errors = []
        self.outputs = dict()
        
    def initializeNewWeights(self):#store new weight values after backprop
        self.newOutputWeights = [] #need to append new weights
        self.newHiddenWeights = [[0]*self.numNeurons for i in range(self.numNeurons)] #need to destructively modify values
        
    def initializeWeights(self):
        self.outputWeights = [.5]*self.numNeurons
        self.hiddenWeights = [[.5]*self.numNeurons for i in range(self.numNeurons)]
        filePath = "Plant_Data"+os.sep+self.species+"Optimal"+os.sep+"Weights.txt"
        if os.path.exists(filePath):
            self.getExistingWeights(filePath)
            
    def getExistingWeights(self,filePath):
        contents = Stats.readFile(filePath)
        weightList = contents.split(";")
        #outerLayer weights
        weightStringOut= weightList[0]
        values = weightStringOut.split(",")
        for inc in range(len(values)):
            self.outputWeights[inc] = float(values[inc])
        #hidden layer weights
        weightStringHid = weightList[1]
        values = weightStringHid.split(",")
        for inc in range(len(values)):
            self.hiddenWeights[inc//self.numNeurons][inc%self.numNeurons] =\
                                                        float(values[inc])
    
    def main(self,type,plant):
        self.outputs[plant] = dict()
        if type == "dayPredictSize":
            for day in range(len(self.valueChanges[plant][-1])):
                self.initializeNeuralNetwork()
                self.initializeNewWeights()
                self.calcHiddenNet(type,plant,day)
                self.calcHiddenOut()
                self.calcOuterNet()
                self.calcOuterOut()
                self.backProp(type,plant,day)  
                self.updateAllWeights()
            #eventually store weight
        elif type == "endPredictSize":
            self.initializeNeuralNetwork()
            self.initializeNewWeights()
            self.calcHiddenNet(type,plant)
            self.calcHiddenOut()
            self.calcOuterNet()
            self.calcOuterOut()  
            self.backProp(type,plant)  
                      
    def calcHiddenNet(self,type,plant,day=0):
        #for each neuron, get each sensor input
        # plantCount = len(self.indivPlantVals)
        for neuronInc in range(self.numNeurons): #for every sensor input
            for sensorInc in range(self.numNeurons):
                if type == "endPredictSize":
                    #calculate individual plant's mean and compare with collecive mean
                    input = Stats.calcMean(self.indivPlantVals[plant][sensorInc+self.startIndex])
                elif type == "dayPredictSize":
                    input = self.indivPlantVals[plant][sensorInc+self.startIndex][day]
                input = input - self.optVals[sensorInc] #input is the diff from optimal
                #for every species, call the basic stats to get all stats
                #then for every plant, depending on type(day or overall), 
                #pass data into network, update weights
                
                #weight for every neuron and every input
                weight = self.hiddenWeights[neuronInc][sensorInc]
                netInput = weight*input
                #use neuronInc since add the input*weight of each sensor current net
                self.hiddenLayerNet[neuronInc]+=netInput
                
    def calcHiddenOut(self):
        for neuronInc in range(self.numNeurons):
            net = self.hiddenLayerNet[neuronInc]
            self.hiddenLayerOut[neuronInc]=self.activeFunc(net)
            
    def calcOuterNet(self):
        for neuronInc in range(self.numNeurons):
            weight = self.outputWeights[neuronInc]
            input = self.hiddenLayerOut[neuronInc]
            netInput = weight*input
            #only one output node, so just add all the hidden layer outputs
            self.outputLayerNet+=netInput
        
    def calcOuterOut(self):
        net = self.outputLayerNet
        self.outputLayerOut=self.activeFunc(net)
        
    def backProp(self,type,plant,day=-1):
        #one output weight for one neuron
        #3 input weights for each neuron b/c 3 sensor inputs
        for neuronInc in range(self.numNeurons):
            errorWrtOuterOut, outerOutWrtOuterNet=\
                self.updateOutputWeights(type,plant,neuronInc,day)
            for sensorInc in range(self.numNeurons):
                self.updateHiddenWeights(type,plant,neuronInc,sensorInc,
                                errorWrtOuterOut,outerOutWrtOuterNet,day)
        
    def updateOutputWeights(self,type,plant,neuronInc,day):
        #list of sizes is last
        #target is end size, so last value
        if type == "endPredictSize":
            target = self.indivPlantVals[plant][-1][day]
            output = self.outputLayerOut*self.growthFactor
        elif type == "dayPredictSize":
            ##DAYS ARE 0-28, so days-1, NOT !!!!!!!!!
            ##Weights for endPredictSize need to be stored in sep file, diff
            ##Can't predict end size b/c of way data generated by generating changes
            output = self.outputLayerOut*self.changeFactor 
            target = self.valueChanges[plant][-1][day]
            #new target is change in plant growth for that day based on that day's factors
            
        self.outputs[plant][day] = output #for endpredictsize, day = -1
        error = .5*(target-output)**2 #not needed, only to see results
        print(error)
        self.errors.append(error)
        errorWrtOuterOut = -1*(target-output)
        outerOutWrtOuterNet = output*(1-output) #only for logistic sigmoid activation fx
        outerNetWrtWeight = self.hiddenLayerOut[neuronInc]
        errorWrtWeight = errorWrtOuterOut* outerOutWrtOuterNet* outerNetWrtWeight
        newWeight = self.outputWeights[neuronInc]-\
                            (neuralNetwork.LEARNING_RATE*errorWrtWeight)
        self.newOutputWeights.append(newWeight)
        return errorWrtOuterOut,outerOutWrtOuterNet
    
    def updateHiddenWeights(self,type,plant,neuronInc,sensorInc,
                                    errorWrtOuterOut,outerOutWrtOuterNet,day):
        if type == "endPredictSize":
            #input is mean sensor value for that plant
            input = Stats.calcMean(self.indivPlantVals[plant][sensorInc+self.startIndex])
        elif type == "dayPredictSize":
            #input is the sensor value of that day
            input = self.indivPlantVals[plant][sensorInc+self.startIndex][day]
        input = input - self.optVals[sensorInc]
        errorWrtOuterNet = errorWrtOuterOut*outerOutWrtOuterNet
        #simply the weight connected to it
        outerNetWrtHiddenOut = self.outputWeights[neuronInc]
        errorWrtHiddenOut = errorWrtOuterNet * outerNetWrtHiddenOut
        
        #neuronInc b/c calculating effects of sensor weights for each neuron
        hiddenOut = self.hiddenLayerOut[neuronInc]
        hiddenOutWrtHiddenNet = hiddenOut*(1-hiddenOut)
        hiddenNetWrtWeight = input
        errorWrtWeight = errorWrtHiddenOut* hiddenOutWrtHiddenNet* hiddenNetWrtWeight
        newWeight = self.hiddenWeights[neuronInc][sensorInc]-\
                        neuralNetwork.LEARNING_RATE*errorWrtWeight
        self.newHiddenWeights[neuronInc][sensorInc] = newWeight
        
    def updateAllWeights(self):
        self.hiddenWeights = self.newHiddenWeights
        self.outputWeights = self.newOutputWeights
    #     
    # def getAverageWeights(self):
    #     plantCount = 0
    #     allHiddenWeights = [[0]*self.numNeurons for i in range(self.numNeurons)]
    #     allOutWeights = [0]*self.numNeurons
    #     for plant in self.indivPlantVals:
    #         plantCount += 1 #used to calculate average of all the weights
    #         for neuronInc in range(self.numNeurons):
    #             allOutWeights[neuronInc] += self.outputWeights[plant][neuronInc]
    #             for sensorInc in range(self.numNeurons):
    #                 allHiddenWeights[neuronInc][sensorInc]+=\
    #                             self.hiddenWeights[plant][neuronInc][sensorInc]
    #     #divide the sum of all weights by number to get average
    #     for neuronInc in range(self.numNeurons):
    #         allOutWeights[neuronInc] = str(allOutWeights[neuronInc]/plantCount)
    #         for sensorInc in range(self.numNeurons):
    #             allHiddenWeights[neuronInc][sensorInc] /= plantCount
    #     return allOutWeights, allHiddenWeights
        
    def storeWeights(self):
        filePath = "Plant_Data"+os.sep+self.species+"Optimal"
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
                for sensorInc in range(self.numNeurons):
                    hiddenWeightString+=str(self.hiddenWeights[neuronInc][sensorInc])
                    hiddenWeightString+=","
                    #WATCH OUT: end of the hidden string has extra comma, must remove
            allLines = outWeightString + ";" + hiddenWeightString[:-1]
            #[[1,2,3],[4,5,6]] --> "1,2,3,4,5,6"
            f.truncate() #erase data already stored in there, replace with new data
            f.write(allLines)
            
    def activeFunc(self,net):
        neuronOutput = 1/(1+math.e**(-net))
        return neuronOutput

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
        data.test.valueTypes,data.test.optVals,data.test.valueChanges,data.test.meanVals)
    data.learning.main(data.type)
    data.plant = "Basil0"
    data.day = 1
    
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
        outWeights, hiddenWeights= data.learning.getAverageWeights()
        data.learning.storeWeights(outWeights,hiddenWeights)
        
    elif event.char == "t":
        data.test.main()
    elif event.char == "c":#change plant
        plantNum = random.randint(0,20)
        data.plant = data.species+str(plantNum)

def timerFired(data):
    data.timerCalled+= 1

def redrawAll(canvas, data):
    data.day+=1
    data.day%=20
    for row in range(data.neuronNum):
        start = data.d/2,row*data.sep+data.d/2
        #sensorName = data.learning.valueTypes[row+data.learning.startIndex]
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
                input = data.learning.indivPlantVals[data.plant][row+data.learning.startIndex][data.day]
                input = input - data.test.optVals[row]
                tempValDiff = "%.1f"%input
                canvas.create_text(x0+data.d/2,y0+data.d/2,text=tempValDiff)
                weight = data.learning.hiddenWeights[row][col]
                canvas.create_text(x0+data.d,y0+data.d,text="%.1f"%weight)
                        
            elif col ==1:
                neuron = "N%d"%row
                weight = data.learning.outputWeights[row]
                canvas.create_text(x0+data.d,y0+data.d,text="%.1f"%weight)
                canvas.create_text(x0+data.d/2,y0+data.d/2,text=neuron)
            
    x0,y0 = 2*data.sep,data.sep,
    x1,y1 = 2*data.sep+data.d,data.sep+data.d
    canvas.create_oval(x0,y0,x1,y1,fill="pink")
    canvas.create_text(x0+data.d/2,y0+data.d/2,text="Out")
    # if data.learning.type == "dayPredictSize"
    # canvas.create_text(x0+data.d,y0+data.d,text="Actual:%.1f"%data.learning.valueChanges[data.plant][-1][day])
    # canvas.create_text(x0+data.d,y0+data.d,text="Output:%.1f"%data.learning.outputs[plant][day])
    # error = sum(data.learning.errors)
    # canvas.create_text(x0+data.d*3,y0,anchor=NE,text=str(error))

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

#run(500, 500)
# test = Stats("Basil")
# for i in range(10):
#     test.main()
test = Stats("Basil")
test.main()
learning = neuralNetwork(test.species,test.indivPlantVals,
        test.valueTypes,test.optVals,test.valueChanges,test.meanVals)
for plant in test.indivPlantVals:
    learning.main(type,plant)