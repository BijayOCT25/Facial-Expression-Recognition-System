from modules import VideoStream
import time
import threading
import Tkinter as tk
from ttk import Frame,Button, Label, Style
from PIL import Image
from PIL import ImageTk
import cv2
from face import Face
from emotion import Emotion
import datetime
import os
import info 

class Capture:
    def __init__(self,label,clf):
        self.frame = None
        self.thread1 = None
        self.thread2 = None
        self.stopEvent1 = None
        self.stopEvent2 = None
        self.started = None
        self.captured = None
        self.label = label
        self.vs = VideoStream().start()
        self.fa = Face()
        self.emotion =  Emotion(clf)
        self.outputPath = None


    def start(self):
        #setting started to true to set it is started in the train function.
        #Because None type cannot be set
        self.started = True


        #Erasing stopEvent value (if any) to loop in the function
        self.stopEvent1 = None

        #checking if train thred is started
        #if started close it
        if(self.captured):
            self.stopEvent2.set()

        #initialize the thread
        self.stopEvent1 = threading.Event()
        self.thread1 = threading.Thread(target=self.videoLoop,args=())
        self.thread1.start()

    def close(self):
   
        #initiallly checking if the threads have been started and then closing 
        #if started      
        if(self.started):
            self.stopEvent1.set()  
        if(self.captured):
            self.stopEvent2.set() 
        # self.vs.stop()

    def exit(self):
        if(self.started):
            self.stopEvent1.set()
            print "closing thread 1"
        if(self.captured):
            self.stopEvent2.set()
            print "closing thread 2"
        self.vs.stop()
        VideoStream().stop()
    

     

    def capture(self,emotion):
        #setting the trained variable to true for same reason as started
        self.captured = True
        # self.emo = emotion 
        self.outputPath = "Dataset"+os.sep+emotion
        if os.path.exists(self.outputPath):
            pass
        else:
            os.mkdir(self.outputPath)

        #Setting StopEvent to None to loop 
        self.stopEvent2 = None
        
        #stopping started thread if running
        if(self.started):
            self.stopEvent1.set()
         
        #initializing the train thred
        self.stopEvent2 = threading.Event()
        self.thread2 = threading.Thread(target=self.captureLoop,args=())
        self.thread2.start()
    
    def snapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        output = os.path.sep.join((self.outputPath,filename))
        cv2.imwrite(output,self.frame.copy())
        self.showInfo()
        
    def showInfo(self):     
        info.show()

    def videoLoop(self):
        try:
            #loop until the stopEvent is not set
            while not self.stopEvent1.is_set():
                self.frame = self.vs.read()

                gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
                image = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)

                faces = self.fa.detect(gray)
                
                image = self.emotion.getLandmarks(image,faces)

                image = Image.fromarray(image)

                image = ImageTk.PhotoImage(image)

                self.label.configure(image = image)
                self.label.image = image

        except RuntimeError, e :
            print "Error"

    def captureLoop(self):
        try:
            while not self.stopEvent2.is_set():
                self.frame = self.vs.read()

                image = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)

                image = Image.fromarray(image)

                image = ImageTk.PhotoImage(image)

                self.label.configure(image=image)
                self.label.image = image
                #self.stopEvent2.set() 

        except RuntimeError, e :
            print "Error"

    
    