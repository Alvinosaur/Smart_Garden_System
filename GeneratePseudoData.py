import math
import random
import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
import os

#TEST REFLECT SUMMER INC 
class GenData(tk.Frame):
    def __init__(self,days):
        self.days = days
        self.tempWeight = 0.2
        self.brightWeight = 0.2
        self.moistWeight = .1
        self.sinAmp = 3
        self.sinFreq = 0.35
        self.allTimes = []
        self.allTemps = []
        self.allBrights = []
        self.allMoists = []
        self.plantSizes = []
        self.medTemp = 60 #degrees Fahrenheit
        self.startBright = 70 #lumens?
        self.startMoist = 50
        self.fluct=3
        self.graphLegend = 1, 0.5 #proportion of page where legend begins

    def synthData(self):
        self.allTimes = []
        self.allTemps = []
        self.allMoists = []
        self.allBrights = []
        self.plantSizes = []
        for day in range(self.days): #30 days in a month
            dayTemp= self.randTemp(day,type)
            tempDiff = dayTemp-self.medTemp
            dayBright = self.randBright(day,tempDiff,type)
            brightDiff = dayBright - self.startBright
            dayMoist = self.randMoist(day,tempDiff,dayBright,type)
            moistDiff = dayMoist - self.startMoist
            size = self.incPlantSize(day,tempDiff,brightDiff,moistDiff,type)
            line = [day]
            self.allTimes.append(day)
            self.allTemps.append(dayTemp)
            self.allMoists.append(dayMoist)
            self.allBrights.append(dayBright)
            self.plantSizes.append(size)
        
            
    def randTemp(self,day,type):
        fluct = GenData.randFluct(self.fluct)
        dayTemp = self.sinAmp*math.sin(self.sinFreq*day)+self.medTemp+\
                                fluct+GenData.gradInc(day,type)
        return dayTemp
        
    def randBright(self,day,tempDiff,type):#brightness can be partly based off temp
        fluct = GenData.randFluct(self.fluct)
        dayBright = self.startBright+self.sinAmp*math.sin(self.sinFreq*day+5)+\
                        fluct+GenData.gradInc(day,type)+tempDiff*self.tempWeight
        return dayBright
        
    def randMoist(self,day,tempDiff,brightDiff,type):
        fluct = GenData.randFluct(self.fluct)
        dayMoist = self.startMoist-GenData.gradInc(day,type)-\
                tempDiff*self.tempWeight - brightDiff*self.brightWeight
        return dayMoist
        
    def incPlantSize(self,day,tempDiff,brightDiff,moistDiff,type):
        M= random.randint(16,20)
        k = .2
        z = random.randint(18,22)
        y0 = random.randint(3,4)
        size = GenData.gradInc(day,type,M,k,z,y0)+\
            tempDiff*self.tempWeight*.5 +brightDiff*self.brightWeight + \
                moistDiff*self.moistWeight
        return size
        
    def plotData(self):
        self.synthData()
        #plt.plot(self.allTimes,self.sizes)
        plt.plot(self.allTimes,self.allTemps,label="Temperature(F)",color="red")
        plt.plot(self.allTimes,self.allMoists,label="Moisture(m^3/m^3)",color="blue")
        plt.plot(self.allTimes,self.allBrights,label="Brightness",color="gold")
        plt.plot(self.allTimes,self.plantSizes,label="Plant Size",color="green")
        plt.hist(self.allTemps,50)
        plt.xlabel('Time')
        plt.ylabel('Plant Growth, Sensor Values')
        plt.legend(bbox_to_anchor=(self.graphLegend), loc=1, borderaxespad=0.)
        plt.show()
    
    # def plantGrowth(self,day,dayTemp,tempDiff,dayBright,brightDiff,
    #             dayMoist,moistDiff):#hot weather, high moisture, less brightness
    #     mainGrowth = gradInc(day,M=20,k=1,z=5,y0=0)
    # #have a class of different plants with different initial preferences,
    #     #orchids would have target preference of higer temp,
    def createData(self,species,name,type):
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
        filePath = "Plant_Data"+os.sep+species+os.sep+name
        #Folder = Plant_Data/Tomato/Tomato1/month
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        csvFile = filePath+os.sep+"Data.csv"
        with open(csvFile, "wt") as f:
            f.write(allLines)  
    def main(self):
        species = "Basil"
        for count in range(10):
            name = species+str(count)
            test.createData(species,name,"low")
        for count in range(10,20):
            name = species+str(count)
            test.createData(species,name,"high")
    @staticmethod
    def randFluct(range):
        return random.randint(-range,range)
        
    def gradInc(day,type,M = 10,k = 0.1,z = 6.2,y0 = 3.5):
        deno = 1+math.e**(-k*(day-z))
        result = (M/deno)-y0
        if type == "low": return -result
        else: return result

test = GenData(31)
test.main()
# test.plotData()
