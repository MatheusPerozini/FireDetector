import cv2
import os.path
import pickle
import sys
import numpy as np
from sklearn.datasets import make_blobs

sys.path.append('/home/mangellan/Personal/iniciacaoCientifica/caputarCaracteristicas')

from getCharsFunctions import *

FILE_NAME = 'video1.mp4'
URL_PATH = os.path.dirname(os.path.abspath(__file__))

# Pega o modelo de IA
with open('/home/mangellan/Personal/iniciacaoCientifica/modeloIA/modelBayess.pkl', 'rb') as f:
    bayessModel = pickle.load(f)

cap = cv2.VideoCapture(URL_PATH+'/../dataset/'+FILE_NAME)

count = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frameData = frameCaracteristics(frame, count)
        if count > 2:
            data = np.array(frameData).reshape(1, -1)
            result = bayessModel.predict(data)
            print(result)

        count += 1
    else:
        break