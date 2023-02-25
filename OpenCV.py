import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import cv2

filename = '42.jpg'

url = os.path.dirname(os.path.abspath(__file__))
img = cv2.imread(url+'/Fire-Detection/1/'+filename)
if img is None:
    print("Imagem não achada")
    print(url+'/Fire-Detection/1/'+filename)

blur = cv2.GaussianBlur(img , (15 , 15) , 0)
hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)

# Mascara fogo
lowerFire = (0, 115, 155)
upperFire = (30, 255, 255)

lowerFire = np.array(lowerFire , dtype='uint8')
upperFire = np.array(upperFire , dtype='uint8')

maskFire = cv2.inRange(hsv , lowerFire , upperFire)

outputFogo = cv2.bitwise_and(img , hsv , mask=maskFire)

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
figFire = plt.figure()
figFire.clear()
plotFIre = figFire.add_subplot(111)
plotFIre.imshow(threshFire, 'gray')
plotFIre.scatter([XcmFire], [YcmFire], s=30, c='yellow', edgecolors='red')
extentFire = plotFIre.get_window_extent().transformed(figFire.dpi_scale_trans.inverted())
figFire.savefig('imagem_fogo.png', bbox_inches=extentFire.expanded(1.2, 1.0))

# Mascara Fumaça
lowerSmoke = (0, 0, 130)
upperSmoke = (179, 50, 255)

lowerSmoke = np.array(lowerSmoke , dtype='uint8')
upperSmoke = np.array(upperSmoke , dtype='uint8')

maskSmoke = cv2.inRange(hsv , lowerSmoke , upperSmoke)

outputFumaça = cv2.bitwise_and(img , hsv , mask=maskSmoke)

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
figSmoke = plt.figure()
figSmoke.clear()
plotSmoke = figSmoke.add_subplot(111)
plotSmoke.imshow(threshSmoke, 'gray')
plotSmoke.scatter([XcmSmoke], [YcmSmoke], s=30, c='yellow', edgecolors='red')
extent = plotSmoke.get_window_extent().transformed(figSmoke.dpi_scale_trans.inverted())
figSmoke.savefig('imagem_fumaca.png', bbox_inches=extent.expanded(1.2, 1.0))