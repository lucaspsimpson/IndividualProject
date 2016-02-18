# plot histogram

import cv2
import numpy as np
from matplotlib import pyplot as plt

imName = 'carSpace4.jpg'
image = cv2.imread( imName)
plt.hist(image.ravel(), 256, [0,256]);
plt.show()
