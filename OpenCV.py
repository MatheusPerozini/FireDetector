import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import cv2

filename = '1.jpg'
threshold = 200

url = os.path.dirname(os.path.abspath(__file__))
img = cv2.imread(url+'/Fire-Detection/1/'+filename)
if img is None:
    print("Imagem não achada")
    print(url+'/Fire-Detection/1/'+filename)

blur = cv2.GaussianBlur(img , (15 , 15) , 0)
hsv = cv2.cvtColor(blur , cv2.COLOR_BGR2HSV)

lowerFire = (0, 115, 155)
upperFire = (30, 255, 255)

lowerFire = np.array(lowerFire , dtype='uint8')
upperFire = np.array(upperFire , dtype='uint8')

mask = cv2.inRange(hsv , lowerFire , upperFire)

outputFogo = cv2.bitwise_and(img , hsv , mask=mask)

tamanhoFogo = cv2.countNonZero(mask)

gray = cv2.cvtColor(outputFogo, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(outputFogo,threshold,255,cv2.THRESH_BINARY)
height, width = thresh.shape[:2]

mass = 0
Xcm  = 0.0
Ycm  = 0.0

for i in range(width) :
    for j in range(height) :
        if not (thresh[j][i]).any() :
            mass += 1
            Xcm  += i
            Ycm  += j

Xcm = Xcm/mass
Ycm = Ycm/mass
fig = plt.figure()
fig.clear()
plot = fig.add_subplot(111)
plot.imshow(thresh, 'gray')
plot.scatter([Xcm], [Ycm], s=30, c='yellow', edgecolors='red')
extent = plot.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
fig.savefig('imagem_final.png', bbox_inches=extent.expanded(1.2, 1.0))