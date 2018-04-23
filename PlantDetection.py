"""Steps:
develop database for characteristics of objects
--> color, 
ask a bunch of questions, calculate each gini impurity and overall gain 
iterate through and choose best question with highest gain
recurse and move on to next branch
base case: gain = 0"""
#source for opencv code: https://thecodacus.com/opencv-object-tracking-colour-detection-python/#.WtpoWdPwY6U
#https://pythonprogramming.net/tkinter-adding-text-images/
import numpy as np
import cv2
import serial
import math
#ser = serial.Serial('/dev/tty.usbmodem14541', 9600)

class plantDetection(object):
    def __init__(self):
        self.lower=np.array([33,80,40])
        self.upper=np.array([102,255,255]) #green
        self.imageSize = 340,220
        self.kernelOpen=np.ones((5,5))
        self.kernelClose=np.ones((20,20))
        self.foundPlants = []
    def takePicture(self):
        cam= cv2.VideoCapture(1)
        ret, initImage = cam.read()
        self.sizedImage = cv2.resize(initImage,(340,220))
        imgHSV= cv2.cvtColor(self.sizedImage,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(imgHSV,self.lower,self.upper)
        
        #remove tiny dots/bits to clean image
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,self.kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,self.kernelClose)
        self.cleanedImage = maskClose
    def showTargets(self,row,col):
        im,conts,h=cv2.findContours(self.cleanedImage,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for i in range(len(conts)):
            x,y,w,h=cv2.boundingRect(conts[i])
            r = w/2 #radius
            x,y=x+r/2,y+r/2
            area = math.pi*r
            cv2.circle(self.sizedImage,(x,y),r,(0,0,255), 2)
            self.foundPlants.append((x,y,area))
        cv2.imwrite('IMAGES'+os.sep+'%s.png'%(row,col))

    def main(self):
        ardMsg = ser.readline().decode("utf-8")
        if ardMsg != "":
            coord = ardMsg.split(",")
            col,row = int(coord[0],coord[1])
            self.takePicture()
            self.showTargets(row,col)
            
#main()


