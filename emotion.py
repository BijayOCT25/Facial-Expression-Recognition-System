import cv2
import dlib
import modules
import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib
from musicplayer import mp
import random
import os
import time


class Emotion:
    '''This class predicts the emotion'''
    def __init__(self,clf):
        self.predictor = dlib.shape_predictor("predictor.dat")
        self.clf = SVC(kernel='linear', probability=True, tol = 1e-3)
        self.x = None
        self.y = None
        self.number = 0
        self.previous = None
        self.current = None
        self.starttime = time.time()
        self.text = None
        self.mp = mp()
        self.actions = self.mp.get_music()
        if (clf):
            print "Universal"
            self.clf = joblib.load('Universal.pkl')
        else:
            self.clf = joblib.load('CustomSVM.pkl')

        self.emotions = ['Angry','Happy','Neutral','Sad','Shocked']

    def getLandmarks(self,image,faces):
        if len(faces)>6:
            warn = " Multiple faces detected. Skipping frame"
            cv2.putText(image,str(warn),(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)
        else:
            for x,y,w,h in faces:
	            self.x  = int(x)-10
	            self.y = int(y)-10
	            roi = image[y:y+h,x:x+w]

	            #incresing the size of the ROI to give it to the shape predictor as image 
	            #ROI = image[(y-10):(y+h+10),(x-10):(x+w+10)]

	            #resizing the roi
	            resized_roi = modules.resize(roi,width=800,inter=cv2.INTER_CUBIC)

	            #getting the bottom and the right corner of the resized image
	            bottom,right = resized_roi.shape[:2]

	            #converting cv2 rectangle to dlib rectangle
	            rect = dlib.rectangle(x,y,x+w,y+h)
	            resized_rect = dlib.rectangle(0,0,right,bottom)

	            shape = self.predictor(image,rect)
	            resized_shape = self.predictor(resized_roi,resized_rect)

	            xlist = []
	            ylist = []
	            landmarks_vectorised = []
	            pred = []
	            
	            for i in range(36,68):
	                xlist.append(float(resized_shape.part(i).x))
	                ylist.append(float(resized_shape.part(i).y))
	                cv2.circle(image,(shape.part(i).x,shape.part(i).y),1,(0,255,0),-1)

	            xmean = np.mean(xlist)
	            ymean = np.mean(ylist)

	            xcentral = [(x-xmean) for x in xlist]
	            ycentral = [(y-ymean) for y in ylist]

	            for x,y,w,z in zip(xcentral,ycentral,xlist,ylist):
	                landmarks_vectorised.append(x)
	                landmarks_vectorised.append(y)

	            meannp = np.asarray((ymean,xmean))
	            coornp = np.asarray((z,w))
	            dist = np.linalg.norm(coornp-meannp)
	            landmarks_vectorised.append(dist)

	            pred.append(landmarks_vectorised)

	            prediction = self.clf.predict(pred)
	            test = self.clf.predict_proba(pred)
	            expression = self.emotions[int(prediction)]
	            

	            #self.text = "You seem to be {} \n Playing music for {} mood".format(expression,expression)

	            cv2.putText(image,str(expression),(self.x,self.y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

	            elapsed_time = time.time() - self.starttime  

	            #check for emotion every 5 seconds
	            if(elapsed_time >= 5.0):

	                cv2.putText(image,"Detecting Emotion",(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

	                #if consecutive frames are same
	                if(self.previous == expression):

	                    #only if the expression is not Neutral
	                    if(expression != "Neutral"):
	                        self.number += 1

	                else:
	                    self.previous = expression
	                    self.number = 0

	                #if emotion is same for 10 consecutive frames
	                if self.number >= 7:
	                  
	                    if (self.current != expression):
	                        self.mp.open_music(expression)
	                        #os.startfile("music\Parelima.mp3")
	                        #actionlist = [x for x in self.actions[prediction]]
	                        #random.shuffle(actionlist)
	                        #self.mp.open_file(actionlist[0])
	                    else:
	                        pass 

	                    self.starttime = time.time()
	                    self.current = expression 
                
        return image
