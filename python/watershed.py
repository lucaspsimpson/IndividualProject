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
import quadtree_example

#for i in range(8,9):
	
imName = "carSpace" + str(4) + ".jpg"
print(imName)
image = cv2.imread( imName)
shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)

width, height = image.shape[:2]
print("Width: ", width, "Height: ", height)


# convert the mean shift image to grayscale, apply Otsu's thresholding
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
#cv2.imwrite("gray" + imName, gray)

thresh = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

print ("Thresh: ", thresh)
#cv2.imshow("Thresh", thresh)
#cv2.waitKey(0)


# compute the exact Euclidean distance from every binary
# pixel to the nearest zero pixel, then find peaks in this
# distance map
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=20,
	labels=thresh)

print("localMax: ", localMax)

fig, ax = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax1, ax2, ax3 = ax.ravel()

ax3.plot(localMax[:,1], localMax[:,0], 'r')

markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)


# perform a connected component analysis on the local peaks,
# using 8-connectivity, then appy the Watershed algorithm


cv2.imshow("Output", image)

print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

# loop over the unique labels returned by the Watershed
# algorithm

#quadtree = quadtree_example

points = []

for label in np.unique(labels):

	
	
	# if the label is zero, we are examining the 'background'
	# so simply ignore it
	if label == 0:
		continue

	# otherwise, allocate memory for the label region and draw
	# it on the mask
	mask = np.zeros(gray.shape, dtype="uint8")
	mask[labels == label] = 255


	#print("mask: ", mask)
	# detect contours in the mask and grab the largest one
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	c = max(cnts, key=cv2.contourArea)
	
	#print("cnts: ", cnts)
	#print("c: ", c[0])
	

	# draw a circle enclosing the object
	((x, y), r) = cv2.minEnclosingCircle(c)
	# print("Width * .23: ", width * .23)
	if (r > width  * .2):
		cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
		print("x: ", x, "y: ", y)
		cv2.putText(image, "#{}".format(label), (int(x) - 10, int(y)),
		cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

	# np.reshape(cnts, (2, 2))
	#print("shape", cnts.shape)
	#plt.imshow(cnts[0][0])	
	#print("cnts", cnts[0][0][0])
	myarray = np.asarray(cnts)
	#print("Shape: ", myarray.shape	)
	points.append(myarray[0][0][0])
	
	markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
	labels = watershed(-D, markers, mask=thresh)

# show the output imagew

pointsArray = np.asarray(points, dtype=float)
pointsArray = pointsArray/(400.0)
print("Points: ", pointsArray)
print("Shape: ", pointsArray.shape)
X = np.random.random((30, 2)) * 2 - 1
print("Random 2d " , X)
quadtree_example.main(pointsArray)
#cv2.imshow("Output", image)
cv2.imwrite("Processed" + imName, image)

cv2.waitKey(0)

