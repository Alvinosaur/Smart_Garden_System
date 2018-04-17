import serial
import RPi.GPIO as GPIO
import time

allPlants = [[]]
userInput = "Iris"
dataLog = dict()
countSeen = dict()

plantType = "Iris"
seenPlants[plantType] = seenPlants.get(plantType,0)+1
plantID = plantType+str(seenPlants.get(plantType,0))
dateValues = dict()
dataLog[plantID] = dateValues


        
        
        
def readArduino():
    ser=serial.Serial("/dev/ttyACM0",9600)#ACM will be diff
    ser.baudrate = 9600
    inputRead = ser.readline().decode("utf-8")
    storeData(inputRead)
    #format: date,x,y,moisture,light
    
    
def storeData(inputRead,numVals=4):
    allVals = inputRead.split(",")
    if len(allVals)< numVals:
        return
    #remove new line command
    allVals[-1] = allVals[-1][:-2]
    date,x,y,moist,light = allVals
    loc = (float(x),float(y))
    dataLog[plantID][date]={loc,float(moisture),float(light)}
    
def accessData(userInput):
    for key in dataLog: #every key is a string
        countSeen = dict()
        if key[:len(userInput)]==userInput:
            #we found a key that is the same plan
            displayGraph()
            
def displayGraph():
    