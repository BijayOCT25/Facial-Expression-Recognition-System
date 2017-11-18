import modules
import dlib
import cv2
import numpy as np

def getLandmarks(image,face,predictor):
    for x,y,w,h in face:
        roi = image[y:y+h,x:x+w]

        #incresing the size of the ROI to give it to the shape predictor as image 
        ROI = image[(y-10):(y+h+10),(x-10):(x+w+10)]

        #resizing the roi
        resized_roi = modules.resize(roi,width=800,inter=cv2.INTER_CUBIC)

        #getting the bottom and the right corner of the resized image
        bottom,right = resized_roi.shape[:2]

        #converting cv2 rectangle to dlib rectangle
        rect = dlib.rectangle(x,y,x+w,y+h)
        resized_rect = dlib.rectangle(0,0,right,bottom)

        shape = predictor(image,rect)
        resized_shape = predictor(ROI,resized_rect)

        xlist = []
        ylist = []
        landmarks_vectorised = []

        for i in range(36,68):
            xlist.append(float(resized_shape.part(i).x))
            ylist.append(float(resized_shape.part(i).y))
            cv2.circle(image,(shape.part(i).x,shape.part(i).y),1,(255,0,0),-1)

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

        return landmarks_vectorised