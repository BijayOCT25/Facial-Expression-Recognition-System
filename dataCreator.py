import cv2
import numpy as np
import os
import time
import math
from face import Face
from ttk import Label
from PIL import Image, ImageTk
from modules import VideoStream

class dataCreator(Label):
    def __init__(self,label,vs):
        self.face = Face()
        self.label = label
        self.vs = vs
        self.emotions = ['Angry','Happy','Neutral','Sad','Shocked']
        self.target = "Dataset"

    def create(self):
        for emotion in self.emotions:
            print ("please look {}. Press Capture button when ready".format(emotion))
            start_time = time.time()
            elapsed_time = time.time()-start_time
            sample = 0
            if os.path.exists(self.target+os.sep+emotion):
                pass
            else:
                os.mkdir(self.target+os.sep+emotion)
        
            while True:
                while elapsed_time < 3.0 :
                    image = self.vs.read()
                    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                    elapsed_time = int(time.time()-start_time)
                    
                    text = "Starting in {} seconds".format(3 - elapsed_time)

                    cv2.putText(image,str(text),(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

                    cv2.waitKey(100)
                    img = Image.fromarray(image)

                    img = ImageTk.PhotoImage(img)

                    self.label.configure(image = img)
                    self.label.image = img
    
                image = self.vs.read()
               
                if (sample > 20):
                    break
                else:
                    gray  = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                    image_copy = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                    faces = self.face.detect(gray)
                    for x,y,w,h in faces:
                        sample += 1
                        #frame = image[y-10:y+h+10,x-10:x+w+10]
                        cv2.rectangle(image_copy,(x,y),(x+w,y+h),(255,0,0),1)
                        cv2.imwrite(self.target + os.sep + emotion + os.sep +str(time.time()) + ".jpg",image)

                        cv2.waitKey(100)

                    img = Image.fromarray(image_copy)

                    img = ImageTk.PhotoImage(img)

                    self.label.configure(image = img)

                    self.label.image = img








