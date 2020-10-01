import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import sys
import time
from tkinter import *
import patient
import doctor2

data1 = sys.argv[1]
print(data1)
data2 = sys.argv[2]
data_path = f'{data1}/{data2}/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]

Training_Data, Labels = [], []

for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)

model = cv2.face.LBPHFaceRecognizer_create()

model.train(np.asarray(Training_Data), np.asarray(Labels))

print("done")

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # contain properties of face. 

global user
user = False

global epo1
epo1 = time.time() # count time. 
def face_detector(img, size = 0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    if faces is():
        return img,[]

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))
    # if face detectd do something. 
    return img,roi

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()

    image, face = face_detector(frame)

    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)

        if result[1] < 500:
            confidence = int(100*(1-(result[1])/300))
            display_string = str(confidence)+'% Confidence it is user'
        cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)


        if confidence > 80:
            cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow(f'Detecting the {data2}', image)
            cv2.putText(image, f"Logining in as {data2}", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            epoc2 = time.time()
            user = True

        else:
            cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow(f'Detecting the {data2}', image)



    except:
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow(f'Detecting the {data2}', image)
        pass

    if cv2.waitKey(1)==13 or user == True :
        break


cap.release()
cv2.destroyAllWindows()

print("working")

if data1 == "patdata":
    data1 = "Patient"
else:
    data1 = "Doctor"

print("debugging")
print(data1)
print("debugging")
print(data2)
if user == True:
    if data1 == "Doctor":
        root1 = Tk()
        patobj = doctor2.Doctor(root1,data2)
        patobj.plot_graph()
        root1.mainloop()
    else:
        root1 = Tk()
        docobj = patient.Patient(root1, data2)
        docobj.get_uid()
        docobj.plot_graph()
        docobj.mltab_funtion()
        root1.mainloop()
else:
    exit(0)
