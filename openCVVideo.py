import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import cv2

filename = 'video.mp4'

url = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(url+'/'+filename)
diferencaTamanhoFogo = []
diferencaTamanhoFumaca = []
outFire = cv2.VideoWriter('Fogo.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (700,600))
outSmoke = cv2.VideoWriter('Fumaça.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (700,600))

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

    Xcm = Xcm/mass
    Ycm = Ycm/mass
    out.write(output)

if cap.isOpened()== False:
    print("Error opening video stream or file")
    print(url+'/Fire-Detection/1/'+filename)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame = cv2.resize(frame, (700, 600))
        blur = cv2.GaussianBlur(frame , (15 , 15) , 0)
        hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)

        # Mascara fogo
        lowerFire = (0, 115, 155)
        upperFire = (30, 255, 255)

        gerarVideos(lowerFire, upperFire, outFire, hsv, 'fogo')        
        # Mascara Fumaça
        lowerSmoke = (0, 0, 130)
        upperSmoke = (179, 50, 255)

        gerarVideos(lowerSmoke, upperSmoke, outSmoke, hsv, 'fumaca')
        print(diferencaTamanhoFumaca, diferencaTamanhoFogo)
    else:
        break

cap.release()
outFire.release()
outSmoke.release()
 
# Closes all the frames
cv2.destroyAllWindows()