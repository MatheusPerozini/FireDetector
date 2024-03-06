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
        frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        blur = cv2.GaussianBlur(frame , (15 , 15) , 0)
        hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)
        frameRGB2BGR = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)

        XcmFogo, YcmFogo, tamanhoFogo = gerarVideos(LOWER_FIRE_MASK, UPPER_FIRE_MASK, hsv, 'fogo', frame, outFire)
        rgbFogo = pegarValoresRGBImagem(frameRGB2BGR, XcmFogo, YcmFogo)
        movimentoFogo = '?'

        XcmFumaca, YcmFumaca, tamanhoFumaca = gerarVideos(LOWER_SMOKE_MASK, UPPER_SMOKE_MASK, hsv, 'fumaca', frame, outSmoke)
        rgbFumaca = pegarValoresRGBImagem(frameRGB2BGR, XcmFumaca, YcmFumaca)
        movimentoFumaca = '?'

        if count >= 2:
            movimentoFumaca = abs(diferencaTamanhoFumaca[count] - diferencaTamanhoFumaca[count - 2])
            movimentoFogo = abs(diferencaTamanhoFogo[count] - diferencaTamanhoFogo[count - 2])
            f.write("{},{},{},{},{},{},{},{},{},{}\n".format(rgbFogo[0], rgbFogo[1], rgbFogo[2], rgbFumaca[0], rgbFumaca[1], rgbFumaca[2], movimentoFogo, movimentoFumaca, tamanhoFogo, tamanhoFumaca))

        count += 1
    else:
        break

cap.release()
outFire.release()
outSmoke.release()
# Closes all the frames
cv2.destroyAllWindows()