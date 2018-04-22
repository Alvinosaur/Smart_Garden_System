import os
import random
import math
import serial
import RPi.GPIO as GPIO
import time
import cv2

class StoreData(object):
    path = "Plant_Data"
    def __init__(self):
        self.numVals = 7
        self.time= ""
        self.plants = dict()
        self.Locations = {(0,0):"Pepper1",(1,0):"Pepper2",
            (0,1):"Strawberry1",(1,1):"Stawberry2"}
        
    def readArduino():
        ser=serial.Serial("/dev/ttyACM0",9600)#ACM will be diff
        ser.baudrate = 9600
        inputRead = ser.readline().decode("utf-8")
        formatData(inputRead)

    def formatData(self,inputRead):
        #sensorset0, 1, 2
        #each set comes with 
        if inputRead == "": return
        inputRead = inputRead[:-2]
        allVals = inputRead.split(";")
        for valueSet in allVals:
            values = valueSet.split(",")
            if len(values) < self.numVals:
                continue
            #values.append(size from another function)
            values.append(30)
            getPlantType(values)
            
    def getPlantType(self,values):
        #do some opencv or already have database of locations stored
        #need to have location flexibility
        x,y = values[1],values[2]
        if self.Locations.get((x,y),0) != 0:
            name = self.Locations[(x,y)]
            self.plants[name] = ",".join(values)
            fillFolder(name)
        
    def writeFile(self,path,name):
        values = self.plants[name] + ";"
        with open(path, "wt") as f:
            f.write(values)  
            
    def fillFolder(self,name):
        species = name[:-1]
        values = self.plants[name]
        date = values[0].split(".") #04.22.11 month.day.hour
        month, day = date[0], date[1]
        filePath = storeData.path+os.sep+species+os.sep+name+os.sep+month
        #Folder = Plant_Data/Tomato/Tomato1/month
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        csvFile = filePath+os.sep+day+".csv"
        writeFile(self,csvFile,name)

        #for i in range(len(self.temps)):
            #diff = self.temps[i] - self.medTemp
            #if diff < 0:
                #coolPlants.append(
class image(object):
    def __init__(self):
        self.cameraPort = 0
        self.camera = cv2.VideoCapture(0)
        self.count = 0
    def takePic(self):
        retval,img = self.camera.read()
        imgFile = StoreData.path+os.sep+"Images"+os.sep+str(count)+".png"
        cv2.imwrite(imgFile,img)
        self.count += 1
    def processImage(self):
        
        
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

        #     if depth ==0:
        #         species = name[:-1]
        #         filePath = filePath+os.sep+species
        #         self.fillFolder(filePath,name,values,depth+1)
        #     elif depth == 1:
        #         filePath = filePath+os.sep+name
        #         self.fillFolder(filePath,name,values,depth+1)
        #     elif depth ==2:
        #         date = values[0].split(".")
        #         month, day = date[0], date[1]
        #         filePath = filepath+os.sep+month
        #         self.writeFile(filePath)
        # else:
        #     os.makedirs(filePath)
        #     if depth < 3:
        #         self.fillFolder(filePath,name,values,depth)
    # 
    # def getData(self):
    #     with open(path+os.sep+"dataLog"+os.sep+"%s"%self.type,"rt") as f:
    #         file = f.read()
    #         lines = file.split("\n")
    #         for line in lines:
    #             values = line.split(",")
    #             date, time, size, temp, moisture, light = values #time by the hour
    #             self.times.append(time)
    #             #self.allValues[date]= [time,[size,temp,moisture,light]]
    # 
    
