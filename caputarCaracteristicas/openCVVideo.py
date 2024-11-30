import numpy as np
import os.path
import cv2
from getCharsFunctions import *
import time

FILE_NAME = 'video28.mp4'

start_time = time.time()
URL_PATH = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(URL_PATH+'/../dataset/'+FILE_NAME)
outFire = cv2.VideoWriter('Fogo.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (IMAGE_WIDTH, IMAGE_HEIGHT))
outSmoke = cv2.VideoWriter('Fumaça.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (IMAGE_WIDTH, IMAGE_HEIGHT))

if os.path.isfile('./caputarCaracteristicas/data.csv') == False:
    f = open('./caputarCaracteristicas/data.csv', 'a')
    f.write('rgbFogoR,rgbFogoG,rgbFogoB,rgbFumacaR,rgbFumacaG,rgbFumacaB,qtdMovimentoFogo,qtdMovimentoFumaca,tamanhoFogo,tamamnhoFumaca')
else:
    f = open('./caputarCaracteristicas/data.csv', 'a')

if cap.isOpened()== False:
    print("Error opening video stream or file")
    print(URL_PATH+'/Fire-Detection/1/'+FILE_NAME)

count = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if count == 20:
        break
    if ret == True:
        frameData = frameCaracteristics(frame, count, outFire, outSmoke)
        if count >= 2:
            f.write("\n{},{},{},{},{},{},{},{},{},{}".format(frameData[0], frameData[1], frameData[2], frameData[3], frameData[4], frameData[5], frameData[6], frameData[7], frameData[8], frameData[9]))

        count += 1
    else:
        break

cap.release()
outFire.release()
outSmoke.release()
# Closes all the frames
cv2.destroyAllWindows()
print("--- %s seconds ---" % (time.time() - start_time))