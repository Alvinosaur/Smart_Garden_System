import os    

class analyzeData(object):
    path = "Plant_Data"
    def __init__(self,type):
        self.type = type #call for every species, ex: tomato
        self.allTimes = [] 
        self.indivPlantVals = dict() #stores specific sensor values for each plant
        self.allSensorVals = dict() #stores all sensor values
        self.valueChanges = dict() #stores rate of change of all values
        self.valueTypes = ["Temp","Bright","Moist","Size"]
        self.numVals = len(self.valueTypes)
        self.medVals = []*self.numVals #self.medVals = [medTemp,medBright,medMoist,medSize]
        self.optVals = []*(self.numVals-1) #not including size
        self.optTemp = self.optBright = self.optMoist = 0 
        self.midIndex = 0
        
    
    def getData(self):
        filePath = analyzeData.path+os.sep+self.type #Plant_Data/Tomato
        for plant in os.listdir(filePath): #every plant instance
            plantFolder = filePath+os.sep+plant
            #read contents
            contents = analyzeData.readFile(plantFolder+os.sep+"Data.csv")
            #sort data, run calculations
            self.sortData(contents,plant)
            self.storeValueRates(plant)
        self.calcCollectiveMed()
        self.getOptimalVals()
    
    def getOptimalVals(self):
        optFolder = analyzeData.path+os.sep+self.type+"Optimal"
        if os.path.exists(optFolder):
            values = analyzeData.readFile(optFolder+os.sep+"optValues.txt")
            self.optTemp, self.optBright, self.optMoist = values.split(",")
            self.optVals  = float(self.optTemp),float(self.optBright),float(self.optMoist)
        else:
            os.path.makedirs(optFolder+os.sep+"optValues.txt")
            self.optTemp = self.medVals[0]
            self.optBright = self.medVals[1]
            self.optMoist = self.medVals[2]
            
    
    def sortData(self,contents,plant):
        #store every sensor value into self.allSensorVals for collective median calc
        #store each plant instance's sensor values into self.indivPlantVals
        self.indivPlantVals[plant] = [[] for type in range(self.numVals)]
        lines = contents.split(";")
        for line in lines:
            sepVals = line.split(",")
            #x,y missing
            #day,temp,light,moist,size = sepVals
            for valueInc in range(self.valueTypes):
                sensor = self.valueTypes[valueInc]
                value = sepVals[valueInc+1] #don't include day
                if self.allSensorVals.get(sensor,0) != 0: #if not empty
                    self.allSensorVals[sensor].append(value)
                else:
                    self.allSensorVals[sensor] = [value]
                #every plant has dict of sensors with datapoints in a list
                self.indivPlantVals[plant][valueInc].append(value)
                
    def calcCollectiveMed(self):#calculate collective median for each sensor
        for sensorInc in range(self.numVals):
            sensor = self.valueTypes[sensorInc]
            #sort list of each sensor to calculate median
            self.allSensorVals[sensor].sort()
            medVal = self.calcMedian(self.allSensorVals[sensor])
            self.medVals[sensorInc] = medVal
            
    # def compareEachSensor(self):
    #     for sensorInc in range(self.numVals):
    #         self.compareEachPlant(sensorInc) #gets 
    #         highGrowthTot = lowGrowthTot= 0
    #         count = 0
    #         weightedHighAvg,weightedHighTot = self.calcGrowthStats(self.higherVals)
    #         weightedLowAvg,weightedLowTot = self.calcGrowthStats(self.lowerVals)
    #         
    #         if highGrowthAvg > lowGrowthAvg:
    #             self.results[self.valueTypes[sensorInc]] = "Higher"
    #         else:
    #             self.results[self.valueTypes[sensorInc]] = "Lower"
#     HOW TO BEST ANALYZE THIS DATA??????
                
    def compareEachPlant(self,sensorInc):
        #compare every med sensor value for every plant 
        #higherVals and lowerVals constantly reset for each sensor
        self.higherVals = dict()
        self.lowerVals = dict()
        for plant in self.indivPlantVals:
            medVal = self.calcMedian(self.indivPlantVals[plant][sensorInc])
            #compare individual and collective median
            difference = medVal-self.medVals[sensorInc]
            if difference >= 0: 
            #get % difference for weighing
                self.higherVals[plant]=abs(difference)/self.medVals[sensorInc]
            else: 
                self.lowerVals[plant] = abs(difference)/self.medVals[sensorInc]
            
    def calcGrowthStats(self,group):
        sumGrowthRates = 0
        growthTotal = 0
        for plant in group:
            #calc avg growth rate, all weighted, so not accurate numbers
            growthVals = self.valueChanges[plant][3]
            growthMed = self.calcMedian(growthVals)
            sumGrowthRates += growthMed*group[plant]
            startGrowth = growthVals[0]
            endGrowth = growthVals[-1]
            weightedGrowthTotal += (endGrowth - startGrowth)*group[plant] #multiply with weight
            count+= 1
        weightedGrowthRateAvg = sumGrowthRates/count #not real growth rate average, weighted version
        return (weightedGrowthRateAvg,weightedGrowthTotal)
    
    def calcMedian(self,curList):
        self.midIndex = len(curList)//2
        if len(curList)%2 == 0:
            #take average of two middle values
            medVal = (curList[midIndex]+curList[midIndex-1])/2
        else:
            medVal = curList[midIndex]
        return medVal
        
    def storeValueRates(self,plant):
        #stores rate of change of all sensor values, including size
        self.valueChanges[plant] = [[] for type in range(self.numVals)]
        for sensorInc in range(len(self.numVals)):
            allVals = self.indivPlantVals[plant][sensorInc] #grab sensor values
            for valInc in range(1,len(allVals)): 
                changePerDay = allVals[valInc]-allVals[valInc-1]
                self.valueChanges[plant][sensorInc].append(changePerDay)
            
    def findAnomalies(self,plant):
        #find anomalies in sensor data, look at growth at each instance
        for sensorInc in range(len(self.numVals)-1): #don't include growth rate
            allData = self.valueChanges[plant][sensorInc]
            mean = analyzeData.calcMean(allData)
            stdDev = analyzeData.calcStdDev(allData,mean)
            lowerOutliers = [x for x in allData if (x < mean-2*stdDev)]
            highOutliers = [x for x in allData if (x > mean+2*stdDev)]
            allOutliers = lowerOutliers + highOutliers
            for outlier in allOutliers:
                index = self.valueChanges[plant][sensorInc].index(outlier)
                growthRate = self.valueChanges[plant][3][index]
                #diffGrowth is percent change in growth rate 
                diffGrowth = (growthRate-self.medVals[3])/(self.medVals[3])
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
        variance = sum([[value - mean]**2 for value in numList])
        return variance**0.5
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
                
def main():
    test = analyzeData("Basil")
    test.getData()
    test.compareEachSensor()
    test.findAnomalies()
    
#main()