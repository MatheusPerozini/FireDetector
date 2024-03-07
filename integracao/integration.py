import cv2
import os.path
import pickle
from caputarCaracteristicas.getCharsFunctions import *

FILE_NAME = 'video1.mp4'
URL_PATH = os.path.dirname(os.path.abspath(__file__))

# Pega o modelo de IA
with open('modelBayess.pkl', 'rb') as f:
    bayessModel = pickle.load(f)

cap = cv2.VideoCapture()

count = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frameData = frameCaracteristics(frame, count)
        bayessModel.predict([frameData])
        count += 1
    else:
        break