import os  
import math  

class Stats(object):
    path = "Plant_Data"
    LEARNING_RATE = 0.5
    def __init__(self,type):
        self.type = type #call for every species, ex: Basil
        self.indivPlantVals = dict() #stores specific values for each plant
        self.allSensorVals = dict() #stores all sensor values
        self.valueChanges = dict() #stores rate of change of all values
        self.groupedPlants = dict()
        self.valueTypes = ["x","y","Day","Temp","Bright","Moist","Size"]
        self.numVals = len(self.valueTypes)
        self.medVals = [0]*self.numVals #[day,medTemp,medBright,medMoist,medSize]
        self.optTemp = self.optBright = self.optMoist = 0  
    
    def getData(self):
        filePath = Stats.path+os.sep+self.type #Plant_Data/Basil
        for plant in os.listdir(filePath): #every plant instance
            if plant.startswith('.'): continue #ignore .DS_Store
            plantFolder = filePath+os.sep+plant
            contents = Stats.readFile(plantFolder+os.sep+"Data.csv")#read contents
            #sort data, calculate rates of change
            self.sortData(contents,plant)
            self.storeValueRates(plant)
            
    def sortData(self,contents,plant):
        #store every sensor value into self.allSensorVals for collective median calc
        #store each plant instance's sensor values into self.indivPlantVals
        self.indivPlantVals[plant] = [[0] for type in range(self.numVals)]
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
                    self.allSensorVals[sensor] = [value]
                #every plant has dict of sensors with datapoints in a list
                self.indivPlantVals[plant][valueInc].append(value)
                
    def storeValueRates(self,plant):
        #stores rate of change of all sensor values, including size
        self.valueChanges[plant] = [[] for type in range(self.numVals)]
        for sensorInc in range(self.numVals):
            allVals = self.indivPlantVals[plant][sensorInc] #grab data values
            for valInc in range(1,len(allVals)): 
                changePerDay = float(allVals[valInc])-float(allVals[valInc-1])
                self.valueChanges[plant][sensorInc].append(changePerDay)
                #includes change in day, just ignore this
                
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
        growthTotal = 0
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
        optFolder = Stats.path+os.sep+self.type+"Optimal"
        optFile = optFolder+os.sep+"optValues.txt"
        if os.path.exists(optFolder):
            if os.path.exists(optFile):
                values = Stats.readFile(optFile)
                self.optTemp, self.optBright, self.optMoist = values.split(",")
                self.optVals  = float(self.optTemp),float(self.optBright),float(self.optMoist)
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
            
    def findAnomalies(self,plant):
        #find anomalies in sensor data, look at growth at each instance
        self.storeValueRates(plant)
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
        
    def calcMedian(sorted(curList)): #takes in sorted list, doesn't modify original
        midIndex = len(curList)//2
        if len(curList)%2 == 0:
            #take average of two middle values
            medVal = (curList[midIndex]+curList[midIndex-1])/2
        else:
            medVal = curList[midIndex]
        return medVal

# class neuralNetwork(object):
#     def __init__(self,):
#         self.hiddenLayerNet = self.hiddenLayerOut = dict()
#         self.outputLayerNet = self.outputLayerOut = dict()
#         self.hiddenWeights = self.outputWeights = dict()
#         self.weights = [.5]*(self.numNeurons)
#         self.hiddenBias = .5
#         self.outerBias = .5
#         #not sure what weights to predefine
#         self.numNeurons = self.numVals-1
#         self.optVals = [0]*(self.numNeurons) #not including size
#         
#     def initializeNeuralNetwork(self,plant):
#         self.hiddenLayerNet[plant]= [0]*(self.numNeurons)+[self.hiddenBias]
#         self.hiddenLayerOut[plant]= [0]*(self.numNeurons)
#         self.outputLayerNet[plant]= self.outerBias
#         self.outputLayerOut[plant]= 0
#         self.hiddenWeights[plant] = [[.5]*self.numNeurons for i in range(self.numVals)]
#         self.outputWeights[plant] = [.5]*self.numNeurons
#         
#     def calcHiddenNet(self,input,sensorInc,plant):
#         self.hiddenWeights[plant] = [[.5]*self.numNeurons for i in range(self.numVals)]
#         plantCount = len(self.indivPlantVals)
#         for neuronInc in range(self.numNeurons):
#             weightList = self.hiddenWeights[plant][sensorInc]
#             #1/20 plants??'
#             weight = self.hiddenWeights[plant][sensorInc][neuronInc]
#             netInput = weight*(1/plantCount)*input
#             self.hiddenLayerNet[plant][neuronInc]=netInput
#         
#     def calcHiddenOut(self,plant):
#         net = self.hiddenLayerNet[plant][0] 
#         for neuronInc in range(self.numNeurons):
#             self.hiddenLayerOut[plant][neuronInc]=self.activeFunc(net)
#             
#     def calcOuterNet(self,input,plant,neuronInc):
#         weight = self.outputWeights[neuronInc]
#         netInput = weight*(1/self.plantCount)*input
#         self.outerLayerNet[plant]+=netInput
#         
#     def calcOuterOut(self,plant):
#         net = self.outerLayerNet[plant]
#         self.outerLayerOut[plant]=activeFunc(net)*50 #*50 ????
#         
#     def backProp(self,sensorInc,plant):
#         for weightIndex in range(len(self.hiddenWeights[plant][sensorInc])):
#             updateWeight(self,plant,weightIndex)
#     
#     
#     def updateWeight(self,plant,weightIndex,sensorInc):
#         target = self.indivPlantVals[plant][3][-1]
#         output = self.outerLayerOut[plant]
#         error = .5(target-output)**2
#         errorWrtOuterOut = -(target-output)
#         outerOutWrtOuterNet = output(1-output)
#         outerNetWrtWeight = self.hiddenLayerOut[plant][weightIndex]
#         errorWrtWeight = errorWrtOuterOut*outerOutWrtOuterNet*outerNetWrtWeight
#         self.hiddenWeights[plant][sensorInc][weightIndex] -= \
#                         Stats.LEARNING_RATE*errorWrtWeight
    #def update optimal
    
    def activeFunc(self,net): #Change this, not sure which to pick
        neuronOutput = 1/(1+math.e**(-net))
        return neuronOutput

def main():
    test = Stats("Basil")
    test.getData()
    test.calcCollectiveMed()
    test.compareEachSensor()
    test.getOptimalVals()
    test.findAnomalies()
    
main()



    # def 
    #     lines = contents.split("\n")
    #     dailyVals = dict()
    #     for line in lines:
    #         values = line.split(",")
    #         date,x,y,size,temp,moist,light = values
    #         loc = (float(x),float(y))
    #         dailyVals[date]=[loc,size,float(temp),float(moisture),float(light)]
    #         self.compMedian(...)   

    # def searchFolders(self):
    #     for species in os.listdir(path): #path = Plant_Data
    #         newPath = path+os.sep+species
    #         for plant in os.listdir(newPath):
    #             subPath = newPath+os.sep+plant
    #             for file in os.listdir(subPath):
    #                 getData(self,subPath,plant,species)
    #             self.plantVals[plant]=dailyVals
    #         self.speciesVals[species]=self.plantVals[plant]