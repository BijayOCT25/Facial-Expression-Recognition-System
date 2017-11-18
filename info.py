from Tkinter import *
import time

def show():
    top = Toplevel()
    top.geometry("100x50+500+300")
    top.title("FER")
    Message(top,text='Image captured').pack()
    top.after(500,top.destroy)

