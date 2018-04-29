import os
import numpy as np
import pandas as pd
import math

class neuralNetwork(object):
    LEARNING_RATE = 0.5
    def __init__(self,plant):
        self.plant = plant
        self.dataFolder = self.plant+"NNData"
        self.weightsFolder = "weightsFolder"
        self.allValues = dict()
        self.plantGrowths = []
        self.valueTypes = ["Temp","Bright","Moist"]
        for sensor in self.valueTypes:
            self.allValues[sensor] = []
        self.numNeurons = len(self.valueTypes)
        self.hiddenBias = .5
        self.outerBias = .5
        self.changeFactor = 2
        
    def collectData(self):
        for inc in range(10):#each species has 10 plants from 0 to 9
            plant = self.plant+str(inc)
            self.allValues[plant] = {"sizeChange":[]}
            for inc in range(len(self.valueTypes)):
                factor = self.valueTypes[inc]
                file = self.dataFolder+os.sep+plant+"Train%s.csv"%factor
                dataTrain = pd.read_csv(file)
                xTrain = dataTrain[factor].values.reshape(1,-1)
                yTrain = dataTrain['sizeChange'].values.reshape(1,-1)
                sensorVals = xTrain.tolist()
                sizeChange = yTrain.tolist()
                self.allValues[plant][factor] = sensorVals[0]
                self.allValues[plant]["sizeChange"].append(sizeChange[0])
        
    def initializeNeuralNetwork(self):
        self.hiddenLayerNet = [self.hiddenBias]*(self.numNeurons)
        self.hiddenLayerOut = [0]*(self.numNeurons) 
        self.outputLayerNet = self.outerBias 
        self.outputLayerOut = 0
        self.errors = []
        
    def initializeNewWeights(self):
        self.newOutputWeights = [] 
        self.newHiddenWeights = [[0]*self.numNeurons for i in range(self.numNeurons)] 
        
    def initializeWeights(self):
        self.outputWeights = [.5]*self.numNeurons
        self.hiddenWeights = [[.5]*self.numNeurons for i in range(self.numNeurons)]
        filePath = self.weightsFolder+os.sep+self.plant+"Weights.txt"
        if os.path.exists(filePath):
            self.getExistingWeights(filePath)
            
    def getExistingWeights(self,filePath):
        contents = neuralNetwork.readFile(filePath)
        weightList = contents.split(";")
        #outerLayer weights
        weightStringOut= weightList[0]
        values = weightStringOut.split(",")
        
        for inc in range(len(values)):
            self.outputWeights[inc] = float(values[inc])
        #hidden layer weights
        weightStringHid = weightList[1]
        values = weightStringHid.split(",")
        for inc in range(len(values)):
            self.hiddenWeights[inc//self.numNeurons][inc%self.numNeurons] =\
                                                        float(values[inc])
                      
    def calcHiddenNet(self,plant,valueInc):
        for neuronInc in range(self.numNeurons):
            for factorInc in range(len(self.valueTypes)):
                factor = self.valueTypes[factorInc]
                input = self.allValues[plant][factor][valueInc]
                weight = self.hiddenWeights[neuronInc][factorInc]
                netInput = weight*input
                self.hiddenLayerNet[neuronInc]+=netInput
            self.calcHiddenOutput(neuronInc)
            self.calcOuterNet(neuronInc)
        self.calcOuterOutput()
        
    def calcHiddenOutput(self,neuronInc):
        netInput = self.hiddenLayerNet[neuronInc]
        self.hiddenLayerOut[neuronInc]=self.activeFunc(netInput)
            
    def calcOuterNet(self,neuronInc):
        weight = self.outputWeights[neuronInc]
        input = self.hiddenLayerOut[neuronInc]
        netInput = weight*input
        self.outputLayerNet+=netInput
        
    def calcOuterOutput(self):
        net = self.outputLayerNet
        self.outputLayerOut=self.activeFunc(net)
        
    def backProp(self,plant,valueInc):
        for neuronInc in range(self.numNeurons):
            #for every neuron...
            errorWrtOuterOut, outerOutWrtOuterNet = \
                        self.updateOutputWeights(plant,neuronInc,valueInc)
                                    
            for sensorInc in range(self.numNeurons):
                #update weight for each input
                self.updateHiddenWeights(plant,neuronInc,sensorInc,valueInc,
                                    errorWrtOuterOut,outerOutWrtOuterNet)
        
    def updateOutputWeights(self,plant,neuronInc,valueInc):
        #output and target: growth rate of plant over one day
        target = 0
        output = self.outputLayerOut
        
        for sensorInc in range(len(self.valueTypes)):
            #sum up the contributions to plant growth from each factor
            target += self.allValues[plant]["sizeChange"][sensorInc][valueInc]
        print(output,target)
        error = .5*(target-output)**2 
        self.errors.append(error)
        
        errorWrtOuterOut = -1*(target-output)
        outerOutWrtOuterNet = output*(1-output) #only for logistic sigmoid activation fx
        outerNetWrtWeight = self.hiddenLayerOut[neuronInc]
        
        errorWrtWeight = errorWrtOuterOut* outerOutWrtOuterNet* outerNetWrtWeight
        newWeight = self.outputWeights[neuronInc]-\
                            (neuralNetwork.LEARNING_RATE*errorWrtWeight)
                            
        self.newOutputWeights.append(newWeight)
        
        return errorWrtOuterOut,outerOutWrtOuterNet
    
    def updateHiddenWeights(self,plant,neuronInc,sensorInc,valueInc,
                                    errorWrtOuterOut,outerOutWrtOuterNet):
        factor = self.valueTypes[sensorInc]
        input = self.allValues[plant][factor][valueInc]

        errorWrtOuterNet = errorWrtOuterOut*outerOutWrtOuterNet
        
        #simply the weight connected to it
        outerNetWrtHiddenOut = self.outputWeights[neuronInc]
        errorWrtHiddenOut = errorWrtOuterNet * outerNetWrtHiddenOut
        
        #neuronInc b/c calculating effects of sensor weights for each neuron
        hiddenOut = self.hiddenLayerOut[neuronInc]
        hiddenOutWrtHiddenNet = hiddenOut*(1-hiddenOut)
        hiddenNetWrtWeight = input
        
        errorWrtWeight = errorWrtHiddenOut* hiddenOutWrtHiddenNet* hiddenNetWrtWeight
        
        newWeight = self.hiddenWeights[neuronInc][sensorInc]-\
                        neuralNetwork.LEARNING_RATE*errorWrtWeight
                        
        self.newHiddenWeights[neuronInc][sensorInc] = newWeight
        
    def updateAllWeights(self):
        self.hiddenWeights = self.newHiddenWeights
        self.outputWeights = self.newOutputWeights

    def storeWeights(self):
        if not os.path.exists(self.weightsFolder):
            os.makedirs(self.weightsFolder)
        txtFile = self.weightsFolder + os.sep + self.plant + "Weights.txt"
        outWeightString = ""
        hiddenWeightString = ""
        
        with open(txtFile, "wt") as f:
            #outputs weights separated by "," then right 
            #output and hidden weight groups separated by ";"
            for weight in self.outputWeights:
                outWeightString+=str(weight)
                outWeightString+=","
            
            for neuronInc in range(self.numNeurons):
                for sensorInc in range(self.numNeurons):
                    hiddenWeightString+=str(self.hiddenWeights[neuronInc][sensorInc])
                    hiddenWeightString+=","
                    
            allLines = outWeightString[:-1] + ";" + hiddenWeightString[:-1]
            #[[1,2,3],[4,5,6]] --> "1,2,3,4,5,6"
            f.truncate() #erase data already stored in there, replace with new data
            f.write(allLines)
            
    def activeFunc(self,net):
        neuronOutput = 1/(1+math.exp(-net))
        return neuronOutput
        
    def main(self):
        self.initializeWeights() #don't reset the old weights
        self.collectData()
        for inc in range(10):#each species has 10 plants from 0 to 9
            plant = self.plant+str(inc)
            for valueInc in range(len(self.allValues[plant]["sizeChange"][0])):
                self.initializeNeuralNetwork()
                self.initializeNewWeights()
                self.calcHiddenNet(plant,valueInc)
                self.backProp(plant,valueInc)  
                self.updateAllWeights()
        #self.storeWeights()
        
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()
            
test = neuralNetwork("Kale")
test.main()
