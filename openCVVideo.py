import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import cv2

filename = 'video.mp4'

url = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(url+'/'+filename)

out1 = cv2.VideoWriter('Fogo.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (700,600))
out2 = cv2.VideoWriter('Fumaça.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (700,600))

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

        lowerFire = np.array(lowerFire , dtype='uint8')
        upperFire = np.array(upperFire , dtype='uint8')

        maskFire = cv2.inRange(hsv , lowerFire , upperFire)

        outputFogo = cv2.bitwise_and(frame , hsv , mask=maskFire)

        tamanhoFogo = cv2.countNonZero(maskFire)
        print(tamanhoFogo)

        retFire,threshFire = cv2.threshold(outputFogo,30,255,cv2.THRESH_BINARY)
        heightFire, widthFire = threshFire.shape[:2]

        massFire = 0
        XcmFire  = 0.0
        YcmFire  = 0.0

        for i in range(widthFire) :
            for j in range(heightFire) :
                if not all(threshFire[j][i] == 0) :
                    massFire += 1
                    XcmFire  += i
                    YcmFire  += j

        XcmFire = XcmFire/massFire
        YcmFire = YcmFire/massFire
        out1.write(outputFogo)
        # Mascara Fumaça
        lowerSmoke = (0, 0, 130)
        upperSmoke = (179, 50, 255)

        lowerSmoke = np.array(lowerSmoke , dtype='uint8')
        upperSmoke = np.array(upperSmoke , dtype='uint8')

        maskSmoke = cv2.inRange(hsv , lowerSmoke , upperSmoke)

        outputFumaça = cv2.bitwise_and(frame , hsv , mask=maskSmoke)

        tamanhoFumaça = cv2.countNonZero(maskSmoke)
        print(tamanhoFumaça)

        retSmoke,threshSmoke = cv2.threshold(outputFumaça,30,255,cv2.THRESH_BINARY)
        heightSmoke, widthSmoke = threshSmoke.shape[:2]

        massSmoke = 0
        XcmSmoke  = 0.0
        YcmSmoke  = 0.0

        for i in range(widthSmoke) :
            for j in range(heightSmoke) :
                if not all(threshSmoke[j][i] == 0) :
                    massSmoke += 1
                    XcmSmoke  += i
                    YcmSmoke  += j

        XcmSmoke = XcmSmoke/massSmoke
        YcmSmoke = YcmSmoke/massSmoke
        out2.write(outputFumaça)

    else:
        break

cap.release()
out1.release()
out2.release()
 
# Closes all the frames
cv2.destroyAllWindows()