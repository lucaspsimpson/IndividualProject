# USAGE
# python watershed.py --image images/coins_01.png

# packages
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from skimage import measure
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2

imName = 'carSpace8.jpg'
image = cv2.imread( imName)
shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)

# convert the mean shift image to grayscale, apply Otsu's thresholding
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray" + imName, gray)

thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#cv2.imshow("Thresh", thresh)
#cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

print("Info {} unique contours found".format(len(cnts)))

for (i, c) in enumerate(cnts):

	((x, y), _) = cv2.minEnclosingCircle(c)
	#cv2.putText(image, "#{}".format(i+1), (int(x) -10, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
	cv2.drawContours(image, [c], -1, (0,255,0), 2)

#cv2.imwrite("ContoursImage",image)
cv2.imshow("Image", image)
cv2.waitKey(0)
