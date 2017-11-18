import cv2
import dlib
import numpy as np
from sklearn.svm import SVC
from sklearn.externals import joblib
import modules
from face import Face
import glob

def train():
    
    def get_images(emotion):
        print "Getting {} images ".format(emotion)
        files = glob.glob("Dataset/%s/*" %emotion)
        print len(files)
        return files

    def get_landmarks(image):
        image = modules.resize(image,width=400)
        cv2.imshow("image",image)
        cv2.waitKey(50)
        faces = face.detect(image)

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

             shape = predictor(image,rect)
             resized_shape = predictor(resized_roi,resized_rect)

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


    def make_sets():
        training_data = []
        training_labels = []
        for emotion in emotions:
            training = get_images(emotion)
            for item in training:
                image = cv2.imread(item,0)
                landmarks_vectorised = get_landmarks(image)
                if landmarks_vectorised == "error":
                    pass
                else:
                    training_data.append(landmarks_vectorised)
                    training_labels.append(emotions.index(emotion))
        cv2.destroyAllWindows()
        return training_data,training_labels

    predictor = dlib.shape_predictor("predictor.dat")
    clf = SVC(kernel = 'linear', probability=True, tol=1e-3)
    emotions = ['Angry','Happy','Neutral','Sad','Shocked']
    face = Face()

    training_data,training_labels = make_sets()
    npar_train = np.array(training_data)
    clf.fit(npar_train,training_labels)
    print "training"
    joblib.dump(clf,'CustomSVM.pkl')
    print "Successful"



