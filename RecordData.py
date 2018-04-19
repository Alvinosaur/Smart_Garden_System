import os
import random
import math
import serial
import RPi.GPIO as GPIO
import time

class StoreData(object):
    path = "Plant_Data"
    def __init__(self,type,count):
        self.numVals
        self.type = type
        self.count = count
        self.hour = 0
        self.data = []
        
    def readArduino():
        ser=serial.Serial("/dev/ttyACM0",9600)#ACM will be diff
        ser.baudrate = 9600
        inputRead = ser.readline().decode("utf-8")
        formatData(inputRead)
        
    def formatData(self,inputRead):
        #sensorset0, 1, 2
        #each set comes with 
        inputRead[:-2]
        getTime = inputRead.split("|")
        self.hour = int(getTime.pop(0))
        allVals = getTime.split(";")
        for valueSet in allVals:
            values = valueSet.split(",")
            if len(values) < self.numVals:
                continue
            self.data.append(values)
            self.data.append("\n")
    
    def writeFile(self,path):
        path = path+ os.sep+"Data.csv"
        contents = "".join(self.data)
        with open(path, "wt") as f:
            f.write(contents)    
    def fillFolder(self,filePath,depth=0):
        if os.path.exists(filePath):
            if depth ==0:
                filePath = StoreData.path+os.sep+self.type+os.sep+str(self.count)
                self.fillFolder(filePath,depth+1)
            else:
                self.writeFile(filePath)
        else:
            os.makedirs(filePath)
            self.writeFile(filePath)
    
    
    
    
    
    def readFile(self,path):
        with open(path, "rt") as f:
            return f.read()
    
    def getData(self,subPath):
        contents = readFile(subPath)
        lines = contents.split("\n")
        for line in lines:
            values = line.split(";")
         
    def analyzeData(self):
        for speciesFile in os.listdir(path): #path = Plant_Data
            for plant in os.listdir(path+os.sep+speciesFile):
                newPath = path+os.sep+speciesFile
                for file in os.listdir(newPath+os.sep+plant):
                    subPath = newPath+os.sep+plant
                    data = getData(self,subPath)

        #for i in range(len(self.temps)):
            #diff = self.temps[i] - self.medTemp
            #if diff < 0:
                #coolPlants.append(
        
        
# class GenData(object):
#     def __init__(self,type,count):
#         self.type = type
#         self.count = count
#         self.temps = []
#         self.lights = []
#         self.moists = []
# 
#     def getData(self):
#         with open(path+os.sep+"dataLog"+os.sep+"%s"%self.type,"rt") as f:
#             file = f.read()
#             lines = file.split("\n")
#             for line in lines:
#                 values = line.split(",")
#                 date, time, size, moisture, light = values #time by the hour
#                 self.times.append(time)
#                 #self.allValues[date]= [time,[size,moisture,light]]
#     
#     def plotData(self):
#         plt.plot(self.times,self.sizes)
#         plt.plot(self.times,self.moistures)
#         plt.plot(self.times,self.lights)
#         plt.xlabel('Time')
#         plt.ylabel('Plant Growth, Sensor Values')
#         plt.show()
        

#Iris1 = StoreData(s,"Iris",1)
#Iris1.fillFolder(StoreData.path+os.sep+Iris1.type)

        
    
    def getData(self):
        with open(path+os.sep+"dataLog"+os.sep+"%s"%self.type,"rt") as f:
            file = f.read()
            lines = file.split("\n")
            for line in lines:
                values = line.split(",")
                date, time, size, temp, moisture, light = values #time by the hour
                self.times.append(time)
                #self.allValues[date]= [time,[size,temp,moisture,light]]
    
    
