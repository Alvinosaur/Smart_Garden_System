import matplotlib.pyplot as plt
import os

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

contentsToWrite = "This is a test!\nIt is only a test!"
writeFile("foo.txt", contentsToWrite)

contentsRead = readFile("foo.txt")
assert(contentsRead == contentsToWrite)

print("Open the file foo.txt and verify its contents.")
class plantData(object):
    def __init__(self,type,
        self.type = type
        #self.allValues = dict()
        self.times = []
        self.sizes = []
        self.moistures = []
        self.lights = []
    def getData(self):
        with open(path+os.sep+"images"+os.sep+"%s"%self.type,"rt") as f:
            file = f.read()
            lines = file.split("\n")
            for line in lines:
                values = line.split(",")
                date, time, size, moisture, light = values #time by the hour
                self.times.append(time)
                #self.allValues[date]= [time,[size,moisture,light]]
    
    def plotData(self):
        plt.plot(self.times,self.sizes)
        plt.plot(self.times,self.moistures)
        plt.plot(self.times,self.lights)
        #2D list of dates and their respective measurements of this plant's size
        #all lines already in order of time entered
        #plt.plot(allVals[0],allVals[1])
    def analyzeData(self):
        #machine learning part??
    
    
class Iris(plantData):
    

        
#program returns data about a new plant with name "pepper"

        