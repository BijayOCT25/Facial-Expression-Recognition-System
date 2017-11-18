import sys, os, subprocess
import pandas
import random
import glob

class mp:
    def __init__(self):
        #self.df = pandas.read_excel("music.xlsx")
        self.source = "music"

    def open_file(filename):
        os.strart(filename)

    
    def get_music(self):
        actions = {}
        actions[0] = [x for x in self.source+os.sep+"Angry"+os.sep+"*"]
        actions[1] = [x for x in self.source+os.sep+"Happy"+os.sep+"*"]
        actions[3] = [x for x in self.source+os.sep+"Sad"+os.sep+"*"]
        actions[4] = [x for x in self.source+os.sep+"Shocked"+os.sep+"*"]
        return actions

    def open_music(self,emotion):
        musics = glob.glob("music/%s/*" %emotion)
        random.shuffle(musics)
        os.startfile(musics[0])
        return
        




