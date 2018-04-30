import math
import random
# import matplotlib.pyplot as plt
#matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# from matplotlib.figure import Figure
# import tkinter as tk
# from tkinter import ttk
import os
from scipy.stats import norm
import pandas as pd
from sklearn import linear_model

#TEST REFLECT SUMMER INC 
class GenData(object):
    def __init__(self,days=30,plant="Kale",type="Train",testerValues=[]):
        self.days = days
        self.plant = plant
        self.testerValues = testerValues
        self.type = type #Train or Test
        
        if self.testerValues != []:
            #need to initialize with GenData(.....)
            self.medTemp, self.medBright, self.medMoist = self.testerValues
        else:
            self.medTemp = 50 
            self.medBright = 40
            self.medMoist = 20
        
        self.tempData = dict()
        self.tempData["Temp"] = []
        self.tempData["sizeChange"] = []
        
        self.brightData = dict()
        self.brightData["Bright"] = []
        self.brightData["sizeChange"] = []
        
        self.moistData = dict()
        self.moistData["Moist"] = []
        self.moistData["sizeChange"] = []
        
        self.initfunctionParams()
        
    def initfunctionParams(self):
        self.tempWeight = 0.2
        self.brightWeight = 0.2
        self.moistWeight = .1
        self.sinAmp = 4
        self.sinFreq = 0.4
        self.fluct=4
        self.graphLegend = 1, 0.5 #proportion of page where legend begins
        self.growthFactor = 10
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
            brightDiff = dayBright - self.medBright
            dayMoist = self.randMoist(day,tempDiff,dayBright)
            moistDiff = dayMoist - self.medMoist
            tempFactor,brightFactor,moistFactor = self.incPlantSize(day,dayTemp,
                                                            dayBright,dayMoist)
            #self.allTimes.append(day)
            self.tempData["Temp"].append(dayTemp)
            self.tempData["sizeChange"].append(tempFactor)
            
            self.moistData["Moist"].append(dayMoist)
            self.moistData["sizeChange"].append(moistFactor)
            
            self.brightData["Bright"].append(dayBright)
            self.brightData["sizeChange"].append(brightFactor)
            
        
    def storeData(self):
        csvDataTemp = pd.DataFrame(self.tempData,columns=["Temp","sizeChange"])
        csvDataBright = pd.DataFrame(self.brightData,columns=["Bright","sizeChange"])
        csvDataMoist = pd.DataFrame(self.moistData,columns=["Moist","sizeChange"])
        if not os.path.exists(self.plant+"Data"):
            os.makedirs(self.plant+"Data")
        csvDataTemp.to_csv(self.plant+"Data"+os.sep+"%sTemp.csv"%self.type)
        csvDataBright.to_csv(self.plant+"Data"+os.sep+"%sBright.csv"%self.type)
        csvDataMoist.to_csv(self.plant+"Data"+os.sep+"%sMoist.csv"%self.type)
            
            
    def randTemp(self,day):
        fluct = self.randFluct(self.fluct)
        dayTemp = self.sinAmp*math.sin(self.sinFreq*day)+self.medTemp+\
                                fluct
        return dayTemp
        
    def randBright(self,day,tempDiff):#brightness can be partly based off temp
        fluct = self.randFluct(self.fluct)
        dayBright = self.medBright+self.sinAmp*math.sin(self.sinFreq*day+5)+\
            fluct
        return dayBright
        
    def randMoist(self,day,tempDiff,brightDiff):
        fluct = self.randFluct(self.fluct)
        dayMoist = self.medMoist+self.sinAmp*math.sin(self.sinFreq*day+10)+fluct*2
        return dayMoist
        
    def incPlantSize(self,day,dayTemp,dayBright,dayMoist):
        tempFactor = self.growthRate(dayTemp,self.medTemp//10)
        brightFactor= self.growthRate(dayBright,self.medBright//10)
        distribution = norm(self.medMoist,3)
        moistFactor = 1/math.log(distribution.pdf(dayMoist)) 
        return tempFactor,brightFactor,abs(moistFactor)
        
    # def gradInc(self,day,M = 10,k = 0.01,z = 6.2,y0 = 3.5):
    #     deno = 1+math.e**(-k*(day-z))
    #     result = (M/deno)-y0
    #     return result
        
    def growthRate(self,value,z,M = 4,k = 0.1):
        deno = 1+math.e**(-k*(value)+z)
        result = (M/deno)
        return result
        
    def linReg(self):
        for factor in ["Temp","Bright","Moist"]:
            dataTrain = pd.read_csv(self.plant+"Data"+os.sep+"Train%s.csv"%factor)
            dataTest = pd.read_csv(self.plant+"Data"+os.sep+"Test%s.csv"%factor)
            
            xTrain = dataTrain[factor].values.reshape(-1,1)
            yTrain = dataTrain['sizeChange']
            
            xTest = dataTest[factor].values.reshape(-1,1)
            yTest = dataTest['sizeChange']
            
            linRegModel = linear_model.LinearRegression()
            predictedModel = linRegModel.fit(xTrain,yTrain)
            yPredict = predictedModel.predict(xTest)
            print(factor,yPredict.item(0))
        #
        # plt.scatter(xTest,yTest,color='black')
        # plt.plot(xTest,yPredict,color='blue', linewidth=3)
    @staticmethod
    def randFluct(range):
        return random.randint(-range,range)
#def __init__(self,days,plant,testerValues=[]
dataTest = GenData(1000,"Dill","Train",[40,20,30])
dataTest.synthData()
dataTest.storeData()
# 
# #dataTrain = GenData(1000,"Kale",[40,50,60],"Train")
# # dataTrain.synthData()
# # dataTrain.storeData()
# 
# dataTest.linReg()
#need to change so bigger difference in growth rates


