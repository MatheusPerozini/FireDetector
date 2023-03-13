import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import cv2

filename = 'video1.mp4'

widthImagem = 700
heightImagem = 600
url = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(url+'/dataset/'+filename)
diferencaTamanhoFogo = []
diferencaTamanhoFumaca = []
outFire = cv2.VideoWriter('Fogo.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (widthImagem, heightImagem))
outSmoke = cv2.VideoWriter('Fumaça.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (widthImagem, heightImagem))
f = open('data.csv', 'a')
#f.write('rgbFogo|rgbFumaca|qtdMovimentoFogo|qtdMovimentoFumaca|tamanhoFogo|tamamnhoFumaca\n')

def pegarValoresRGBImagem(frame, Xcm, Ycm):
    tamanhoGrid = 9 # 9 x 9
    yGrid = 0
    xGrid = 0
    r = 0
    g = 0
    b = 0
    for i in range(tamanhoGrid):
        if i % 3 == 0:
            xGrid = 1
            yGrid += 1
        rgb = frame[int((Xcm - 1) + xGrid), int((Ycm - 1) + yGrid)]
        xGrid += 1
        r += rgb[0]
        g += rgb[1]
        b += rgb[2]
    return [int(r / tamanhoGrid), int(g / tamanhoGrid), int(b / tamanhoGrid)]

def gerarVideos(lower, upper, out, hsv, type):
    lower = np.array(lower , dtype='uint8')
    upper = np.array(upper , dtype='uint8')
    mask = cv2.inRange(hsv , lower , upper)

    output = cv2.bitwise_and(frame , hsv , mask=mask)

    tamanho = cv2.countNonZero(mask)
    if type == 'fogo':
        diferencaTamanhoFogo.append(tamanho)
    else:
        diferencaTamanhoFumaca.append(tamanho)

    ret,thresh = cv2.threshold(output,30,255,cv2.THRESH_BINARY)
    height, width = thresh.shape[:2]

    mass = 0
    Xcm  = 0.0
    Ycm  = 0.0

    for i in range(width) :
        for j in range(height) :
            if not all(thresh[j][i] == 0) :
                mass += 1
                Xcm  += i
                Ycm  += j

    if mass == 0:
        Xcm = 0
        Ycm = 0
    else:
        Xcm = Xcm/mass
        Ycm = Ycm/mass

    output = cv2.circle(output, (int(Xcm), int(Ycm)), 20, (255,0,0), 2)
    out.write(output)
    return [Xcm, Ycm, tamanho]

if cap.isOpened()== False:
    print("Error opening video stream or file")
    print(url+'/Fire-Detection/1/'+filename)

count = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if count == 6:
        break
    if ret == True:
        frame = cv2.resize(frame, (widthImagem, heightImagem))
        blur = cv2.GaussianBlur(frame , (15 , 15) , 0)
        hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)
        frameRGB2BGR = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)

        # Mascara fogo
        lowerFire = (120, 27, 0)
        upperFire = (179, 255, 255)

        XcmFogo, YcmFogo, tamanhoFogo = gerarVideos(lowerFire, upperFire, outFire, hsv, 'fogo')
        rgbFogo = pegarValoresRGBImagem(frameRGB2BGR, XcmFogo, YcmFogo)
        movimentoFogo = '?'
            
        # Mascara Fumaça
        lowerSmoke = (105, 0, 90)
        upperSmoke = (179, 140, 220)

        XcmFumaca, YcmFumaca, tamanhoFumaca = gerarVideos(lowerSmoke, upperSmoke, outSmoke, hsv, 'fumaca')
        rgbFumaca = pegarValoresRGBImagem(frameRGB2BGR, XcmFumaca, YcmFumaca)
        movimentoFumaca = '?'

        if count >= 2:
            movimentoFumaca = abs(diferencaTamanhoFumaca[count] - diferencaTamanhoFumaca[count - 2])
            movimentoFogo = abs(diferencaTamanhoFogo[count] - diferencaTamanhoFogo[count - 2])
            f.write("{}|{}|{}|{}|{}|{}\n".format(rgbFogo, rgbFumaca, movimentoFogo, movimentoFumaca, tamanhoFogo, tamanhoFumaca))

        count += 1
    else:
        break

cap.release()
outFire.release()
outSmoke.release()
# Closes all the frames
cv2.destroyAllWindows()