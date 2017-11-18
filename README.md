# Facial-Expression-Recognition-System
Facial expression analysis and recognition has been one of the fast-developing Computer Vision technology due to its wide range of application areas such as emotion analysis, biometrics, image retrieval and is one of the subjects on which lots of research has been done through solving the problems occurring in recognition of the facial expressions under different illuminations, orientations and numerous other variations. 

FER system consists of different pre-processing and processing parts. The detection and extraction of face images from the input data together with the normalization process form up the pre-processing part. The processing part on the other hand; aims to extract specific features from the already pre-processed images, and recognize the facial expressions depending on these features. 
.
This Facial Expression Recognition System, capable of distinguishing the six universal emotions: Shocked, anger, happiness, sadness and neutral. It is designed to be person independent and tailored for dynamic images taken from webcam. The system integrates a face detection mechanism using Viola-Jones algorithm, uses Dlib for feature extraction and performs classiﬁcation using a multi-class Support Vector Machine model.

It also triggered the Song based on the emotion detected by using the default media player of OS.

Requirements:-

             Python 2.7X
             Open CV2
             SKLearn
             Dlib, C++ Library
             CMake “Add CMake to the system PATH"
             Visual Studio 2015 (install Python 2.7 tools)
             Boost Python
             
 P.S. Download the Dlib predicator (.dat file) from this link http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 . 
      This project is done for educational purpose and refrence is taken from http://www.paulvangent.com/2016/08/05/emotion-recognition-using-facial-landmarks/
 
             
