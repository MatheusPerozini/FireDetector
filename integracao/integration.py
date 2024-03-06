import cv2
import os.path
import pickle
from caputarCaracteristicas.getCharsFunctions import *

FILE_NAME = 'video1.mp4'
URL_PATH = os.path.dirname(os.path.abspath(__file__))

# Pega o modelo de IA
with open('modelBayess.pkl', 'rb') as f:
    bayessModel = pickle.load(f)

cap = cv2.VideoCapture(URL_PATH+'../dataset/'+FILE_NAME)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        blur = cv2.GaussianBlur(frame , (15 , 15) , 0)
        hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)
        frameRGB2BGR = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)
        
        XcmFogo, YcmFogo, tamanhoFogo = gerarVideos(LOWER_FIRE_MASK, UPPER_FIRE_MASK, outFire, hsv, 'fogo')
        rgbFogo = pegarValoresRGBImagem(frameRGB2BGR, XcmFogo, YcmFogo)
        movimentoFogo = '?'

        XcmFumaca, YcmFumaca, tamanhoFumaca = gerarVideos(LOWER_SMOKE_MASK, UPPER_SMOKE_MASK, outSmoke, hsv, 'fumaca')
        rgbFumaca = pegarValoresRGBImagem(frameRGB2BGR, XcmFumaca, YcmFumaca)
        movimentoFumaca = '?'
        bayessModel.predict([rgbFogo[0], rgbFogo[1], rgbFogo[2], rgbFumaca[0], rgbFumaca[1], rgbFumaca[2], movimentoFogo, movimentoFumaca, tamanhoFogo, tamanhoFumaca])
    else:
        break