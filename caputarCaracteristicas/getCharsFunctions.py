import numpy as np
import cv2

IMAGE_WIDTH = 700
IMAGE_HEIGHT = 600

LOWER_FIRE_MASK = (120, 27, 0)
UPPER_FIRE_MASK = (179, 255, 255)

LOWER_SMOKE_MASK = (105, 0, 90)
UPPER_SMOKE_MASK = (179, 140, 220)

diferencaTamanhoFogo = []
diferencaTamanhoFumaca = []

def gerarVideos(lower, upper, hsv, type, frame, out):
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
    if out:
        out.write(output)

    return [Xcm, Ycm, tamanho]

def handleCordenates(cordinate, size):
    if cordinate > size:
        return size
    else :    
        return cordinate

def pegarValoresRGBImagem(frame, Xcm, Ycm):
    GRID_SIZE = 9 # 9 x 9
    yGrid = 0
    xGrid = 0
    r = 0
    g = 0
    b = 0
    for i in range(GRID_SIZE):
        if i % 3 == 0:
            xGrid = 1
            yGrid += 1
        rgb = frame[handleCordenates(int((Ycm - 1) + yGrid), IMAGE_HEIGHT),handleCordenates(int((Xcm - 1) + xGrid), IMAGE_WIDTH)]
        xGrid += 1
        r += rgb[0]
        g += rgb[1]
        b += rgb[2]
    return [int(r / GRID_SIZE), int(g / GRID_SIZE), int(b / GRID_SIZE)]

def frameCaracteristics(frame, count, outFogo, outFumaca):
    frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
    blur = cv2.GaussianBlur(frame , (15 , 15) , 0)
    hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)
    frameRGB2BGR = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)
        
    XcmFogo, YcmFogo, tamanhoFogo = gerarVideos(LOWER_FIRE_MASK, UPPER_FIRE_MASK, hsv, 'fogo', frame, outFogo)
    rgbFogo = pegarValoresRGBImagem(frameRGB2BGR, XcmFogo, YcmFogo)
    movimentoFogo = '?'

    XcmFumaca, YcmFumaca, tamanhoFumaca = gerarVideos(LOWER_SMOKE_MASK, UPPER_SMOKE_MASK, hsv, 'fumaca', frame, outFumaca)
    rgbFumaca = pegarValoresRGBImagem(frameRGB2BGR, XcmFumaca, YcmFumaca)
    movimentoFumaca = '?'

    if (count > 2):
        movimentoFumaca = abs(diferencaTamanhoFumaca[count] - diferencaTamanhoFumaca[count - 2])
        movimentoFogo = abs(diferencaTamanhoFogo[count] - diferencaTamanhoFogo[count - 2])

    return rgbFogo[0], rgbFogo[1], rgbFogo[2], rgbFumaca[0], rgbFumaca[1], rgbFumaca[2], movimentoFogo, movimentoFumaca, tamanhoFogo, tamanhoFumaca