import numpy as np
from matplotlib import pyplot as plt

#----------------------------------------------------------------------
# This function adjusts matplotlib settings for a uniform feel in the textbook.
# Note that with usetex=True, fonts are rendered with LaTeX.  This may
# result in an error if LaTeX is not installed on your system.  In that case,
# you can set usetex to False.
from astroML.plotting import setup_text_plots
setup_text_plots(fontsize=8, usetex=False)


# We'll create a QuadTree class which will recursively subdivide the
# space into quadrants
class QuadTree:
    """Simple Quad-tree class"""

    # class initialization function
    def __init__(self, data, mins, maxs, depth=3):
        self.data = np.asarray(data)

        # data should be two-dimensional
        #assert self.data.shape[1] == 2

        if mins is None:
            mins = data.min(0)
        if maxs is None:
            maxs = data.max(0)

        self.mins = np.asarray(mins)
        self.maxs = np.asarray(maxs)
        self.sizes = self.maxs - self.mins

        self.children = []

        mids = 0.5 * (self.mins + self.maxs)
        xmin, ymin = self.mins
        xmax, ymax = self.maxs
        xmid, ymid = mids

        if depth > 0:
            # split the data into four quadrants
            data_q1 = data[(data[:, 0] < mids[0])
                           & (data[:, 1] < mids[1])]
            data_q2 = data[(data[:, 0] < mids[0])
                           & (data[:, 1] >= mids[1])]
            data_q3 = data[(data[:, 0] >= mids[0])
                           & (data[:, 1] < mids[1])]
            data_q4 = data[(data[:, 0] >= mids[0])
                           & (data[:, 1] >= mids[1])]

            # recursively build a quad tree on each quadrant which has data
            if data_q1.shape[0] > 0:
                self.children.append(QuadTree(data_q1,
                                              [xmin, ymin], [xmid, ymid],
                                              depth - 1))
            if data_q2.shape[0] > 0:
                self.children.append(QuadTree(data_q2,
                                              [xmin, ymid], [xmid, ymax],
                                              depth - 1))
            if data_q3.shape[0] > 0:
                self.children.append(QuadTree(data_q3,
                                              [xmid, ymin], [xmax, ymid],
                                              depth - 1))
            if data_q4.shape[0] > 0:
                self.children.append(QuadTree(data_q4,
                                              [xmid, ymid], [xmax, ymax],
                                              depth - 1))

    def draw_rectangle(self, ax, depth):
        """Recursively plot a visualization of the quad tree region"""
        if depth is None or depth == 0:
            rect = plt.Rectangle(self.mins, *self.sizes, zorder=2,
                                 ec='#000000', fc='none')
            ax.add_patch(rect)
        if depth is None or depth > 0:
            for child in self.children:
                child.draw_rectangle(ax, depth - 1)


