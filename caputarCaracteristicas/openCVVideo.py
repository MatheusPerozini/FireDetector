import numpy as np
import os.path
import cv2
from getCharsFunctions import *

FILE_NAME = 'video1.mp4'

URL_PATH = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(URL_PATH+'../dataset/'+FILE_NAME)
outFire = cv2.VideoWriter('Fogo.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (IMAGE_WIDTH, IMAGE_HEIGHT))
outSmoke = cv2.VideoWriter('Fumaça.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (IMAGE_WIDTH, IMAGE_HEIGHT))

f = open('data.csv', 'a')
if os.path.isfile('data.csv') == False:
    f.write('rgbFogoR,rgbFogoG,rgbFogoB,rgbFumacaR,rgbFumacaG,rgbFumacaB,qtdMovimentoFogo,qtdMovimentoFumaca,tamanhoFogo,tamamnhoFumaca\n')
else:
    f.write('\n')

if cap.isOpened()== False:
    print("Error opening video stream or file")
    print(URL_PATH+'/Fire-Detection/1/'+FILE_NAME)

count = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if count == 6:
        break
    if ret == True:
        if count >= 2:
            frameData = frameCaracteristics(frame, count, outFire, outSmoke)
            f.write("{},{},{},{},{},{},{},{},{},{}\n".format(frameData))

        count += 1
    else:
        break

cap.release()
outFire.release()
outSmoke.release()
# Closes all the frames
cv2.destroyAllWindows()