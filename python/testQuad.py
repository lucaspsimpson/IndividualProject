from QuadTree import QuadTree
import numpy as np
from matplotlib import pyplot as plt
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=False)
import cv2


def draw_grid(ax, xlim, ylim, Nx, Ny, **kwargs):
    """ draw a background grid for the quad tree"""
    for x in np.linspace(xlim[0], xlim[1], Nx):
        ax.plot([x, x], ylim, **kwargs)
    for y in np.linspace(ylim[0], ylim[1], Ny):
        ax.plot(xlim, [y, y], **kwargs)

def main(X):

	#------------------------------------------------------------
	# Create a set of structured random points in two dimensions
	np.random.seed(0)

	# X is a 2 * 30 array. 
	# X = np.random.random((30, 2)) * 2 - 1
	print("X: ", X)
	X[:, 1] *= 0.1
	X[:, 1] += X[:, 0] ** 2

	#------------------------------------------------------------
	# Use our Quad Tree class to recursively divide the space
	mins = (-1.1, -0.1)
	maxs = (1.1, 1.1)

	#mins = (0,0)
	#maxs = (570,240)	

	QT = QuadTree(X, mins, maxs, depth=3)

	#------------------------------------------------------------
	# Plot four different levels of the quad tree
	fig = plt.figure(figsize=(5, 5))
	fig.subplots_adjust(wspace=0.1, hspace=0.15,
		            left=0.1, right=0.9,
		            bottom=0.05, top=0.9)

	for level in range(1, 5):
	    ax = fig.add_subplot(2, 2, level, xticks=[], yticks=[])
	    ax.scatter(X[:, 0], X[:, 1])
	    QT.draw_rectangle(ax, depth=level - 1)

	    Nlines = 1 + 2 ** (level - 1)
	    draw_grid(ax, (mins[0], maxs[0]), (mins[1], maxs[1]),
		      Nlines, Nlines, linewidth=1,
		      color='#CCCCCC', zorder=0)

	    ax.set_xlim(-1.2, 1.2)
	    ax.set_ylim(-0.15, 1.15)
	    ax.set_title('level %i' % level)

	# suptitle() adds a title to the entire figure
	fig.suptitle('Quad-tree Example')
	plt.show()

#main()


imName = "carSpace" + str(4) + ".jpg"
print(imName)
image = cv2.imread( imName)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
(thresh, binImage) = cv2.threshold(gray, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#cv2.imshow("binary", binImage)
#cv2.waitKey(0)

mat  = np.asarray ( binImage, dtype="int32") 

main(mat)

X = np.random.random((30, 2)) * 2 - 1
print("X: ", X)
# data should be two-dimensional
print (mat.shape[1])
#print(mat)
