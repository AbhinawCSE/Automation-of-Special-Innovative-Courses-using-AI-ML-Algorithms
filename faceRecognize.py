#!/usr/bin/env python
# coding: utf-8

# import the necessary packages
from imutils import paths
import face_recognition
import pickle
import cv2
import numpy

# # Obtaining face encodeings of known faces
def encodeFace(imagePath,imageName):
    # grab the paths to the input images in our dataset
    img = cv2.imread(imagePath)
    
    # initialize the list of known encodings and known names
    knownFaceEncodings = []
    knownFaceNames = []
    
    # load the input image and convert it from RGB (OpenCV ordering)
    # to dlib ordering (RGB)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input image
    knownFaceLocations = face_recognition.face_locations(rgb,model='hog')
    
    # compute the facial embedding for the face
    FaceEncodings = face_recognition.face_encodings(rgb, knownFaceLocations)
    
    # loop over the encodings
    # add each encoding + name to our set of known names and encodings
    knownFaceEncodings.append(FaceEncodings)
    knownFaceNames.append(imageName)
    
    # dump the facial encodings + names to disk
    data = {"encodings": knownFaceEncodings, "names": knownFaceNames}
    f = open("C:/Users/Abhi/Desktop/Project20/pickle_folder/encodedFace", "wb")
    f.write(pickle.dumps(data))
    f.close()

# # Recognizing faces in the image using known face encoding
def recognizeFace(imagePath,imageName):
    # load the known faces and embeddings
    data = pickle.loads(open("C:/Users/Abhi/Desktop/Project20/pickle_folder/encodedFace", "rb").read())
    # load the input image and convert it from BGR to RGB
    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    testFaceLocations = face_recognition.face_locations(rgb, model="hog")
    testFaceEncodings = face_recognition.face_encodings(rgb, testFaceLocations)
    # initialize the list of names for each face detected
    names = []
    if(len(testFaceLocations) == 0 and len(testFaceEncodings) == 0):
        return 0
    else:
        # loop over the facial embeddings
        for encoding in testFaceEncodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"], encoding)
            arr=numpy.array(matches)
            name = "Unknown"
            # check to see if we have found a match
            if True in arr:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in numpy.ndenumerate(arr) if b]
                counts = {}
                matched=[]
                for (i,j) in enumerate(matchedIdxs):
                    matched.append(i)
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in range(0,len(matched)-127):
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                # determine the recognized face with the largest number of
                # votes (note: in the event of an unlikely tie Python will
                # select first entry in the dictionary)
                name = max(counts, key=counts.get)
            # update the list of names
            names.append(name)
        #print(names)
        if imageName in names:
            return 1
        else:
            return 0
        
if __name__ == '__main__':
    encodeFace(input("Enter the path: "),input("Enter the name: "))
    recognizeFace(input("Enter the path: "),input("Enter the name: "))