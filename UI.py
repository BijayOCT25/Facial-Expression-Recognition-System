from Tkinter import *
import Tkinter as ttk
from ttk import *
from functools import partial
from capture import Capture
from trainer import Trainer
from emotion import Emotion
from confusionMatrix import confusionMatrix
from PIL import Image 
from PIL import ImageTk
import cv2
import tkFileDialog
import shutil
import re

class UI(Frame):
    """description of class"""
    """General UI of the application"""

    def __init__(self,parent):

        Frame.__init__(self,parent)

        self.parent = parent
        self.emotion = None
        self.captureStarted = False
        self.cap = None
        self.frameArea = None
        self.clf = True
        self.trainer = Trainer()
        self.confusionMatrix = confusionMatrix()
        self.initUI()

    def initUI(self):
        self.parent.title("FER Music Player")
        self.parent.wm_protocol("WM_DELETE_WINDOW",self.stop)
        self.pack(fill=BOTH,expand=True)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(3,pad=7)
        self.rowconfigure(3,weight=1)
        self.rowconfigure(5,pad=7)    

        menubar = Menu(self.parent)
        self.parent.config(menu = menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label='Start',command = self.start)
        fileMenu.add_command(label='Train',command = self.train)
        #fileMenu.add_command(label='Confusion Matrix',command = self.confuse)
        fileMenu.add_command(label='Stop', command = self.stopCamera)
        menubar.add_cascade(label='Option',menu=fileMenu)

        emotions = {'Angry','Happy','Neutral','Sad','Shocked'}

        optionMenu = Menu(menubar)
        for emotion in emotions: 
            optionMenu.add_command(label=emotion,command=partial(self.setEmotion,emotion))

        selectMenu = Menu(menubar)
        selectMenu.add_command(label='Universal',command =  partial(self.setClf,1))
        selectMenu.add_command(label='Custom',command =  partial(self.setClf,0))
        menubar.add_cascade(label='Select',menu=selectMenu) 
       

        #setting the focus to the label element to get keyboard in put
        def prep(event):
            #event.widget.config(bg="light blue")
            event.widget.focus_set()

        def clicked(event):
            print "clicked"

        menubar.add_cascade(label='Capture Emotions',menu=optionMenu)

        musicMenu = Menu(menubar)
        musicMenu.add_command(label='Angry',command=partial(self.openDialog,emotion))
        musicMenu.add_command(label='Happy',command=partial(self.openDialog,emotion))
        musicMenu.add_command(label='Sad',command=partial(self.openDialog,emotion))
        musicMenu.add_command(label='Shocked',command=partial(self.openDialog,emotion))
        menubar.add_cascade(label='Import Music',menu=musicMenu)

        #Label(self,text="FER").grid()
        self.frameArea = Label(self,relief=RAISED,borderwidth=1)
        self.frameArea.grid(row=1,column=0,columnspan=2,rowspan=4,sticky=(N,E,W,S))

        #self.frameArea.bind('<Button-1>',prep)

        self.frameArea.bind('<Return>',self.capture)

        self.setFrame()

    #start capturing frame
    def capture(self,event):
        print self.emotion
        self.cap.snapshot() 

    #setting the classifier
    def setClf(self,val):
        if(val):
            self.clf = True
            print self.clf
        else:
            self.clf = False
            print self.clf

    #Calculating accuracy
    def accuracy(self):
       self.trainer.accuracy()

    #cimputing confusion matrix
    def confuse(self):
        self.confusionMatrix.getconfusion()

    #setting emotion for capturing
    def setEmotion(self,emotion):
        self.emotion = emotion
        self.frameArea.focus_set()
        if not self.captureStarted:
           self.captureStarted = True
           self.cap = Capture(self.frameArea,self.clf)
        self.cap.capture(self.emotion)

    #starting recognition
    def start(self):
        if not self.captureStarted:
            self.captureStarted = True
            self.cap = Capture(self.frameArea,self.clf)
        self.cap.start()

    #Quit
    def stop(self):
        if self.captureStarted:
            self.cap.exit()
        print "closing"
        self.quit()

    #training the predictor
    def train(self):
        self.trainer.train()

    #setting image to frame
    def setFrame(self):
        display_image = cv2.imread("img.jpg")
        display_image = Image.fromarray(display_image)
        display_image = ImageTk.PhotoImage(display_image)
        self.frameArea.configure(image = display_image)
        self.frameArea.image = display_image

    #Closing camera
    def stopCamera(self):
        if self.captureStarted:
            self.cap.exit()
        self.setFrame()
        self.captureStarted = False
        self.cap = None
        print "captureStarted False"
        
    #selection of music
    def openDialog(self,emotion):
        ftypes = [('Audio files','*.mp3 *wav')]
        dialog = tkFileDialog.Open(self,filetypes=ftypes)
        fl = dialog.show()

        if fl != '':
           self.importFile(fl,emotion)

    def importFile(self,filename,emotion):
        target = "music/%s" %emotion
        shutil.copy(filename,target)
        print "{} imported".format(filename)
        
 



