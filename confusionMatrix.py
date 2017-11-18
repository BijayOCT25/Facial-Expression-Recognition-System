import cv2
import dlib
import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib
import modules
from face import Face
import glob
import random
import os

class confusionMatrix:
    def __init__(self):
        self.predictor = dlib.shape_predictor("predictor.dat")
        self.clf = SVC(kernel = 'linear', probability=True, tol=1e-3)
        self.emotions = ['Angry','Happy','Neutral','Sad','Shocked']
        self.face = Face()

    def getconfusion(self):
        # predictor = dlib.shape_predictor("predictor.dat")
        # clf = SVC(kernel = 'linear', probability=True, tol=1e-3)
        # emotions = ['Angry','Happy','Neutral','Sad','Shocked']
        # face = Face()
      
        mat = []
        training_data,training_labels,prediction_data,prediction_labels = self.make_sets()
        npar_train = np.array(training_data)
        npar_pred = np.array(prediction_data)
        self.clf.fit(npar_train,training_labels)
        print "training..."
        print len(prediction_data)
        for index,pred in enumerate(prediction_data):
            prediction = self.clf.predict(npar_pred[index].reshape(1,-1))
            #print self.emotions[int(prediction)]
            pred = int(prediction)
            actual =  int(prediction_labels[index])
            if(pred != actual):
                print "{} predicted as {}".format(self.emotions[actual],self.emotions[pred])
                cell = "_"+str(actual)+str(pred)+"_"
                mat.append(cell)
        print "Successful"
        print mat

        def count_mat(mat):
            new_mat = []
            count = {}
            for n in mat:
                if n not in new_mat:
                    new_mat.append(n)
                    count[n] = 1
                else:
                    count[n] += 1
            return new_mat,count

        New_mat, count = count_mat(mat)
        for mats in New_mat:
            print "{} : {} \n".format(mats,count[mats])


       

        

    def get_images(self,emotion):
        print "Getting {} images ".format(emotion)
        files = glob.glob("Dataset/%s/*" %emotion)
        random.shuffle(files)
        training = files[:int(len(files)*0.7)]
        prediction = files[-int(len(files)*0.3):]
        print len(files)
        return training,prediction

    def get_landmarks(self,image):
        image = modules.resize(image,width=400)
        cv2.imshow("image",image)
        cv2.waitKey(10)
        faces = self.face.detect(image)

        for x,y,w,h in faces:
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

            for i in range(36,68):
                xlist.append(float(resized_shape.part(i).x))
                ylist.append(float(resized_shape.part(i).y))

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
        if len(faces)<1:
            landmarks_vectorised = "error"
        return landmarks_vectorised


    def make_sets(self):
        training_data = []
        training_labels = []
        prediction_data= []
        prediction_labels = []
        for emotion in self.emotions:
            training,prediction = self.get_images(emotion)
            for item in training:
                image = cv2.imread(item,0)
                landmarks_vectorised = self.get_landmarks(image)
                if landmarks_vectorised == "error":
                    pass
                else:
                    training_data.append(landmarks_vectorised)
                    training_labels.append(self.emotions.index(emotion))
            for item in prediction:
                image = cv2.imread(item,0)
                landmarks_vectorised = self.get_landmarks(image)
                if landmarks_vectorised == "error":
                    pass
                else:
                    prediction_data.append(landmarks_vectorised)
                    prediction_labels.append(self.emotions.index(emotion))
        cv2.destroyAllWindows()
        return training_data,training_labels,prediction_data,prediction_labels

    



        



