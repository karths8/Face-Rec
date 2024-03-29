import os 
from PIL import Image
import cv2
import pickle
import numpy as np
face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir=os.path.join(BASE_DIR,"images")

current_id=0
label_ids={}
y_labels = []
x_train = []

for root,dirs,files in os.walk(image_dir):
    for file in files:
        path=os.path.join(root,file)
        label = os.path.basename(os.path.dirname(path))
        if not label in label_ids:
            label_ids[label] = current_id
            current_id+=1
        id_ = label_ids[label]        
        pil_image = Image.open(path).convert("L")#for grayscale
        image_array = np.array(pil_image,"uint8")#gray image to list of numbers
        faces=face_cascade.detectMultiScale(image_array)
        
        for (x,y,w,h) in faces:
            roi = image_array[y:y+h,x:x+w]
            x_train.append(roi)
            y_labels.append(id_)
            
with open("labels.pickle","wb") as f:
    pickle.dump(label_ids,f)
    
recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainer.yml")