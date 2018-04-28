import math
import random
import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import os
from scipy.stats import norm

#TEST REFLECT SUMMER INC 
class GenData(tk.Frame):
    def __init__(self,days,type, season):
        data.season = season #winter, summer, spring, fall
        self.days = days
        self.tempWeight = 0.2
        self.brightWeight = 0.2
        self.moistWeight = 0.1
        self.sinAmp = 4
        self.sinFreq = 0.4
        self.medTemp = 72 #degrees Fahrenheit
        self.startBright = 50 #lumens?
        self.startMoist = 45
        self.fluct=7
        self.graphLegend = 1, 0.5 #proportion of page where legend begins
        self.stdDevs = [4,14,7]
        self.type = type
        self.growthFactor = 25
        self.prodYield = 0
        
    def synthData(self):
        self.allTimes = []
        self.allTemps = []
        self.allMoists = []
        self.allBrights = []
        self.plantSizes = [0]
        for day in range(self.days): #30 days in a month
            dayTemp= self.randTemp(day)
            tempDiff = dayTemp-self.medTemp
            dayBright = self.randBright(day,tempDiff)
            brightDiff = dayBright - self.startBright
            dayMoist = self.randMoist(day,tempDiff,dayBright)
            moistDiff = dayMoist - self.startMoist
            sensorValues = [tempDiff,brightDiff,moistDiff]
            size = self.incPlantSize(day,sensorValues)
            line = [day]
            self.allTimes.append(day)
            self.allTemps.append(dayTemp)
            self.allMoists.append(dayMoist)
            self.allBrights.append(dayBright)
            if self.plantSizes == [0]:
                self.plantSizes = [size]
            else:
                self.plantSizes.append(size)
            
    def randTemp(self,day):
        randomFactor = random.randint(0,2)
        fluct = self.randFluct(self.fluct)
        dayTemp = self.sinAmp*math.sin(self.sinFreq*day)+self.medTemp+\
                                fluct+self.gradInc(day)
        return dayTemp
        
    def randBright(self,day,tempDiff):#brightness can be partly based off temp
        fluct = self.randFluct(self.fluct)
        dayBright = self.startBright+self.sinAmp*math.sin(self.sinFreq*day+5)+\
            fluct+self.gradInc(day)
        return dayBright
        
    def randMoist(self,day,tempDiff,brightDiff):
        fluct = self.randFluct(self.fluct)
        dayMoist = self.startMoist-tempDiff*self.tempWeight - brightDiff*self.brightWeight- self.gradInc(day)
        return dayMoist
        
    def incPlantSize(self,day,sensorValues):
        prevSize = self.plantSizes[day-1]
        change = 1
        for sensorInc in range(len(sensorValues)):
            stdDev = self.stdDevs[sensorInc]
            distribution = norm(0,stdDev) #mean/optimal difference is 0
            optimality = 1/math.log(distribution.pdf(abs(sensorValues[0])))
            change *= abs(optimality)
        newSize = prevSize + change*self.growthFactor
        return newSize
    def cropYield(self,day):
        #some complex function to make it harder for network to learn
        endGrowth = self.plantSizes[day]
        self.prodYield = (.075*endGrowth)**6
        self.prodYield //= 1 #can't have non-int number of produce
        
    def plotData(self):
            plt.plot(self.allTimes,self.allTemps,label="Temperature(F)",color="red")
            plt.plot(self.allTimes,self.allMoists,label="Moisture(m^3/m^3)",color="blue")
            plt.plot(self.allTimes,self.allBrights,label="Brightness",color="gold")
            plt.plot(self.allTimes,self.plantSizes,label="Plant Size",color="green")
            plt.plot(self.allTimes,[self.prodYield]*self.days,color="purple")
        # else:
        #     plt.plot(self.allTimes,self.allTemps,color="red")
        #     plt.plot(self.allTimes,self.allMoists,color="blue")
        #     plt.plot(self.allTimes,self.allBrights,color="gold")
        #     plt.plot(self.allTimes,self.plantSizes,color="green")
        # self.count+=1
        #plt.plot(self.allTimes,self.sizes)
        
    
    # def plantGrowth(self,day,dayTemp,tempDiff,dayBright,brightDiff,
    #             dayMoist,moistDiff):#hot weather, high moisture, less brightness
    #     mainGrowth = gradInc(day,M=20,k=1,z=5,y0=0)
    # #have a class of different plants with different initial preferences,
    #     #orchids would have target preference of higer temp,
    def createData(self,species,name):
        self.synthData()
        allLines = ""
        for day in range(self.days):
            temp = self.allTemps[day]
            light = self.allBrights[day]
            moist = self.allMoists[day]
            size = self.plantSizes[day]
            x,y = random.randint(0,55),random.randint(0,55) #centimeters
            line = "%d,%d,%d,%.1f,%.1f,%.1f,%.1f;"%(x,y,day,temp,light,moist,size)
            allLines += line
            if day == (self.days-1): #final day, calculate overall yield
            #separate last item with ;
                allLines += str(self.cropYield(day))
        self.plotData()
        filePath = "Plant_Data"+os.sep+species+os.sep+name
        #Folder = Plant_Data/Tomato/Tomato1/month
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        csvFile = filePath+os.sep+"Data.csv"
        with open(csvFile, "wt") as f:
            f.write(allLines)  
            
    def gradInc(self,day,M = 10,k = 0.1,z = 6.2,y0 = 3.5):
        deno = 1+math.e**(-k*(day-z))
        result = (M/deno)-y0
        if self.type == "low": return -1*result
        elif self.type == "high": return result
        
    def growthRate(self,value,M = 2,k = 0.1,z = 6):
        deno = 1+math.e**(-k*(value)+z)
        result = (M/deno)
        return result
            
    def main(self):
        species = "Kale"
        #starts off initially high
        for count in range(10):
            name = species+str(count)
            test.createData(species,name)
        self.type = "low"
        for count in range(10,20):
            name = species+str(count)
            test.createData(species,name)
        plt.xlabel('Time')
        plt.ylabel('Plant Growth, Sensor Values')
        plt.legend(bbox_to_anchor=(self.graphLegend), loc=1, borderaxespad=0.)
        plt.show()
        
    @staticmethod
    def randFluct(range):
        return random.randint(-range,range)

test = GenData(31,"high")
test.main()
