import math
import random
import matplotlib.pyplot as plt

#TEST REFLECT SUMMER INC 
class GenData(object):
    def __init__(self):
        self.tempWeight = 0.2
        self.brightWeight = 0.2
        self.sinAmp = 3
        self.times = []
        self.temps = []
        self.lights = []
        self.moists = []
        self.medTemp = 60 #degrees Fahrenheit
        self.startBright = 70 #lumens?
        self.startMoist = 50

    def synthData(self):
        for day in range(31): #30 days in a month
            dayTemp= self.randTemp(day)
            tempDiff = dayTemp-self.medTemp
            dayBright = self.randBright(day,tempDiff)
            brightDiff = dayBright - self.startBright
            dayMoist = self.randMoist(day,tempDiff,dayBright)
            line = [day]
            self.times.append(day)
            self.temps.append(dayTemp)
            self.moists.append(dayMoist)
            self.lights.append(dayBright)
            
    def randTemp(self,day):
        fluct = GenData.randFluct()
        dayTemp = self.sinAmp*math.sin(.35*day)+self.medTemp+\
                                fluct+GenData.gradInc(day)
        return dayTemp
        
    def randBright(self,day,tempDiff):#brightness can be partly based off temp
        fluct = GenData.randFluct()
        dayBright = self.startBright+self.sinAmp*math.sin(.35*day+5)+\
                        fluct+GenData.gradInc(day)+tempDiff*self.tempWeight
        return dayBright
        
    def randMoist(self,day,tempDiff,brightDiff):
        fluct = GenData.randFluct()
        dayMoist = self.startMoist-GenData.gradInc(day)-\
                tempDiff*self.tempWeight - brightDiff*self.brightWeight
        return dayMoist
        
    def plotData(self):
        self.synthData()
        #plt.plot(self.times,self.sizes)
        plt.plot(self.times,self.temps,label="Temperature",color="red")
        plt.plot(self.times,self.moists,label="Moisture",color="blue")
        plt.plot(self.times,self.lights,label="Brightness",color="gold")
        plt.xlabel('Time')
        plt.ylabel('Plant Growth, Sensor Values')
        plt.legend(bbox_to_anchor=(1, .5), loc=1, borderaxespad=0.)
        plt.show()
        
    @staticmethod
    def randFluct():
        range = 2
        return random.randint(-range,range)
        
    def gradInc(day):
        M = 10
        k = 0.1
        z = 6.2
        y0 = 3.5
        deno = 1+math.e**(-k*(day-z))
        result = (M/deno)-y0
        return result
test = GenData()
test.plotData()