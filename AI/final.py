from __future__ import print_function
import argparse
import numpy  as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.sampler import SubsetRandomSampler
from torchvision import transforms

from data_loaders import Plain_Dataset, eval_data_dataloader
from deep_emotion import Deep_Emotion
from generate_data import Generate_data
import cv2
import matplotlib.pyplot as plt
from collections import Counter
import serial.tools.list_ports
from Adafruit_IO import MQTTClient
import os
import time

AIO_USERNAME = os.environ['AIO_USERNAME']
AIO_KEY = os.environ['AIO_KEY']
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.connect()
client.loop_background()


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net = Deep_Emotion()
net.load_state_dict(torch.load('deepEmotion.pt'))
net.to(device)

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


writer = cv2.VideoWriter('', cv2.VideoWriter_fourcc(*'XVID'),30, (width, height))
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotions = { 
    0: 'Angry', 
    1: 'Disgust',
    2: 'Fear', 
    3: 'Happy', 
    4: 'Sad', 
    5: 'Surprise', 
    6: 'Neutral'
} 
font = cv2.FONT_HERSHEY_SIMPLEX

face_roi = None
def predict(frame):
    # Model
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.1, 4)
    for x, y, w, h in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        facess = faceCascade.detectMultiScale(roi_gray)
        if len(facess) == 0:
            # print("Face is not detected")
            pass
        else:
            for (ex, ey, ew, eh) in facess:
                global face_roi
                face_roi = roi_color[ey:ey+eh, ex:ex+ew]
    
                final_image = cv2.resize(gray, (48,48))
                final_image = np.expand_dims(final_image, axis=0)
                final_image = np.expand_dims(final_image, axis=0)
                
                final_image = final_image / 255.0
                data = torch.from_numpy(final_image)
                data = data.type(torch.FloatTensor)
                data = data.cuda()
                outputs = net(data)
                pred = F.softmax(outputs, dim=1)
                emotion = torch.argmax(pred).item()
                if emotion in (0, 1, 2, 4):
                    return emotion, 0 # Negative
                else:
                    return emotion, 1 # Positive
    return 0, 1

emotionArr = Counter()
count = 0
emotionIdx = 0

while True:
    ret, frame = cap.read()
    emotion, isPositive = predict(frame)
    emotionArr[isPositive] += 1
    count += 1
    if count == 40:
        emotionIdx = emotionArr.most_common(1)[0][0]
        emotionArr = Counter()
        count = 0
        client.publish(
            'emotion',
            emotionIdx,
        )

    cv2.putText(frame, emotions[emotion], (10,450), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
    writer.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        
cap.release()
writer.release()
cv2.destroyAllWindows()