import cv2

class Face:
    """Returns the faces in the given image"""
    def __init__(self):

        
        self.cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_alt.xml')

    def detect(self,image):
        faces = self.cascade.detectMultiScale(image,1.3,5)
        return faces


